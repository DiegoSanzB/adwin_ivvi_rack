'<ADbasic Header, Headerversion 001.001>
' Process_Number                 = 6
' Initial_Processdelay           = 1000
' Eventsource                    = Timer
' Control_long_Delays_for_Stop   = No
' Priority                       = High
' Version                        = 1
' ADbasic_Version                = 5.0.8
' Optimize                       = Yes
' Optimize_Level                 = 1
' Info_Last_Save                 = TUD205822  TUD205822\LocalAdmin
'<Header End>
' logampcla: ramps voltage on AO1, recording voltage on MUX1

'Inputs:
'PAR_7 = initial voltage point
'PAR_8 = set voltage point
'PAR_9 = final voltage point
'PAR_10 = total run time
'PAR_11 = actual time
'PAR_12 = actual MUX1 value in bin
'PAR_13 = actual MUX2 value in bin
'PAR_55 = no of points to average over
'PAR_56 = no of loops to wait before measure
'PAR_58 = Gt finished, ready to ramp down to end V : 0 =  not ready ; 1 = ready
'PAR_59 = process status : 1 =  running ; 2 = stopped

'Outputs:
'DATA_2 = averaged MUX1 bin array (maximum length 1048576, so 4 arrays can be handled in parallel)
'DATA_3 = averaged MUX2 bin array (maximum length 1048576, so 4 arrays can be handled in parallel)
'DATA_4 = averaged MUX1 current values array (maximum length 1048576, so 4 arrays can be handled in parallel)
'DATA_5 = averaged MUX2 current values array (maximum length 1048576, so 4 arrays can be handled in parallel)
'DATA_11= bins of the voltages to apply  

DIM DATA_4[65536] as long
DIM DATA_10[65536] as float
DIM DATA_11[65536] as long
DIM DATA_13[65536] as long
DIM rampflag,measureflag,waitflag as long
DIM totalcurrent1,currentV as long
DIM totalcurrent3 as float
DIM index,loops,avcounter,waitcounter,timecounter as long

INIT:
  measureflag= 0 'to start measurement directly after start voltage is reached, then increase output 
  avcounter = 0
  waitcounter = 0
  totalcurrent1 = 0
  'totalcurrent3 = 0
  index = 1 
  timecounter = 1
  loops=0
  currentV = DATA_11[index]
  PAR_8 = currentV
  DAC(1, currentV)
  set_MUX(1010000000b) 'use MUX
  
EVENT:
  PAR_1 = index
  IF  (avcounter=PAR_55) THEN
    PAR_12=totalcurrent1 / PAR_55
    DATA_13[index]=PAR_12
    totalcurrent1=0
    avcounter=0
    INC(index)
  ENDIF
  
  DAC(1,currentV)
  
  IF (loops<PAR_56) THEN
    START_CONV(00011b)
    WAIT_EOC(00011b)
    totalcurrent1 = totalcurrent1 + READADC(1)
    INC(avcounter)
    currentV=DATA_11[index]
    loops=0
  ELSE
    INC(loops)
  ENDIF
  
  IF(index>= PAR_9) THEN 
    PAR_59=2
    DAC(1,32768)
    END
  ENDIF 
