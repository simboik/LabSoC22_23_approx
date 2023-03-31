//
// Maps $add cell to a carry-lookahead adder implementation
//

module exact (A, B, Y);
	input [5:0] A;
	input [5:0] B;
	output [6:0] Y;
	wire [5:0] G;
	wire [5:0] P;
	wire [6:0] C;

	genvar i;
	generate
		for (i=0; i<=5; i=i+1) begin
			assign Y[i] = A[i] ^ B[i] ^ C[i];
			assign G[i] = A[i] & B[i];
			assign P[i] = A[i] | B[i];
			assign C[i+1] = G[i] | (P[i] & C[i]);
		end
	endgenerate
	
	assign C[0] = 1'b0;
	assign Y[6] = C[6];
endmodule
