import subprocess
import os
import re
import shutil
import fileinput
from error import *
from get_ports import *

####################################################################
# PREPARATION

# Get the path to the models and executables folders
script_dir = os.path.dirname(os.path.abspath(__file__))
models_dir = os.path.join(script_dir, "models")
executables_dir = os.path.join(script_dir, "executables")

# Create the executables folder if it doesn't already exist
if not os.path.exists(executables_dir):
   os.makedirs(executables_dir)

# Get a list of all the Verilog source files in the models folder
source_files = [os.path.join(models_dir, f) for f in os.listdir(models_dir) if f.endswith(".v")]

####################################################################
# CHECK FILES

# create a copy from the 'models' folder
shutil.copytree('./models', './tmp', ignore=shutil.ignore_patterns('test_bench.v'))

verilog_count = 0

for file in os.listdir('tmp'):
   if file.endswith('.v'):
      verilog_count += 1

# print error message if there are not exactely 2 verilog files in the models folder
if verilog_count != 2:
   print("There are not an approximated and an exact design in the 'models' folder.")
   exit()

######################################################################
# DETERMINE PORTS

# determine number of inputs
ports = []
for file in os.listdir('tmp'):
      ports.append(check_verilog_file('./tmp/'+ file))

if ports[0] != ports[1]:
	  print('Ports of exact and approximate design do not match!')
	  exit()
else:
	  INPUTS = str(ports[0][0])
	  OUTPUTS = str(ports[0][1])

####################################################################
# SAT SOLVER

# create the miter and the .blif file
command = ["yosys", "-c", "miter.ys", "-l", "yosys_log"]
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
print(stdout.decode())
print(stderr.decode())

# get the mapping file
command = ["./mappedblif2cnf.pl", "-m", "EX_vs_APP.blif"]
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
print(stdout.decode())
print(stderr.decode())

# run the SAT solver
print("Running SAT solver...")
command =["./error-metrics-determination/Solver/nbc_minisat_all", "EX_vs_APP.cnf", "EX_vs_APP.map", "input_vectors_dup.txt"]
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
print(stdout.decode())
print(stderr.decode())
print("Finished computation!\n")

# remove temorary folder
shutil.rmtree('./tmp')


# remove duplicates in input_vector.txt file
with open('input_vectors_dup.txt', 'r') as f_in, open('input_vectors.txt', 'w') as f_out:
   # use a set to remove duplicates
   unique_lines = set(f_in.readlines())
   # save file without duplicates
   f_out.writelines(unique_lines)

# Open the input vector file and read the input vectors into a list
with open("input_vectors.txt", "r") as f:
   input_vectors = [line.strip() for line in f]

input_vectors_adapted = []

for vector in input_vectors:
   # regex to convert to format "xxxx xxxx"
   vector = re.sub(" 0$", "", vector)
   vector = re.sub("[0-9]+", "1", vector)
   vector = re.sub("-[0-9]+", "0", vector)
   bits = vector.split(" ")
   input_string = "".join(bits[0:int(len(bits)/2)]) + " " + "".join(bits[int(len(bits)/2):])
   if input_string not in input_vectors_adapted:
      input_vectors_adapted.append(input_string)

with open("input_vectors_adapted.txt", "w+") as f:
   for vector in input_vectors_adapted:
      f.write(vector + "\n")

####################################################################
# PREPARE TESTBENCH

# get module names
with open('var.txt', 'r') as f:
    content = f.read()

# split content into lines and remove first and second line, remove whitespaces at the beginning
lines = content.split('\n')[2:]
module1 = lines[0].lstrip()
module2 = lines[1].lstrip()

# set ports in testbench
for line in fileinput.input('./models/test_bench.v', inplace=True):
   if "tb_ports_in =" in line:
      print('\tparameter tb_ports_in = ' + INPUTS + ';')
   elif "tb_ports_out =" in line:
      print('\tparameter tb_ports_out = ' + OUTPUTS + ';')
   elif "dut1" in line:
      index = line.find('dut1')
      print('\t' + module1 + ' ' + line[index:]),
   elif "dut2" in line:
      index = line.find('dut2')
      print('\t' + module2 + ' ' + line[index:]),
   else:
      print(line),

# cleanup
os.remove('var.txt')
      
####################################################################
# CREATE EXCECUTABLE
      
print("Generating executable...")

# Set the path to the output simulation executable
output_file = os.path.join(executables_dir, "simv")

# Set any additional options for the iverilog compiler
options = ["-Wall"]

# Build the command to compile the source files and generate the simulation executable
command = ["iverilog"] + options + ["-o", output_file] + source_files

# Call iverilog using the subprocess module
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# Read the output from iverilog and print any error messages
output, errors = process.communicate()
if errors:
   print("Compilation failed with errors:")
   print(errors.decode())
else:
   print("Compilation successful!\n")

print("Launch testbench...")


# Launch the simulation executable and pass it the input vectors
process = subprocess.Popen(["./executables/simv"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

# Read the output from the simulation
output = process.stdout.readlines()
print("Finished!\n")

# Write the output to a text file
with open("output_values.txt", "w") as f:
   for line in output:
      f.write(line.strip() + "\n")

#Get the results from the output_values.txt
input_1 = []
input_2 = []
exact_results = []
approx_results = []

exact_results_str = []
approx_results_str = []

with open('output_values.txt', 'r') as f:
   for line in f:
      test_results = line.strip().split()
      input_1.append(test_results[0])
      input_2.append(test_results[1])
      exact_results.append(int(test_results[2], 2))
      exact_results_str.append(test_results[2])
      approx_results.append(int(test_results[3], 2))

nr_error = len(exact_results)
wc_error = worst_case_error(exact_results, approx_results)
max_bf_error = max_bit_flip_error(exact_results, approx_results, exact_results_str[0])
er_rate = error_rate(input_1[0], input_2[0], exact_results, approx_results)
avg_case_error = average_case_error(input_1[0], input_2[0], exact_results, approx_results)

# Print results to console with additional info
print("*********** ERROR METRICES *********** ")
print("Compared modules: " + module1 + ' vs ' + module2)
print("Bit width: " + INPUTS)
print("\n")
print("Total Nr of possible values: {:.2f}".format(2 ** (2*int(INPUTS))))
print("Total Nr of errors: {:.2f}".format(nr_error))
print("Worst Case Error: {:.2f}".format(wc_error))
print("Max Bit Flip Error:", max_bf_error)
print("Error Rate: {:.2f}%".format(er_rate))
print("Average Case Error: {}".format(avg_case_error))

# Save results to file
with open("results.txt", "w") as f:
   f.write("*********** ERROR METRICES ***********\n")
   f.write("Compared modules: " + module1 + ' vs ' + module2)
   f.write("Bit width: " + INPUTS + "\n")
   f.write("\n")
   f.write("Total Nr of possible values: {:.2f}".format(2 ** (2*int(INPUTS))))
   f.write(("Total Nr of errors: {:.2f}\n".format(nr_error)))
   f.write("Worst Case Error: {}\n".format(wc_error))
   f.write("Max Bit Flip Error: {}\n".format(max_bf_error))
   f.write("Error Rate: {:.2f}%\n".format(er_rate))
   f.write("Average Case Error: {}\n".format(avg_case_error))




