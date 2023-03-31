//
// Maps $add cell to a carry-lookahead adder implementation
//

module exact (A, B, Y);
	input [7:0] A;
	input [7:0] B;
	output [8:0] Y;
	wire [7:0] G;
	wire [7:0] P;
	wire [8:0] C;

	genvar i;
	generate
		for (i=0; i<=7; i=i+1) begin
			assign Y[i] = A[i] ^ B[i] ^ C[i];
			assign G[i] = A[i] & B[i];
			assign P[i] = A[i] | B[i];
			assign C[i+1] = G[i] | (P[i] & C[i]);
		end
	endgenerate
	
	assign C[0] = 1'b0;
	assign Y[8] = C[8];
endmodule
