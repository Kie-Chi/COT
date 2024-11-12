`timescale 1ns / 1ps

module mips_tb;
	reg clk;
	reg reset;
	mips uut (
		.clk(clk), 
		.reset(reset)
	);

	initial begin
		clk = 0;
		reset = 0;
		reset = 1;
		#10;
        #2 reset = 0;
	end
	always #1 clk = ~clk;
      
endmodule


