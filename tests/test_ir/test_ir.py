from magma import DeclareCircuit, DefineCircuit, EndCircuit, In, Out, Bit, \
    wire, Array, array
from magma.ir import compile


def test_print_ir():

    And2 = DeclareCircuit('And2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit)) 

    AndN2 = DefineCircuit("AndN2", "I", In(Array[2, Bit]), "O", Out(Bit) ) 
    and2 = And2() 
    wire( AndN2.I[0], and2.I0 ) 
    wire( AndN2.I[1], and2.I1 ) 
    wire( and2.O, AndN2.O ) 
    EndCircuit() 

    main = DefineCircuit("main", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit)) 
    and2 = AndN2() 
    main.O( and2(array([main.I0, main.I1])) ) 
    EndCircuit() 

    result = compile(main)
    #print(result)
    assert result == """\
AndN2 = DefineCircuit("AndN2", "I", Array[2, In(Bit)], "O", Out(Bit))
And2_inst0 = And2()
wire(AndN2.I[0], And2_inst0.I0)
wire(AndN2.I[1], And2_inst0.I1)
wire(And2_inst0.O, AndN2.O)
EndCircuit()
main = DefineCircuit("main", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))
AndN2_inst0 = AndN2()
wire(main.I0, AndN2_inst0.I[0])
wire(main.I1, AndN2_inst0.I[1])
wire(AndN2_inst0.O, main.O)
EndCircuit()
"""
#    assert result == """\
#And2 = DefineCircuit("And2", "I", Array(2,In(Bit)), "O", Out(Bit))  # {filename} 10
#inst0 = And2()  # {filename} 11
#wire(And2.I[0], inst0.I0)  # {filename} 12
#wire(And2.I[1], inst0.I1)  # {filename} 13
#wire(inst0.O, And2.O)  # {filename} 14
#EndCircuit()  # {filename} 15
#
#main = DefineCircuit("main", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))  # {filename} 17
#inst0 = And2()  # {filename} 18
#wire(main.I0, inst0.I[0])  # {filename} 19
#wire(main.I1, inst0.I[1])  # {filename} 19
#wire(inst0.O, main.O)  # {filename} 19
#EndCircuit()  # {filename} 20
#
#""".format(filename=__file__)

