import magma as m
import magma.testing
import os

def check_port(definition, port, type, direction):
    assert hasattr(definition, port)
    port = getattr(definition, port)
    assert isinstance(port, type)
    if direction == "input":
        assert port.isoutput()
    elif direction == "output":
        assert port.isinput()
    else:
        raise NotImplementedError(direction)

def check_rxmod(RXMOD):
    check_port(RXMOD, "RX", m.BitType, "input")
    check_port(RXMOD, "CLK", m.BitType, "input")
    check_port(RXMOD, "data", m.ArrayType, "output")
    check_port(RXMOD, "valid", m.BitType, "output")

    m.compile("build/test_rxmod", RXMOD)
    assert m.testing.check_files_equal(__file__, "build/test_rxmod.v",
            "gold/test_rxmod.v")    

def test_basic():
    file_path = os.path.dirname(__file__)
    RXMOD = m.DefineFromVerilogFile(os.path.join(file_path, "rxmod.v"))[0]

    check_rxmod(RXMOD)


def test_target_modules_arg():
    file_path = os.path.dirname(__file__)
    circuits = m.DefineFromVerilogFile(os.path.join(file_path, "rxmod.v"), ["RXMOD"])
    assert len(circuits) == 1
    assert circuits[0].name == "RXMOD"

    check_rxmod(circuits[0])


def test_coreir_compilation():
    file_path = os.path.dirname(__file__)
    RXMOD = m.DefineFromVerilogFile(os.path.join(file_path, "rxmod.v"))[0]

    top = m.DefineCircuit("top",
                          "RX", m.In(m.Bit),
                          "CLK", m.In(m.Bit),
                          "data", m.Out(m.Bits(8)),
                          "valid", m.Out(m.Bit))
    RXMOD_inst = RXMOD()
    m.wire(top.RX, RXMOD_inst.RX)
    m.wire(top.CLK, RXMOD_inst.CLK)
    m.wire(top.data, RXMOD_inst.data)
    m.wire(top.valid, RXMOD_inst.valid)
    m.EndCircuit()

    m.compile("build/test_rxmod_top", top, output="coreir")

    assert m.testing.check_files_equal(
        __file__, "build/test_rxmod_top.json", "gold/test_rxmod_top.json")
