// Module `Mux2_x4` defined externally
// Module `Mux2` defined externally
module coreir_reg_arst #(parameter width = 1, parameter arst_posedge = 1, parameter clk_posedge = 1, parameter init = 1) (input clk, input arst, input [width-1:0] in, output [width-1:0] out);
  reg [width-1:0] outReg;
  wire real_rst;
  assign real_rst = arst_posedge ? arst : ~arst;
  wire real_clk;
  assign real_clk = clk_posedge ? clk : ~clk;
  always @(posedge real_clk, posedge real_rst) begin
    if (real_rst) outReg <= init;
    else outReg <= in;
  end
  assign out = outReg;
endmodule

module coreir_eq #(parameter width = 1) (input [width-1:0] in0, input [width-1:0] in1, output out);
  assign out = in0 == in1;
endmodule

module coreir_const #(parameter width = 1, parameter value = 1) (output [width-1:0] out);
  assign out = value;
endmodule

module corebit_const #(parameter value = 1) (output out);
  assign out = value;
endmodule

module corebit_and (input in0, input in1, output out);
  assign out = in0 & in1;
endmodule

module Register_comb (output [3:0] O0, output [3:0] O1, input en, input [3:0] self_value_O, input [3:0] value);
wire [3:0] Mux2_x4_inst0_O;
Mux2_x4 Mux2_x4_inst0(.I0(self_value_O), .I1(value), .O(Mux2_x4_inst0_O), .S(en));
assign O0 = Mux2_x4_inst0_O;
assign O1 = self_value_O;
endmodule

module Register (input ASYNCRESET, input CLK, output [3:0] O, input en, input [3:0] value);
wire [3:0] Register_comb_inst0_O0;
wire [3:0] Register_comb_inst0_O1;
wire [3:0] reg_PR_inst0_out;
Register_comb Register_comb_inst0(.O0(Register_comb_inst0_O0), .O1(Register_comb_inst0_O1), .en(en), .self_value_O(reg_PR_inst0_out), .value(value));
coreir_reg_arst #(.arst_posedge(1), .clk_posedge(1), .init(4'h0), .width(4)) reg_PR_inst0(.arst(ASYNCRESET), .clk(CLK), .in(Register_comb_inst0_O0), .out(reg_PR_inst0_out));
assign O = Register_comb_inst0_O1;
endmodule

module RegisterMode_comb (output [3:0] O0, output O1, output [3:0] O2, output [3:0] O3, input clk_en, input [3:0] config_data, input config_we, input [3:0] const_, input [1:0] mode, input [3:0] self_register_O, input [3:0] value);
wire Mux2_inst0_O;
wire Mux2_inst1_O;
wire Mux2_inst2_O;
wire [3:0] Mux2_x4_inst0_O;
wire [3:0] Mux2_x4_inst1_O;
wire [3:0] Mux2_x4_inst2_O;
wire [3:0] Mux2_x4_inst3_O;
wire [3:0] Mux2_x4_inst4_O;
wire [3:0] Mux2_x4_inst5_O;
wire [3:0] Mux2_x4_inst6_O;
wire [3:0] Mux2_x4_inst7_O;
wire [3:0] Mux2_x4_inst8_O;
wire bit_const_0_None_out;
wire bit_const_1_None_out;
wire [1:0] const_0_2_out;
wire [1:0] const_1_2_out;
wire eq_inst0_out;
wire eq_inst1_out;
wire eq_inst2_out;
Mux2 Mux2_inst0(.I0(clk_en), .I1(bit_const_0_None_out), .O(Mux2_inst0_O), .S(eq_inst2_out));
Mux2 Mux2_inst1(.I0(Mux2_inst0_O), .I1(bit_const_0_None_out), .O(Mux2_inst1_O), .S(eq_inst1_out));
Mux2 Mux2_inst2(.I0(Mux2_inst1_O), .I1(bit_const_1_None_out), .O(Mux2_inst2_O), .S(eq_inst0_out));
Mux2_x4 Mux2_x4_inst0(.I0(value), .I1(value), .O(Mux2_x4_inst0_O), .S(eq_inst2_out));
Mux2_x4 Mux2_x4_inst1(.I0(self_register_O), .I1(value), .O(Mux2_x4_inst1_O), .S(eq_inst2_out));
Mux2_x4 Mux2_x4_inst2(.I0(self_register_O), .I1(self_register_O), .O(Mux2_x4_inst2_O), .S(eq_inst2_out));
Mux2_x4 Mux2_x4_inst3(.I0(Mux2_x4_inst0_O), .I1(value), .O(Mux2_x4_inst3_O), .S(eq_inst1_out));
Mux2_x4 Mux2_x4_inst4(.I0(Mux2_x4_inst1_O), .I1(const_), .O(Mux2_x4_inst4_O), .S(eq_inst1_out));
Mux2_x4 Mux2_x4_inst5(.I0(Mux2_x4_inst2_O), .I1(self_register_O), .O(Mux2_x4_inst5_O), .S(eq_inst1_out));
Mux2_x4 Mux2_x4_inst6(.I0(Mux2_x4_inst3_O), .I1(config_data), .O(Mux2_x4_inst6_O), .S(eq_inst0_out));
Mux2_x4 Mux2_x4_inst7(.I0(Mux2_x4_inst4_O), .I1(self_register_O), .O(Mux2_x4_inst7_O), .S(eq_inst0_out));
Mux2_x4 Mux2_x4_inst8(.I0(Mux2_x4_inst5_O), .I1(self_register_O), .O(Mux2_x4_inst8_O), .S(eq_inst0_out));
corebit_const #(.value(0)) bit_const_0_None(.out(bit_const_0_None_out));
corebit_const #(.value(1)) bit_const_1_None(.out(bit_const_1_None_out));
coreir_const #(.value(2'h0), .width(2)) const_0_2(.out(const_0_2_out));
coreir_const #(.value(2'h1), .width(2)) const_1_2(.out(const_1_2_out));
corebit_and eq_inst0(.in0(config_we), .in1(bit_const_1_None_out), .out(eq_inst0_out));
coreir_eq #(.width(2)) eq_inst1(.in0(mode), .in1(const_0_2_out), .out(eq_inst1_out));
coreir_eq #(.width(2)) eq_inst2(.in0(mode), .in1(const_1_2_out), .out(eq_inst2_out));
assign O0 = Mux2_x4_inst6_O;
assign O1 = Mux2_inst2_O;
assign O2 = Mux2_x4_inst7_O;
assign O3 = Mux2_x4_inst8_O;
endmodule

module RegisterMode (input ASYNCRESET, input CLK, output [3:0] O0, output [3:0] O1, input clk_en, input [3:0] config_data, input config_we, input [3:0] const_, input [1:0] mode, input [3:0] value);
wire [3:0] RegisterMode_comb_inst0_O0;
wire RegisterMode_comb_inst0_O1;
wire [3:0] RegisterMode_comb_inst0_O2;
wire [3:0] RegisterMode_comb_inst0_O3;
wire [3:0] Register_inst0_O;
RegisterMode_comb RegisterMode_comb_inst0(.O0(RegisterMode_comb_inst0_O0), .O1(RegisterMode_comb_inst0_O1), .O2(RegisterMode_comb_inst0_O2), .O3(RegisterMode_comb_inst0_O3), .clk_en(clk_en), .config_data(config_data), .config_we(config_we), .const_(const_), .mode(mode), .self_register_O(Register_inst0_O), .value(value));
Register Register_inst0(.ASYNCRESET(ASYNCRESET), .CLK(CLK), .O(Register_inst0_O), .en(RegisterMode_comb_inst0_O1), .value(RegisterMode_comb_inst0_O0));
assign O0 = RegisterMode_comb_inst0_O2;
assign O1 = RegisterMode_comb_inst0_O3;
endmodule

