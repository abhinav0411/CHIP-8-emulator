#Emulator for a CHIP-8 system


#Importing all required modules

import random

#Making the class for the structure of emulator
class Chip8:
    def __init__(self):
        self.memory = [0] * 4096
        self.V = [0] * 16
        self.I = [0]
        self.PC = 0x200
        self.stack = []
        self.delay_timer = 0
        self.sound_timer = 0
        self.keypad = [0] * 16
        self.display = [[0] * 64 for i in range(32)]


#Loading ROM into memory
def load_ROM(chip8, ROM):
    chip8.memory[0x200:0x200+len(ROM)] = ROM

#Implementing Fetch, Decode, Execute   
def fetch_code(chip8):
    opcode = (chip8.memory[chip8.PC] << 8) | chip8.memory[chip8.PC + 1]
    return opcode

def decode_and_execute(chip8, opcode):
    # x = (opcode & 0x0F00) >> 8
    # y = (opcode & 0x00F0) >> 4
    # n = (opcode & 0x000F)
    # nn = (opcode & 0x00FF)
    # nnn = (opcode & 0x0FFF)
    # N = (opcode & 0xF000) >> 12

    if (opcode == 0x00E0):  
        chip8.display = [[0] * 64 for _ in range(32)]
    
    elif (opcode == 0x00EE):  
        chip8.PC = chip8.stack.pop()
    
    elif (opcode & 0xF000) == 0x1000:  
        nnn = opcode & 0x0FFF
        chip8.PC = nnn

    elif (opcode & 0xF000) == 0x2000:
        nnn = (opcode & 0x0FFF)
        chip8.stack.append(chip8.PC)
        chip8.PC = nnn

    elif (opcode & 0xF000) == 0x3000:
        x = (opcode & 0x0F00) >> 8
        nn = (opcode & 0x00FF) 
        if chip8.V[x] == nn:
            chip8.PC += 2
    elif (opcode & 0xF000) == 0x4000:
        x = (opcode & 0x0F00) >> 8
        nn = (opcode & 0x00FF) 
        if chip8.V[x] != nn:
            chip8.PC += 4
        else:
            chip8.PC += 2

    elif (opcode & 0xF000) == 0x5000:
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        if chip8.V[x] == chip8.V[y]:
            chip8.PC += 4
        else:
            chip8.PC += 2

    elif (opcode & 0xF000) == 0x6000:
        x = (opcode & 0x0F00) >> 8
        nn = (opcode & 0x00FF) 
        chip8.V[x] = nn

    elif (opcode & 0xF000) == 0x7000:
        x = (opcode & 0x0F00) >> 8
        nn = (opcode & 0x00FF)
        chip8.V[x] += nn

    elif (opcode & 0xF000) == 0x8000:
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        chip8.V[x] = chip8.V[y]
    elif (opcode & 0xF00F) == 0x8001:
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        chip8.V[x] = chip8.V[x] | chip8.V[y]

    elif (opcode & 0xF00F) == 0x8002:
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        chip8.V[x] = chip8.V[x] & chip8.V[y]
    
    elif (opcode & 0xF00F) == 0x8003:
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        # chip8.V[x] = (chip8.V[x] | chip8.V[y]) & ~(chip8.V[x] & chip8.V[y])  -> alternate way of creating an XOR gate in Python
        chip8.V[x] = chip8.V[x] ^ chip8.V[y]

    elif (opcode & 0xF00F) == 0x8004:
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4

        if (chip8.V[x] + chip8.V[y] > 0xFF):
            chip8.V[15] = 1
        else:
            chip8.V[15] = 0

        chip8.V[x] = ((chip8.V[x] + chip8.V[y]) & 0xFF)
    
    elif (opcode & 0xF00F) == 0x8005:
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4

        if (chip8.V[x] >= chip8.V[y]):
            chip8.V[15] = 1
        else:
            chip8.V[15] = 0
        
        chip8.V[x] = (chip8.V[x] - chip8.V[y]) & 0xFF

    elif (opcode & 0xF00F) == 0x8006:
        x = (opcode & 0x0F00) >> 8
        chip8.V[15] = chip8.V[x] & 0x01
        chip8.V[x] = chip8.V[x] >> 1

    elif (opcode & 0xF00F) == 0x8007:
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4

        if (chip8.V[x] <= chip8.V[y]):
            chip8.V[15] = 1
        else:
            chip8.V[15] = 0

        chip8.V[x] = (chip8.V[y] - chip8.V[x]) & 0xFF
    
    elif (opcode & 0xF00F) == 0x800E:
        x = (opcode & 0x0F00) >> 8
        chip8.V[15] = (chip8.V[x] & 0x80) >> 7
        chip8.V[x] = (chip8.V[x] << 1) & 0xFF

    elif (opcode & 0xF00F) == 0x9000:
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4

        if (chip8.V[x] != chip8.V[y]):
            chip8.PC += 4
        else:
            chip8.PC += 2

    elif (opcode & 0xF000) == 0xA000:
        nnn = (opcode & 0x0FFF)
        chip8.I = nnn

    elif (opcode & 0xF000) == 0xB000:
        nnn = (opcode & 0x0FFF)
        chip8.PC = (nnn + chip8.V[0]) & 0xFFFF

    elif (opcode & 0xF000) == 0xC000:
        x = (opcode & 0x0F00) >> 8
        nn = (opcode & 0x00FF)
        chip8.V[x] = random.randint(0,255) & nn
