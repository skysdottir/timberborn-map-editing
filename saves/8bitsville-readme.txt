8bitsville-readme

This is a slightly weird computer. It only has one instruction, MOVE. So, it has some tricky registers instead - registers 0-12 are special. You can write into them as normal, but when you read from them, you get something different!

Currently, the computer works in two phases: in phase zero it moves the register at the program counter to address 0, the exec register. Then in phase one it execs the instruction, and updates the PC. I'm working on getting execute-in-place working, which should let the computer run much faster- theoretically, up to one cycle per tick.

Special registers:
0: exec (don't read or write me!)
1: pc
2: IO
3: add (outputs carry bit)
4: add (outputs sum)
5: not
6: rshift
7: lshift
8: outputs 0 (input for branch)
9: outputs 1 (input for branch)
10: outputs 8 if 0, 9 if other
11: 11 xor 12
12: 11 and 12

General registers, with current fibonacci-sequence program:
13: NOP
14: move 8 3
15: move 9 4
16: move 29 9
17: NOP
18: move 4 2
19: move 4 3
20: move 3 10
21: move 31 8
22: move 10 1
23: move 4 2
24: move 4 4
25: move 3 10
26: move 30 8
27: move 10 1
28: NOP
29: const 14
30: const 18
31: const 23

And a bit more human-readable:

startup:

move "0" to 3 (reset)
move "1" to 4
move addr(reset) -> 9

The loop:

move 4 to disp (start of loop)
move 4 to 3
move 3 to 10
move addr(continue) -> 8
goto 10 [reset or continue]
move 4 to disp (continue)
move 4 to 4
move 3 to 10
move addr(start of loop) -> 8
goto 10 [reset or start of loop]

consts:

reset
start of loop
continue