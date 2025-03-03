
A CHIP-8 system is a simple interpreter designed in the 1970s to run small games on early computers. It has a very simple architecture and is great for learning emulation or computer architecture.


##### How does it work (steps involved)
- Load program into memory
- Fetch, Decode, Execute
- Handle Input and Graphics
- Decrement Timers



##### CHIP-8 Specifications

1. **Memory**- CHIP-8 is capable of having 4kb(4096 bytes) of memory. The first 512 bytes are where the original interpreter was located and therefore should not be used. 
2. **Registers**- It has 16 general purpose 8-bit registers. It also has a 16 bit register used to store memory address called I. VF register should not be used as it generally contains the information of carry, borrow. It is called as a flag register(register which is used to store results of certain operations like carry, borrow or overflow conditions). It also has a Program Counter which is 16 bit which is used to store the currently executing address. The stack is an array of 16 16 bit values used to store the address that the interpreter should return to after executing a program.
3. **Keyboard**- CHIP-8 uses 16 key hexadecimal keypad. This can be implemented by binding some keys on our keyboard to match with the hexadecimal keys.
4. **Display**- It uses a 64x32 monochrome display (monochrome means it has only 2 colors i.e. white and black). Chip-8 draws graphics using sprites on the screen.
5. **Timers**- It has 2 timers - Delay timer and Sound timer. Delay timer does nothing mor than subtract 1 at a rate of 60hz. When it reaches 0 it deactivates. Sound timer is also similar except it will sound a buzzer as long as it's value is greater than 0. CHIP-8 has only one tone.