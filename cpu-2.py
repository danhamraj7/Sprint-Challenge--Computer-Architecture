"""CPU functionality."""

import sys

# # get file name from sys.argv
# file_name = sys.argv[1]
# print(file_name)


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # 256 bytes memory
        self.ram = [0] * 256
        # 8 registers
        self.reg = [0] * 8
        # program counter
        # starts with 0
        # # keeps track of where we are in memory  Stp #1
        self.pc = 0
        # reserved registers
        self.interrupt_mask = self.reg[5]
        self.interrupt_status = self.reg[6]
        self.stack_pointer = self.reg[7]

    def load(self, file_name):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        with open(file_name) as file:
            for line in file:
                split_line = line.split("#")[0].strip()

                if split_line == "":
                    continue
                else:
                    command = int(split_line, 2)
                    self.ram_write(command, address)
                    address += 1

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8 save
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

            # stp 2 add RAM functions
     # takes the given address and reads and returns the value at that address.

    def ram_read(self, mar):
        return self.ram[mar]

    # takes the given address and writes the value at that given address
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    # stp 3 implement run to:
    # keep track of the pc and read whatever address it is at in the register
    # it then takes the value of the pc address and
    # stores it in the instruction register(IR)

    def run(self):
        """Run the CPU."""
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        is_running = True

        while is_running:
            # takes the value of the pc address
            # and stores it in the instruction register(IR)
            # first instr read the ram at pc
            IR = self.ram[self.pc]
            # reset orperand_a and operand_b
            operand_a = self.ram[self.pc + 1]
            operand_b = self.ram[self.pc + 2]

        if IR == HLT:
            is_running = False
            #self.pc += 1
        elif IR == LDI:
            self.reg[operand_a] = operand_b
            #self.pc += 3
        elif IR == PRN:
            print(self.reg[operand_a])
            #self.pc += 2
        elif IR == MUL:
            a = self.reg[operand_a]
            b = self.reg[operand_b]
            self.reg[operand_a] = a * b
            #self.pc += 3

            # take the command, right-shift 6 places,
            # and add the resulting 0, 1, or 2 to the
            # one-point increment
            self.pc += 1 + (IR >> 6)
