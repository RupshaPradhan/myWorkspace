import time
rowLkup = []
colLkup = []
backSlashCodeLkup =[]
slashCodeLkup=[]
placed = 0
score = 0
maxScore = 0
reachedChild = 0
officerCount = 0
startTime =time.time()
endTime=0

k = open("input.txt", 'r')
N = int(k.readline())
officerCount = int(k.readline())
cyclistCount = int(k.readline())
line = k.readline().strip()
my_dict = dict()
for i in range(N):
    for j in range(N):
        my_dict[str(i)+","+str(j)]=0

while line:
    if line.strip() in my_dict:
        my_dict[line.strip()] += 1
    else:
        my_dict[line.strip()] = 1
    line = k.readline()

sortedDict = sorted(my_dict.iteritems(), key=lambda (k, v): (v, k), reverse=True)


def isSafeMove(row, col,value):
    global backSlashCodeLkup
    global slashCodeLkup
    global maxScore
    global placed
    global officerCount
    global endTime
    global startTime

    if slashCodeLkup[slashCode[row][col]] == 1 or backSlashCodeLkup[backSlashCode[row][col]] == 1 or rowLkup[
        row] == 1 or colLkup[col] == 1 or maxScore >= (((officerCount-placed)*value)+score):
        return False
    endTime=time.time()
    if(endTime-startTime>175):
        f = open("output.txt", "w")
        f.write(str(maxScore))
        exit(0)
    return True


def solveUtil(i):
    global placed
    global maxScore
    global score
    global backSlashCodeLkup
    global slashCodeLkup
    global reachedChild
    global officerCount

    if placed == officerCount:
        if maxScore < score:
            maxScore = score
        reachedChild=1
        return

    for index in range(i, len(sortedDict)):
        if placed == officerCount - 2:
            reachedChild = 0
        if reachedChild == 1:
            return

        row = int(sortedDict[index][0].split(",")[0])
        col = int(sortedDict[index][0].split(",")[1])
        value = int(sortedDict[index][1])

        if isSafeMove(row, col, value):
            placed = placed + 1
            score = score + value
            rowLkup[row] = 1
            colLkup[col] = 1
            slashCodeLkup[slashCode[row][col]] = 1
            backSlashCodeLkup[backSlashCode[row][col]] = 1

            if solveUtil(index + 1):
                return True

            placed = placed - 1
            score = score - value
            rowLkup[row] = 0
            colLkup[col] = 0
            slashCodeLkup[slashCode[row][col]] = 0
            backSlashCodeLkup[backSlashCode[row][col]] = 0



def cons(N):
    w, h = N, N
    global slashCode
    global backSlashCode
    global rowLkup
    global colLkup
    global backSlashCodeLkup
    global slashCodeLkup

    slashCode = [[0 for x in range(w)] for y in range(h)]
    backSlashCode = [[0 for x in range(w)] for y in range(h)]

    for i in range(N):
        rowLkup.append(0)

    for i in range(N):
        colLkup.append(0)

    for i in range((2 * N) - 1):
        slashCodeLkup.append(0)

    for i in range((2 * N) - 1):
        backSlashCodeLkup.append(0)

    for row in range(N):
        for col in range(0, N):
            slashCode[row][col] = row + col
            backSlashCode[row][col] = row - col + (N - 1)

def solve(N):
    global maxScore
    global officerCount

    cons(N)
    f = open("output.txt", "w")
    for fl in range(0, len(sortedDict)):

        if (maxScore >= int(sortedDict[fl][1] * officerCount)):
            f.write(str(maxScore))
            return True
        if solveUtil(fl) == False:
            f.write("No solution")
            return False
        cons(N)

    f.write(str(maxScore))
    return True


solve(N)
