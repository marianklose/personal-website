##################################################################
##################### LIBRARY ####################################
##################################################################

# Load packages
import os
import math
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
    "Provide detailed comments."
)

##################################################################
##################### API CALL LOOP ##############################
##################################################################

# Loop over each chunk, call the API, and process the response
for idx, chunk in enumerate(chunks):
    # Prepare user message for the current chunk
    user_message = f"{base_user_message}\n\nExcerpt:\n{chunk}"

    try:
        # Make the API request
        completion = client.chat.completions.create(
            model=gpt_model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
        )

        # Extract the response content
        response_text = completion.choices[0].message.content

        # Add comments directly into the document with line breaks and '> xxx'
        document.add_paragraph(f"\n> Feedback for chunk {idx + 1}:\n{response_text}")

        # Optional: Print progress
        print(f"Processed chunk {idx + 1}/{len(chunks)}")

    except Exception as e:
        print(f"Error at chunk {idx}: {e}")

##################################################################
##################### SAVE RESULTS ###############################
##################################################################

# Define output directory and file name
output_dir = "output_reviews"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "reviewed_document.docx")

# Save the updated document
document.save(output_file)

print(f"Reviewed document saved to {output_file}")
