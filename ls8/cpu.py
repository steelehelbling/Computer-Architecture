"""CPU functionality."""

import sys
PRN = 0b01000111
HLT = 0b00000001
LDI = 0b10000010
MUL = 0b10100010
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.PC = 0
        self.reg = [0] * 8 
        self.ram = [0] * 256 
        self.running = True

    def ram_read(self, value):
        return self.ram[value]


    def ram_write(self,value,new):
        self.ram[value] = new

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        if len(sys.argv) != 2:
            print("usage: comp.py progname")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as files:
                for i in files:
                    i = i.split("#")
                    i = i[0].strip()

                    if i == "":
                        continue
                    else:
                        self.ram[address] = int(i, 2)
                        address += 1

        except FileNotFoundError:
            print(f"File not found {sys.argv[1]}")
            sys.exit(2)

        if address == 0:
            print("Program was empty!")

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111

        running = True

        while running == True:
            instruction = self.ram_read(self.PC)
            first_opperator = self.ram_read(self.PC + 1)
            second_opperator = self.ram_read(self.PC + 2)
            print(self.ram_read(self.PC))
            if instruction == HLT:
                running = False
                self.PC = self.PC + 1

            elif instruction == LDI:
                self.reg[first_opperator] = second_opperator
                self.PC = self.PC + 3 

            elif instruction == PRN:#prints first opperator 8
                # print(self.reg[first_opperator])
                self.PC = self.PC + 2

            elif instruction == MUL:# 8 * 9
                self.reg[first_opperator] = self.reg[first_opperator] * self.reg[second_opperator]
                self.PC = self.PC + 3
            else:
                print(f" input {instruction}")
                running = False

# * `LDI`: load "immediate", store a value in a register, or "set this register to
#   this value".

# * `PRN`: a pseudo-instruction that prints the numeric value stored in a
#   register.

# * `HLT`: halt the CPU and exit the emulator.