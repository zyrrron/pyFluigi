DEVICE flow_focus

LAYER FLOW 

PORT p_in r=100 ;
PORT p_oil_1 r=100 ;
PORT p_oil_2 r=100 ;
PORT p_out r=100 ;
DROPLETGENERATOR ff radius=100 oilChannelWidth=100 waterChannelWidth=40 angle=30 ;

CHANNEL c1 from ff 1 to ff 1 width=100  ;
CHANNEL c2 from n1 3 to n1 3 width=20  ;
CHANNEL c3 from n2 3 to n2 3 width=100  ; 

END LAYER

