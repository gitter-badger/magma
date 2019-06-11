import magma as m
from test_combinational import compile_and_check, phi
from collections import Sequence
import coreir

default_port_mapping = {
    "I": "in",
    "I0": "in0",
    "I1": "in1",
    "O": "out",
    "S": "sel",
}


def DeclareCoreirCircuit(*args, **kwargs):
    return m.DeclareCircuit(*args, **kwargs,
                            renamed_ports=default_port_mapping)


@m.cache_definition
def DefineCoreirReg(width, init=0, has_reset=False, T=m.Bits):
    if width is None:
        width = 1
    name = "reg_P"  # TODO: Add support for clock interface
    config_args = {"init": coreir.type.BitVector[width](init)}
    gen_args = {"width": width}
    T = T[width]
    io = ["I", m.In(T), "clk", m.In(m.Clock), "O", m.Out(T)]
    methods = []

    def reset(self, condition):
        wire(condition, self.rst)
        return self

    if has_reset:
        io.extend(["arst", m.In(m.AsyncReset)])
        name += "R"  # TODO: This assumes ordering of clock parameters
        # methods.append(circuit_type_method("reset", reset))
        # gen_args["has_rst"] = True

    def when(self, condition):
        wire(condition, self.en)
        return self

    # if has_ce:
    #     io.extend(["en", In(Enable)])
    #     name += "E"  # TODO: This assumes ordering of clock parameters
    #     methods.append(circuit_type_method("when", when))
    #     gen_args["has_en"] = True

    # default_kwargs = gen_args.copy()
    default_kwargs = {"init": coreir.type.BitVector[width](init)}
    # default_kwargs.update(config_args)

    return DeclareCoreirCircuit(
        name,
        *io,
        stateful=True,
        circuit_type_methods=methods,
        default_kwargs=default_kwargs,
        coreir_genargs=gen_args,
        coreir_configargs=config_args,
        coreir_name="reg_arst" if has_reset else "reg",
        verilog_name="coreir_" + ("reg_arst" if has_reset else "reg"),
        coreir_lib="coreir"
    )


@m.cache_definition
def DefineRegister(n, init=None, has_ce=False, has_reset=False,
                   has_async_reset=False, _type=m.Bits):
    T = _type[n]
    return DefineCoreirReg(n, init, has_async_reset, _type)


def Register(n, init=0, has_ce=False, has_reset=False, has_async_reset=False,
             **kwargs):
    return DefineRegister(n, init, has_ce, has_reset,
                          has_async_reset)(**kwargs)


def pytest_generate_tests(metafunc):
    if 'target' in metafunc.fixturenames:
        metafunc.parametrize("target", ["coreir", "coreir-verilog"])


def _run_verilator(circuit, directory):
    import subprocess
    def run_from_directory(cmd):
        return subprocess.call(cmd, cwd=directory, shell=True)
    top = circuit.name
    assert not run_from_directory(
        f"verilator -Wall -Wno-INCABSPATH -Wno-DECLFILENAME --cc {top}.v "
        f"--exe ../{top}_driver.cpp --top-module {top}")
    assert not run_from_directory(
        f"make -C obj_dir -j -f V{top}.mk V{top}")
    assert not run_from_directory(
        f"./obj_dir/V{top}")


def test_seq_simple(target):
    @m.circuit.sequential
    class TestBasic:
        def __init__(self):
            self.x: m.Bits[2] = m.bits(0, 2)
            self.y: m.Bits[2] = m.bits(0, 2)

        def __call__(self, I: m.Bits[2]) -> m.Bits[2]:
            O = self.y
            self.y = self.x
            self.x = I
            return O

    compile_and_check("TestBasic", TestBasic, target)
    if target == "coreir-verilog":
        """
        The following sequence was used to create the verilator driver:

        tester = fault.Tester(TestBasic, clock=TestBasic.CLK)
        tester.circuit.I = 1
        tester.step(2)
        tester.circuit.I = 2
        tester.step(2)
        tester.circuit.O.expect(1)
        tester.circuit.I = 3
        tester.step(2)
        tester.circuit.O.expect(2)
        tester.circuit.I = 0
        tester.step(2)
        tester.circuit.O.expect(3)

        """
        _run_verilator(TestBasic, directory="tests/test_syntax/build")


def test_seq_hierarchy(target):

    def DefineCustomRegister(width, init=0):
        @m.circuit.sequential
        class Register:
            def __init__(self):
                self.value: m.Bits[width] = m.bits(init, width)

            def __call__(self, I: m.Bits[width]) -> m.Bits[width]:
                O = self.value
                self.value = I
                return O

        return Register

    CustomRegister0 = DefineCustomRegister(2, init=0)
    CustomRegister1 = DefineCustomRegister(2, init=1)

    @m.circuit.sequential
    class TestShiftRegister:
        def __init__(self):
            # [<exp>] means execute the Python expression during the first
            # stage of compilation

            # The type of a hierarchal output must have the same signature for
            # the input and output (can have a tuple for multiple inputs). This
            # reflects the ability to read and write to the variable with the
            # same meaning

            # Only supported in __init__ body for now
            self.x: CustomRegister0 = CustomRegister0()
            self.y: CustomRegister1 = CustomRegister1()

        def __call__(self, I: m.Bits[2]) -> m.Bits[2]:
            O = self.y
            self.y = self.x
            self.x = I
            return O

    compile_and_check("TestShiftRegister", TestShiftRegister, target)
    if target == "coreir-verilog":
        """
        The following sequence was used to create the verilator driver:

        tester = fault.Tester(TestShiftRegister, clock=TestShiftRegister.CLK)
        tester.circuit.I = 1
        tester.step(2)
        tester.circuit.I = 2
        tester.step(2)
        tester.circuit.O.expect(1)
        tester.circuit.I = 3
        tester.step(2)
        tester.circuit.O.expect(2)
        tester.circuit.I = 0
        tester.step(2)
        tester.circuit.O.expect(3)

        """
        _run_verilator(TestShiftRegister, directory="tests/test_syntax/build")


def test_fifo_ready_valid():
    import mantle
    @m.circuit.sequential
    class ModuleA:
        def __init__(self):
            self.count: m.UInt[4] = m.uint(0, 4)

        def __call__(self, ready_in: m.Bit) -> (m.UInt[4], m.Bit):
            data = self.count
            if ready_in:
                self.count = self.count + m.uint(1, 4)
            return data, self.count % m.uint(2, 4)

    @m.circuit.sequential
    class ModuleB:
        def __init__(self):
            self.count: m.UInt[4] = m.uint(0, 4)
            self.data: m.UInt[4] = m.uint(0, 4)

        def __call__(self, data: m.UInt[4], valid: m.Bit) -> m.Bit:
            self.data = data
            self.count = self.count + 1
            return self.count % 2

    @m.circuit.sequential
    class FIFO:
        def __init__(self):
            # self.buffer: m.Array[4, m.UInt[4]] = m.array(
            #     [m.uint(0, 4) for _ in range(4)])
            self.write_ptr: m.UInt[2] = m.uint(0, 2)
            # self.read_ptr: m.UInt[2] = m.uint(0, 2)

        def __call__(self, valid_in: m.Bit, data_in: m.UInt[4], ready_in:
                     m.Bit) -> (m.Bit, m.Bit, m.UInt[4]):
            # TODO: Implement FIFO logic
            self.write_ptr = self.write_ptr + m.uint(1, 2)
            return m.bit(1), m.bit(1), data_in

    @m.circuit.sequential
    class Top:
        def __init__(self):
            self.module_a: ModuleA = ModuleA()
            self.module_b: ModuleB = ModuleB()
            self.fifo: FIFO = FIFO()

        # TODO: Doesn't support no IO
        def __call__(self, I: m.Bit) -> m.Bit:
            ready_out = m.Wire(m.Bit)
            ready_in = m.Wire(m.Bit)
            while m.unstable(ready_out):
                valid_in, data_in = self.module_a(ready_out)
                ready_out, valid_out, data_out = self.fifo(valid_in, data_in, ready_in)
                ready_in = self.module_b(valid_out, data_out)

    print(repr(Top))
    assert False
