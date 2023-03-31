This software requires a mitered circuit in the form of a .blif file as input. This can be done in a hardware package such as the Yosys package. For convinence, steps are given to miter two circuits from their verilog description in Yosys to a mitered .blif circuit. In order to download the Yosys package, use the following link: https://github.com/YosysHQ/yosys 

====================
========YOSYS=======
====================
The following is an example of the steps taken in Yosys to establish the mitered circuit. The user is free to follow different steps under their own discretion. 
1. use: read_verilog [options] [filename]
	to read both input files
2. use: miter -equiv [options] gold_name gate_name miter_name
	to miter the two circuits together. To know the token name of the circuits in yosys, "stats" can be used. 
	The options to use with miter are: -flatten and -make_outputs
3. delete the original two circuits using "delete" and the token name
4. Use the command "synth" 
	to synthesize the circuit into basic units (gates)
5. print the circuit in blif format using "write_blif"
	to have it as input for the next step
====================
===MAPPEDBLIF2CNF===
====================
A modified script (based on: https://github.com/Shubhankar007/ECEN-699/tree/master/blif2cnf)  that produces a CNF file for SAT solver usage along with a map file that maps primary inputs and outputs to their respective integer variable within the CNF file. 

1. Simply call the mappedblif2cnf.pl script with the blif file as input. The option -m produces a map that states the number of inputs and outputs and numerates the variable numbers corresponding to inputs and outputs in the produced cnf file. The option -M produces a detailed map with each variable name and its corresponding variable number in the cnf file. 

=====================
=====ALLSATSOLVER====
=====================
The SAT solver used is a modified solver based on the modified minisat solver found in  ww.sd.is.uec.ac.jp/toda/code/nbc_minisat_all.html. 

Use the command in the form: ./nbc_minisat_all [CNFFILE] [MAPFILE] [log1] [log2]
	After the program runs:
	[log1] will contain enumerated input assignments that produce errrors 
	[log2] can (optionally) calculate difference between two circuits per errorus input 
=====================
