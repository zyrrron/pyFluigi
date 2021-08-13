# Placement
Cases to consider:
## Floating Connections

### Desicription
This is the scenario where the connection does not metion the terminal to which one needs to connect to.

### Potential Solutions
Predefined Assignment - Incase there's only 1 terminal, then you need to assign it to the that terminal, incase there's more than 1 terminal, assign to closes terminal after placement


# Routing
## Terminal inside cell boundry

### Description
This is the scenario where the terminal is inside the boudary of the PlacementCell and not on the edges. This would be case for components like `PORT` (where the terminal in in the center of the component) and `TRANSPOSER` (the control lines inputs would be inside the boundary connecting to the valves in there).

### Potential Solutions

Option 1 - prioritize the routing
Option 2 - ???


## Current Run Log

```
  grad_cells_no_par.json
     "x-span" and "y-span" is zero for "Component - n1".
	Floating connection appear for "Connection - c5, c6, c7, c8, c9, c10, c11, c12, c13, cc1, cc2, cc3, cc4".
  hasty_no_par.json
     "x-span" and "y-span" is zero for "Component - n1, n2".
     Floating connection appear for "Connection - c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18, c19, c20".
  logic04_no_par.json
     "x-span" and "y-span" is zero for "Component - la, n1".
     Floating connection appear for "Connection - cc21, cc22, cc23, cc24, cc25, cc26".    
  multi_input_no_par.json
     "x-span" and "y-span" is -1 for "Component - ct1".
     No port existes for "Component - ct1".    
     Floating connection appear for "Connection - cc1, cc2, cc3, cc4".  
  net_mux_no_par.json
     "x-span" and "y-span" is zero for "Component - n1,n2,...,n16".
     Floating connection appear.
  rotary_cells_no_par.json
     Floating connection appear.
  rotary16_no_par.json
     Floating connection appear.
  simple_no_par.json
     "x-span" and "y-span" is zero for "Component - n1".
	Some ports are connectted to more than one ports.
     Floating connection appear.
  tdroplet_no_par.json
     "x-span" and "y-span" is zero for "Component - t1,t2".
	Some ports are connectted to more than one ports.
     Floating connection appear.
```
