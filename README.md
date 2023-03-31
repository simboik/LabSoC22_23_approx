# LabSoC22_23_approx
Pipeline to evaluate exact and approximate integrated circuits

#################################################################################################
# 		      Approximate Design Trade-Off Evaluation Tool v1.0									#												
#																								#
# developed by: Lukas Baumgartner, Simon Boike, Verena Dangl, Tobias Kiefer, Moritz Steinhauser # 
#																								#
# Labor SoC Design 384.178 ICT TU Wien															#
#																								#
# 06.03.2023																					#
#################################################################################################

This is the installation and user guide for the approximate design trade off evaluation tool.

Prerequisites:
The tool uses the following open source IPs:
[yosys] 0.10+1
[ikarus iverilog] 10.3
[SAT-Solver] source: https://github.com/AliRady/error-metrics-determination/ (no need to install when using the provided repository)

Interpreters
[Python] 2 any version

Setup Guide:
Once the needed IPs are installed the pipeline can be started.
Two Verilog files of the approximate DUT and its exact equivalent have to be provided and saved in the "models" folder. The testbench.v file has to remain in the models folder.
Works for any pair of Verilog files, each of which has 2 inputs of arbitrary, but equal bit width, and one associated output.

EXAMPLE:
The input/outputs need to be specified using:
input [X:0] input_port_name1 
input [X:0] input_port_name2
output [Y:0] output_port_name

in both verilog files (exact and approximated). No additional in or outputs should be defined. No X-1 or Y-1 notation should be used.
Each of the verilog files should just contain one module.


The evaluation is started with the console command "python approx_evaluation.py"

During the evaluation the models go through the following steps:
- SAT-Solver search for satisfiability vectors where the output of the two modules differ from another
	-generation of the "input_vectors.txt"
- simulation of the modules and calculation of the modules outputs for each input vector found by the satisfiability function
	-generation of the "output_values.txt"
- evaluation of the error metrics of the given module based on the results of the step before
	-output on the console
	-generation of "results.txt"
-results.txt contains the calculated error metrics
