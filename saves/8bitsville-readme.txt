8bitsville-readme

This is a slightly weird computer. It only has one instruction, MOVE. So, it has some tricky registers instead - registers 0-15 are special. You can write into them as normal, but when you read from them, you get something different!


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
13: 13 OR 14
14: 13 == 14 (1 if true, 0 if false)
15: 2s complimeent

The code saved in 8bitsville-primecalc.timber:

0x10	0x37	0x02	START	move (const 2) 2	Just hacky display 2. :)
0x11	0x09	0x34		move (const 1) (candidate)	set candidate = 1
0x12	0x34	0x03	GENERATE	move (candidate) (adder)	Add 2 to candidate
0x13	0x37	0x04		move (const 2) (adder)	
0x14	0x04	0x34		move (adder) (candidate)	
0x15	0x09	0x35		move (const 1) (divisor)	set divisor = 1
0x16	0x35	0x03	CONTINUE	move (divisor) (adder)	add 2 to divisor
0x17	0x37	0x04		move (const 2) (adder)	
0x18	0x04	0x35		move (adder) (divisor)	
0x19	0x08	0x36		move (const 0) (test_val)	Reset test_val
0x1A	0x35	0x0D		move (divisor) (equaller)	check if divisor == candidate
0x1B	0x34	0x0E		move (candidate) (equaller)	
0x1C	0x3F	0x09		move (addr:win) 9	If so, we're out of divisors. Win!
0x1D	0x3D	0x08		move (addr:innerloop) 8	Otherwise, continue to the inner loop
0x1E	0x0E	0x0A		move (equaller) 10	
0x1F	0x0A	0x01		move (tester) 1	
0x20	0x36	0x03	INNERLOOP	move (test val) (adder)	add divisor to test_val
0x21	0x35	0x04		move (divisor) (adder)	
0x22	0x04	0x36		move (adder) (test val)	
0x23	0x36	0x0D		move (test_val) (equaller)	Check if test val == candidate (which is still in equaller from 0x1b)
0x24	0x3B	0x09		move (addr: generate) 9	if so, we've collided and aren't prime. Abandon this candidate and generate the next
0x25	0x3E	0x08		move(addr: didwepass) 8	otherwise, we haven't collided, make sure we haven't passed our target
0x26	0x0E	0x0A		move (equaller) 10	
0x27	0x0A	0x01		move (tester) 1	
0x28	0x36	0x0F	DIDWEPASS	move (test_val) (2s_complimenter)	Generate the 2s compliment of test_val
0x29	0x34	0x03		move (candidate) (adder)	Add -test_val to candidate
0x2A	0x0F	0x04		move (2s_complimenter) (adder)	
0x2B	0x39	0x0B		move (const 0x8000) (ander)	Bit-mask the result with 0x8000
0x2C	0x04	0x0C		move (adder) (ander)	
0x2D	0x3D	0x08		move (addr: innerloop) 8	If it's 0, the subtraction result is still positive. We haven't passed the candidate yet.
0x2E	0x3C	0x09		move (addr: continue) 9	otherwise, we've passed the candidate, continue to next divisor
0x2F	0x0C	0x0A		move (ander) 10	
0x30	0x0A	0x01		move (tester) 1	
0x31	0x34	0x02	WIN	move (candidate) 2	Display the candidate, now a proven prime
0x32	0x3B	0x01		move (addr: generate) 1	and hard jump to generating the next prime
0x33					
0x34			MEMS	candidate	
0x35				divisor	
0x36				test_val	
0x37	0x02		CONSTS	0x02	
0x38	0x03			0x03	
0x39	0x00	0x80		0x8000	
0x3A					
0x3B	0x12		ADDRESSES	Generate	
0x3C	0x16			Continue	
0x3D	0x20			Innerloop	
0x3E	0x28			Didwepass	
0x3F	0x31			Win	