//
// Maps $add cell to a carry-lookahead adder implementation
//

module exact (A, B, Y);

	input [1:0] A;
	input [1:0] B;
	output [2:0] Y;
	wire [1:0] G;
	wire [1:0] P;
	wire [2:0] C;

	genvar i;
	generate
		for (i=0; i<=1; i=i+1) begin
			assign Y[i] = A[i] ^ B[i] ^ C[i];
			assign G[i] = A[i] & B[i];
			assign P[i] = A[i] | B[i];
			assign C[i+1] = G[i] | (P[i] & C[i]);
		end
	endgenerate
	
	assign C[0] = 1'b0;
	assign Y[2] = C[2];
endmodule
