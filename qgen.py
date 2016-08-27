import argparse, random

# initialize and parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("filename")
parser.add_argument("n")
parser.add_argument("--star_only", action='store_true')
args = parser.parse_args()
filename = args.filename
n = int(args.n)

allq = []

# read line by line and add questions to the big list
print filename
f = open(filename)

for line in f:
    # ignore small lines
    wonl = line.strip()
    if len(wonl) < 2:
        continue
    if wonl[0]=="*":
        print "Yeay"
        allq.append(wonl)

f.close()
if len(allq) < n:
    raise RuntimeError("The number of questions must be less than " + str(len(allq)))
print allq
qlist = []
for i in xrange(n):
	random.shuffle(allq)
	qlist.append(allq.pop())

wf = open(filename+"-qgen.txt","w")
num = 1
for q in qlist:
    wf.write(str(num)+ ". " +q)
    num = num+1
    for i in range(6):
        wf.write("\n")
wf.close()
