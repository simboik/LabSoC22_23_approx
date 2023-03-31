//
// Maps $add cell to a carry-lookahead adder implementation
//

module approx (A, B, Y);
	parameter p = 1; // number of approximated bits

	input [1:0] A;
	input [1:0] B;
	output [2:0] Y;
	wire [1:0] G;
	wire [1:0] P;
	wire [2:p] C;

	genvar i;
	
	// approximate
	generate
		for (i=0; i<=p-1; i=i+1) begin
			assign Y[i] = A[i] | B[i];
		end
	endgenerate
	
	// exact
	generate
		for (i=p; i<=1; i=i+1) begin
			assign Y[i] = A[i] ^ B[i] ^ C[i];
			assign G[i] = A[i] & B[i];
			assign P[i] = A[i] | B[i];
			assign C[i+1] = G[i] | (P[i] & C[i]);
		end
	endgenerate
	
	if (p>0) 
		assign C[p] = A[p-1] & B[p-1];
	else
		assign C[0] = 1'b0;
	
	assign Y[2] = C[2];
endmodule
