#Emulator for a CHIP-8 system using Python
#This script handles the chip8 design, fetch-decode-execute loop, etc.

#Importing all required modules

import random
import pygame

pygame.mixer.init()
import numpy as np

# Code for generating a sound
sample_rate = 44100
duration = 0.2
frequency = 440 

t = np.linspace(0, duration, int(sample_rate * duration), False)
wave = 0.5 * np.sign(np.sin(2 * np.pi * frequency * t))
wave = np.array(wave * 32767, dtype=np.int16)

sound = pygame.mixer.Sound(wave)


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
        self.display = [[0] * 64 for _ in range(32)]

    
    #Function for timers
    def update_timer(self):
        if (self.delay_timer > 0):
            self.delay_timer -= 1
        
        if (self.sound_timer > 0):
            sound.play()
            self.sound_timer -=1

    #Function for loading fonts
    def load_fonts(self):
        FONT_SET = [
            0xF0, 0x90, 0x90, 0x90, 0xF0,  
            0x20, 0x60, 0x20, 0x20, 0x70,  
            0xF0, 0x10, 0xF0, 0x80, 0xF0,  
            0xF0, 0x10, 0xF0, 0x10, 0xF0,  
            0x90, 0x90, 0xF0, 0x10, 0x10,  
            0xF0, 0x80, 0xF0, 0x10, 0xF0,  
            0xF0, 0x80, 0xF0, 0x90, 0xF0,  
            0xF0, 0x10, 0x20, 0x40, 0x40,  
            0xF0, 0x90, 0xF0, 0x90, 0xF0,  
            0xF0, 0x90, 0xF0, 0x10, 0xF0, 
            0xF0, 0x90, 0xF0, 0x90, 0x90, 
            0xE0, 0x90, 0xE0, 0x90, 0xE0,  
            0xF0, 0x80, 0x80, 0x80, 0xF0,  
            0xE0, 0x90, 0x90, 0x90, 0xE0,  
            0xF0, 0x80, 0xF0, 0x80, 0xF0,  
            0xF0, 0x80, 0xF0, 0x80, 0x80   
        ]
        for i, byte in enumerate(FONT_SET):
            self.memory[i] = byte

    #Function for drawing
    def draw(self, screen):
        screen.fill((0, 0, 0))

        for y in range(32):
            for x in range(64):
                if self.display[y][x]:
                    pygame.draw.rect(screen, (255, 255, 255), 
                                     (x * 10, y * 10, 10, 10))
        
        pygame.display.flip()


    #Function to load ROM files
    def load_ROM(self, filename):
        with open(filename, 'rb') as rom:
            rom_data = rom.read()
            for i, byte in enumerate(rom_data):
                self.memory[0x200 + i] = byte




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
        chip8.PC += 2

    elif (opcode == 0x00EE):  
        chip8.PC = chip8.stack.pop()
    
    elif (opcode & 0xF000) == 0x1000:  
        nnn = opcode & 0x0FFF
        chip8.PC = nnn

    elif (opcode & 0xF000) == 0x2000:
        nnn = (opcode & 0x0FFF)
        chip8.stack.append(chip8.PC + 2)
        chip8.PC = nnn

    elif (opcode & 0xF000) == 0x3000:
        x = (opcode & 0x0F00) >> 8
        nn = (opcode & 0x00FF) 
        if chip8.V[x] == nn:
            chip8.PC += 4
        else:
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
        chip8.PC += 2


    elif (opcode & 0xF000) == 0x7000:
        x = (opcode & 0x0F00) >> 8
        nn = (opcode & 0x00FF)
        chip8.V[x] = (chip8.V[x] + nn) & 0xFF  
        chip8.PC += 2

    elif (opcode & 0xF00F) == 0x8000:
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        chip8.V[x] = chip8.V[y]
        chip8.PC += 2

    elif (opcode & 0xF00F) == 0x8001:
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        chip8.V[x] = (chip8.V[x] | chip8.V[y]) & 0xFF
        chip8.PC += 2


    elif (opcode & 0xF00F) == 0x8002:
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        chip8.V[x] = (chip8.V[x] & chip8.V[y]) & 0xFF
        chip8.PC += 2

    
    elif (opcode & 0xF00F) == 0x8003:
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        # chip8.V[x] = (chip8.V[x] | chip8.V[y]) & ~(chip8.V[x] & chip8.V[y])  -> alternate way of creating an XOR gate in Python
        chip8.V[x] = (chip8.V[x] ^ chip8.V[y]) & 0xFF
        chip8.PC += 2


    elif (opcode & 0xF00F) == 0x8004:
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4

        sum_result = (chip8.V[x] + chip8.V[y])
    
        chip8.V[x] = sum_result & 0xFF 
        chip8.V[0xF] = 1 if (sum_result & 0x100) else 0
        chip8.PC += 2
    
    elif (opcode & 0xF00F) == 0x8005:
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        
        chip8.V[0xF] = 1 if chip8.V[x] >= chip8.V[y] else 0
        chip8.V[x] = (chip8.V[x] - chip8.V[y]) & 0xFF
        
        chip8.PC += 2 

    elif (opcode & 0xF00F) == 0x8006:
        x = (opcode & 0x0F00) >> 8
        chip8.V[0xF] = chip8.V[x] & 0x01  
        chip8.V[x] >>= 1
        chip8.PC += 2

    elif (opcode & 0xF00F) == 0x8007:
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        chip8.V[x] = (chip8.V[y] - chip8.V[x]) & 0xFF

        if (chip8.V[x] <= chip8.V[y]):
            chip8.V[15] = 1
        else:
            chip8.V[15] = 0

        chip8.PC += 2 
    
    elif (opcode & 0xF00F) == 0x800E:
        x = (opcode & 0x0F00) >> 8
        chip8.V[15] = (chip8.V[x] & 0x80) >> 7
        chip8.V[x] = (chip8.V[x] << 1) & 0xFF
        chip8.PC += 2 

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
        chip8.PC += 2

    elif (opcode & 0xF000) == 0xB000:
        nnn = (opcode & 0x0FFF)
        chip8.PC = (nnn + chip8.V[0]) & 0xFFFF

    elif (opcode & 0xF000) == 0xC000:
        x = (opcode & 0x0F00) >> 8
        nn = (opcode & 0x00FF)
        chip8.V[x] = random.randint(0,255) & nn
        chip8.PC += 2
        
    elif (opcode & 0xF000) == 0xD000:
        x = chip8.V[(opcode & 0x0F00) >> 8] % 64
        y = chip8.V[(opcode & 0x00F0) >> 4] % 32
        height = opcode & 0x000F
        chip8.V[15] = 0 

        for row in range(height):
            sprite_byte = chip8.memory[chip8.I + row]
            for col in range(8):
                if (sprite_byte & (0x80 >> col)) != 0: 
                    screen_x = (x + col) % 64
                    screen_y = (y + row) % 32
                
                    if chip8.display[screen_y][screen_x] == 1: 
                        chip8.V[15] = 1

                    chip8.display[screen_y][screen_x] ^= 1

        chip8.PC += 2

    elif (opcode & 0xF0FF) == 0xE09E:
        x = (opcode & 0x0F00) >> 8
        key = chip8.V[x]
        if chip8.keypad[key]:
            chip8.PC += 4 
        else:
            chip8.PC += 2

    elif (opcode & 0xF0FF) == 0xE0A1:
        x = (opcode & 0x0F00) >> 8
        key = chip8.V[x]
        if not (chip8.keypad[key]):
            chip8.PC += 4  # Should be +4 total
        else:
            chip8.PC += 2  # Missing this line
    
    elif (opcode & 0xF0FF) == 0xF007:
        x = (opcode & 0x0F00) >> 8
        chip8.V[x] = chip8.delay_timer
        chip8.PC += 2

    elif (opcode & 0xF0FF) == 0xF00A:
        x = (opcode & 0x0F00) >> 8
        key_pressed = False  
        for i in range(16):  
            if chip8.keypad[i]:  
                chip8.V[x] = i
                chip8.PC += 2  
                key_pressed = True
                break
        if not key_pressed:
            chip8.PC += 2

    elif (opcode & 0xF0FF) == 0xF015:
        x = (opcode & 0x0F00) >> 8
        chip8.delay_timer = chip8.V[x]
        chip8.PC += 2

    elif (opcode & 0xF0FF) == 0xF018:
        x = (opcode & 0x0F00) >> 8
        chip8.sound_timer = chip8.V[x]
        chip8.PC += 2
    
    elif (opcode & 0xF0FF) == 0xF01E:
        x = (opcode & 0x0F00) >> 8
        chip8.I += chip8.V[x]
        chip8.PC += 2

    elif (opcode & 0xF0FF) == 0xF029:
        x = (opcode & 0x0F00) >> 8
        digit = chip8.V[x] & 0xF
        chip8.I = digit * 5
        chip8.PC += 2

    elif (opcode & 0xF0FF) == 0xF033:
        x = (opcode & 0x0F00) >> 8
        chip8.memory[chip8.I] = (int(chip8.V[x]) // 100)
        chip8.memory[chip8.I+1] = (int(chip8.V[x]) % 100) // 10
        chip8.memory[chip8.I+2] = (int(chip8.V[x]) % 10)
        chip8.PC += 2

    elif (opcode & 0xF0FF) == 0xF055:
        x = (opcode & 0x0F00) >> 8
        for i in range(x + 1):
            chip8.memory[chip8.I + i] = chip8.V[i]
        chip8.PC += 2  # Missing this line

    elif (opcode & 0xF0FF) == 0xF065:
        x = (opcode & 0x0F00) >> 8
        for i in range(x+1):
            chip8.V[i] = chip8.memory[chip8.I + i]
        chip8.PC += 2  


        