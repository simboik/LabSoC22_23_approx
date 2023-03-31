module testbench;







  // Declare inputs and outputs for DUT



	parameter tb_ports_in = 1;
	parameter tb_ports_out = 3;
  reg [tb_ports_in:0] A, B, A_ex, A_ap, B_ex, B_ap;



  wire [tb_ports_out:0] S_ex, S_ap;







  // Instantiate DUT



	accumul dut1(A_ex, B_ex, S_ex);



	approxmul1 dut2(A_ap, B_ap, S_ap);



  



  // Declare file handle for reading input vectors from STDIN



  integer input_file;



  integer input_file2;







  initial begin



    // Open STDIN for reading input vectors



    input_file = $fopen("input_vectors_adapted.txt", "r");



    



    // Loop over input vectors



    while (!$feof(input_file)) begin



      // Read input vector from STDIN



      input_file2 = $fscanf(input_file, "%b %b\n", A, B);



      A_ex = A;



      A_ap = A;



      B_ex = B;



      B_ap = B;



      // Evaluate DUT



      #1; // Delay to allow DUT to settle







      // Print output to console



      $display("%b %b %b %b", A, B, S_ex, S_ap);



    end







    // Close file handle



    $fclose(input_file);







    // Finish simulation



    $finish;



  end







endmodule



