#Tests for filtering frames. For dev work only!

f = open("original.txt",'r')
f_out = open("filtered.txt",'w')

f_lines = f.read().split("\n")

for i in range(len(f_lines)):
    line = f_lines[i]
    if len(line) >= 100:
        f_out.write(line[20:])

f_out.close()
