#Emulator for a CHIP-8 system

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
    fetch = (chip8.memory[chip8.PC] << 8) | chip8.memory[chip8.PC + 1]
