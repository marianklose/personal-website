$PROBLEM 1cmt_iv_map_est

$INPUT ID TIME EVID AMT RATE DV MDV

$DATA C:\Users\mklose\Desktop\GitHub\personal-website\posts\bayes_map_estimation_r\data\sim_data_ID5.csv IGNORE=@
; $DATA C:\Users\maria\Documents\GitHub\personal-website\posts\bayes_map_estimation_r\data\sim_data_ID5.csv IGNORE=@

$SUBROUTINES ADVAN1 TRANS2

$PK
; define fixed effects parameters
CL = THETA(1) * EXP(ETA(1))
V = THETA(2)

; scaling
S1=V

$THETA
0.247 FIX               ; 1 TVCL
3.15 FIX                ; 2 TVV

$OMEGA 
0.11 FIX                ; 1 OM_CL

$SIGMA
0.50 FIX                ; 1 SIG_PROP
2.00 FIX                ; 2 SIG_ADD

$ERROR 
; add residual unexplained variability
IPRED = F
Y = IPRED + IPRED * EPS(1) + EPS(2)

$ESTIMATION METHOD=1 INTERACTION MAXEVAL=0 SIGDIG=3 PRINT=1 NOABORT POSTHOC

$TABLE ID TIME EVID AMT RATE DV PRED IPRED MDV ETA1 CL NOAPPEND ONEHEADER NOPRINT FILE=map_estim_out
