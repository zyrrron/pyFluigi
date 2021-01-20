DEVICE flow_focus

LAYER FLOW 

PORT p_in portRadius=100 ;
PORT p_oil_1 portRadius=100 ;
PORT p_oil_2 portRadius=100 ;
PORT p_out portRadius=100 ;
NOZZLE DROPLET GENERATOR ff oilChannelWidth=100 waterChannelWidth=400 ;

NODE n1, n2;

CHANNEL c1 from ff 1 to n1  width=100  ;
CHANNEL c2 from n1  to n2  width=20  ;
CHANNEL c3 from n2 to p_out width=100  ; 

END LAYER

