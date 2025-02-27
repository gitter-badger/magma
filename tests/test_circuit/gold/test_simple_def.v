// Defined at tests/test_circuit/test_define.py:16
module main (input [1:0] I, output  O);
wire  And2_inst0_O;
// Instanced at tests/test_circuit/test_define.py:18
// Argument I0(I[0]) wired at tests/test_circuit/test_define.py:20
// Argument I1(I[1]) wired at tests/test_circuit/test_define.py:21
// Argument O(And2_inst0_O) wired at tests/test_circuit/test_define.py:22
And2 And2_inst0 (.I0(I[0]), .I1(I[1]), .O(And2_inst0_O));
// Wired at tests/test_circuit/test_define.py:22
assign O = And2_inst0_O;
endmodule

