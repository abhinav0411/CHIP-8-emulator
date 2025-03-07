

Computer Architecture is the study of the different components in a computer like the CPU, Memory(RAM), Program Counter, etc.

For a [[CHIP-8]] system we will need to know about the following components-
- [ ] Memory(RAM)
- [ ] Registers
- [ ] Program Counter
- [ ] Stack
- [ ] Input
- [ ] Display
- [ ] Timer


##### Memory(RAM)
Memory is the hardware that stores the data and operations to be used by the CPU to execute it's functions.

Now we have different types of Memory in a computer like RAM, Registers, Cache and Storage(HDD/SSD). Here we will only discuss about RAM and Registers as a CHIP-8 system does not have other types of memory.

RAM(Random Access Memory) is used to store temporary data which is used while the program is active.
Registers are small storage locations that are faster than RAM inside the CPU. They are faster than RAM because they are connected directly to the CPU.


##### Program Counter
Program counter keeps the address of the next process to be executed.
==NOTE - PC is incremented by 2 in a CHIP-8 system as each instruction is 2 bytes long==


##### Stack
Stack is used to store the return addresses  when calling a function.
Return Addresses is the memory location a program need to go to after executing a function.


##### Input
CHIP-8 follows a hexadecimal(0-9-A-F) keypad. To implement a CHIP-8 system we need to remap our keyboard to hexadecimal keys.



##### Display
Here in this project we will use Python's pygame library to build the display for the CHIP-8 system. CHIP-8 has a 64x32 monochrome display.


##### Timer
Timers in general are used to handle events like synchronizing events or process scheduling without blocking the CPU. In CHIP-8 because it does not have any interrupts timers are used to handle animation speed, physics updates, etc.

