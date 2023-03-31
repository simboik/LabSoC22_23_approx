
// Approximated Multiplier 1



module approxmul1 (a, b, out);

	input [1:0] a;
	input [1:0] b;
	output wire [3:0] out;
	
	assign out[0] = a[0] && b[0];
	assign out[1] = (a[0] && b[1]) || (a[1] && b[0]); 
	assign out[2] = a[1] && b[1];
	assign out[3] = 0;

endmodule
