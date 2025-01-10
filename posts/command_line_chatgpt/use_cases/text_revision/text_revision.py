##################################################################
##################### LIBRARY ####################################
##################################################################

# Load packages
import os
import json
import math
import pandas as pd
from docx import Document
from openai import OpenAI

##################################################################
##################### PREAMBLE ###################################
##################################################################

# Initialize OpenAI client
client = OpenAI()

# Define model
gpt_model = "gpt-4o"

##################################################################
##################### FUNCTIONS ##################################
##################################################################

# Function to split text into n nearly equal chunks
def split_text(text, n_chunks):
    words = text.split()
    chunk_size = math.ceil(len(words) / n_chunks)
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

##################################################################
##################### DATA #######################################
##################################################################

# Load the document
doc_path = "pharmacokinetics.docx"
document = Document(doc_path)

# Extract full text from the docx
full_text = "\n".join([para.text for para in document.paragraphs])

# Split the text into n chunks
chunks = split_text(full_text, 5)

##################################################################
##################### PROMPT #####################################
##################################################################

# Define system and base user messages for review
system_message = "You are a professor reviewing a manuscript."
base_user_message = (
    "Please review the following text excerpt for style, errors, conciseness, and understandability. "
    "Provide detailed comments in JSON format according to the given schema."
)

# Define the JSON schema for the response
json_schema = {
  "name": "review_comments",
  "schema": {
    "type": "object",
    "properties": {
      "comments": {
        "type": "array",
        "description": "A list of review comments with their respective positions in the text.",
        "items": {
          "type": "object",
          "properties": {
            "position": {
              "type": "integer",
              "description": "The position in the text where the comment should be placed."
            },
            "comment": {
              "type": "string",
              "description": "The actual review comment."
            }
          },
          "required": [
            "position",
            "comment"
          ],
          "additionalProperties": False
        }
      }
    },
    "required": [
      "comments"
    ],
    "additionalProperties": False
  },
  "strict": True
}

##################################################################
##################### API CALL LOOP ##############################
##################################################################

# Lists to store responses and structured responses
responses = []
structured_responses = []

# Loop over each chunk, call the API, and process the response
for idx, chunk in enumerate(chunks):
    # Prepare user message for the current chunk
    user_message = f"{base_user_message}\n\nExcerpt:\n{chunk}"

    try:
        # Make the API request with response_format using the defined JSON schema
        completion = client.chat.completions.create(
            model=gpt_model,
            response_format={
                "type": "json_schema",
                "json_schema": json_schema
            },
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
        )

        # Extract the response content
        response_text = completion.choices[0].message.content

        # Parse the JSON response
        response_json = json.loads(response_text)

        # It's assumed that the response JSON adheres to the schema provided.
        # Add the current chunk index to each comment for reference.
        for comment in response_json.get("comments", []):
            comment["chunk_index"] = idx

        # Store raw response
        responses.append(response_json)

        # Structure the response for dataframe storage
        structured_responses.append({
            "chunk_index": idx,
            "comments": response_json.get("comments", [])
        })

        # Optional: Print progress
        print(f"Processed chunk {idx + 1}/{len(chunks)}")

    except Exception as e:
        print(f"Error at chunk {idx}: {e}")

##################################################################
##################### SAVE RESULTS ###############################
##################################################################

# Create a DataFrame from the structured responses
df = pd.DataFrame(structured_responses)

# Define output directory and file name
output_dir = "output_reviews"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "review_comments.csv")

# Save the DataFrame to the specified output directory
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print(f"Review comments saved to {output_file}")
