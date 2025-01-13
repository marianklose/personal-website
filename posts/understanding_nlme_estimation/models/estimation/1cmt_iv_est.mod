$PROBLEM 1cmt_iv_est

$INPUT ID TIME EVID AMT RATE DV MDV

$DATA C:\Users\maria\Desktop\G\Mitarbeiter\Klose\Miscellaneous\NLME_reproduction_R\data\output_from_sim\sim_data.csv IGNORE=@

$SUBROUTINES ADVAN1 TRANS2

$PK
; define fixed effects parameters
CL = THETA(1) * EXP(ETA(1))
V = THETA(2)

; scaling
S1=V

$THETA
(0, 0.1, 1)             ; 1 TVCL
3.15 FIX                ; 2 TVV

$OMEGA 
0.15                    ; 1 OM_CL

$SIGMA
0.1 FIX                 ; 1 SIG_ADD

$ERROR 
; add additive error
Y = F + EPS(1)

; store error for table output
ERR1 = EPS(1)

$ESTIMATION METHOD=COND LAPLACIAN MAXEVAL=9999 SIGDIG=3 PRINT=1 NOABORT POSTHOC

$COVARIANCE PRINT=E

$TABLE ID TIME EVID AMT RATE DV MDV ETA1 ERR1 CL NOAPPEND ONEHEADER NOPRINT FILE=estim_out
