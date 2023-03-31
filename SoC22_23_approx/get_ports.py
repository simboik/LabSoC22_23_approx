
import re

def get_number(string):
	# pattern = r"\[(\d+)(-|:)"
	pattern = r"\[(\d+):"

	# find pattern [ :  in string
	match = re.search(pattern, string)

	#  Sie, ob das Match-Objekt vorhanden ist, um sicherzustellen, dass die Zahl gefunden wurde
	if match:
		# Extrahieren Sie die Zahl aus dem Match-Objekt
		number_str = match.group(1)
    	# Konvertieren Sie die Zahl von String in Integer
		return int(number_str)
	else:
		return None

def check_verilog_file(filename):
    # oeffnen der Datei und Lesen der Zeilen
	with open(filename, 'r') as file:
		lines = file.readlines()

	#  der Zeilen, um Eingangs- und Ausgangsvariablen und Bitbreiten zu finden
	inputs = []
	outputs = []
	for line in lines:
        # , ob es sich um eine Eingangsvariable handelt
		if line.lstrip().startswith('input'):
			input_vars = line.split()[1:]
			for var in input_vars:
				var = get_number(var)
				if isinstance(var, int):
					inputs.append(var)
        # , ob es sich um eine Ausgangsvariable handelt
		elif line.lstrip().startswith('output'):
			output_vars = line.lstrip().split()[1:]
			for var in output_vars:
				var = get_number(var)
				if isinstance(var, int):
					outputs.append(var)

	# check for correct number of ports
	if len(inputs) is not 2 or len(outputs) is not 1:
		print('The file ' + filename + ' does not contain the correct number of ports.')

	# check if input ports have same length
	if inputs[0] is not inputs[1]:
		print('Length of input ports of file ' + filename + ' are not equal!')
	
	return [inputs[0], outputs[0]]




'''



def check_verilog_file(filename):
	# open file and read content
   with open(filename, 'r') as file:
       lines = file.readlines()
   
   # Checking file to find ports and bit widths
inputs = []
outputs = []
for line in lines:
 	# check if port is input
	if line.startswith('input'):
		print('a')
  		input_vars = line.split()[1:]
  		print(input_vars)
  	for var in input_vars:
      		inputs.append(var)
		# check if port is output
		elif line.startswith('output'):
      	output_vars = line.split()[1:]
         for var in output_vars:
         	outputs.append(var)

   # check if file contains correct number of in and output ports
   if len(inputs) != 2 or len(outputs) != 1:
       exit()

   # check if input bit length is the same in both files
   input_widths = [int(var.split('[')[1].split(']')[0]) for var in inputs]
   print(input_widths)
   output_width = int(outputs[0].split('[')[1].split(']')[0])
   if len(set(input_widths)) != 1 or input_widths[0] != output_width:
       exit()

   return input_widths, output_width
'''
