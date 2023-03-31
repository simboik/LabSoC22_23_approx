/*
LDIS - Extending the PicoRV32 core with an approximate multiplier
Copyright (C) 2022 - Tobias Kiefer, Dominik Koukola, Maximilian Kern

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
*/
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