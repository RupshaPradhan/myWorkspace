import copy
import time
import math
import numpy as np




reward = []
currentUtil = []
prevUtil = []
policy = []
carStartCoord = []
carStopCoord =[]
obsCoord=[]
grid_s = 0
flag = 0
car_count=0
obs_count =0
startTime = time.time()

def start():
        global currentUtil
        global carStartCoord
        global grid_s
        global obsCoord
        global carStopCoord
        global car_count
        global obs_count


        fp = open("input.txt", 'r')
       # print "Start time "+str(startTime)
        grid_s = int(fp.readline())

        car_count = int(fp.readline().strip())
        obs_count = int(fp.readline().strip())


        for i in range (0,obs_count):
            obsCoord.append(fp.readline().strip())


        for i in range (0,car_count):
            carStartCoord.append(fp.readline().strip())

        for i in range (0,car_count):
            carStopCoord.append(fp.readline().strip())




def turn_left(dir):
  if(dir == 'E'):
      return 'N'
  elif(dir == 'W'):
      return 'S'
  elif(dir == 'N'):
      return 'W'
  else:
      return 'E'

def turn_right(dir):
  if(dir == 'E'):
     return 'S'
  elif(dir == 'W'):
     return 'N'
  elif(dir == 'N'):
     return 'E'
  else:
     return 'W'

def calcValue(car):
    global moneyEarned
    global carStartCoord
    global carStopCoord
    global reward

    
    moneyEarned = 0
    meanTotal = 0
    for j in range(10):
         moneyEarned = 0

         pos = carStartCoord[car]
         np.random.seed(j)
         swerve = np.random.random_sample(1000000)
         k = 0
         while pos != carStopCoord[car]:
             move = policy[int(pos.split(",")[1])][int(pos.split(",")[0])]

             if swerve[k] > 0.7:
                 if swerve[k] > 0.8:
                     if swerve[k] > 0.9:
                         move = turn_left(turn_left(move))
                         pos = moveToPos(move, pos)
                         moneyEarned += reward[int(pos.split(",")[1])][int(pos.split(",")[0])]
                     else:
                         move = turn_right(move)
                         pos = moveToPos(move, pos)
                         moneyEarned += reward[int(pos.split(",")[1])][int(pos.split(",")[0])]
                 else:
                     move = turn_left(move)
                     pos = moveToPos(move, pos)
                     moneyEarned += reward[int(pos.split(",")[1])][int(pos.split(",")[0])]
             else:
                 pos = moveToPos(move, pos)
                 moneyEarned += reward[int(pos.split(",")[1])][int(pos.split(",")[0])]
             k += 1

         meanTotal +=moneyEarned

    #print str(int(math.floor(meanTotal/10.0)))
    return (str(int(math.floor(meanTotal/10.0))))


def moveToPos(move, pos):
     global grid_s

     lc=pos.split(",")

     if(move == 'N'):
         if(int(lc[1])-1>=0):
            newPos = str(int(lc[0]))+","+str(int(lc[1])-1)
         else:
             newPos = str(int(lc[0]))+","+str(int(lc[1]))
         return newPos

     elif(move == 'S'):
         if (int(lc[1]) + 1 < grid_s):
             newPos = str(int(lc[0])) + "," + str(int(lc[1]) + 1)
         else:
             newPos = str(int(lc[0])) + "," + str(int(lc[1]))
         return newPos

     elif(move == 'E'):
         if(int(lc[0])+1<grid_s):
            newPos = str(int(lc[0])+1)+","+str(int(lc[1]))
         else:
            newPos = str(int(lc[0])) + "," + str(int(lc[1]))
         return newPos

     elif(move == 'W'):
         if (int(lc[0])-1>=0):
            newPos = str(int(lc[0])-1)+","+str(int(lc[1]))
         else:
            newPos=str(int(lc[0])) + "," + str(int(lc[1]))
         return newPos
7

def calculateUtil():
    global currentUtil
    global prevUtil
    global grid_s
    global policy
    global flag
    global car_count
    global reward
    global obsCoord
    global obs_count

    op = open("output.txt", "a")
    for m in range(0,car_count):
        policy = [['' for x in range(grid_s)] for y in range(grid_s)]
        reward = [[-1 for x in range(grid_s)] for y in range(grid_s)]

        for i in range(0, obs_count):
            location = obsCoord[i].split(",")
            reward[int(location[1])][int(location[0])] += -100

        reward[int((carStopCoord[m].split(","))[1])][int((carStopCoord[m].split(","))[0])] += 100

        currentUtil = copy.deepcopy(reward)


        while(flag==0):
            prevUtil=copy.deepcopy(currentUtil)

            for i in range(0,grid_s):
                for j in range(0,grid_s):
                    if reward[i][j] == 99:
                        currentUtil[i][j]=99
                        continue

                    
                    left=""
                    right=""
                    up=""
                    down=""
                    downUtil=0
                    upUtil=0
                    leftUtil=0
                    rightUtil=0

                    if (j-1)>=0:
                        left+=str(i)+","+str(j-1)
                    else:
                        left+=str(i)+","+str(j)

                    if (j+1)<grid_s:
                        right+=str(i)+","+str(j+1)
                    else:
                        right+=str(i)+","+str(j)

                    if (i-1)>=0:
                        up+=str(i-1)+","+str(j)
                    else:
                        up+=str(i)+","+str(j)

                    if (i+1)<grid_s:
                        down+=str(i+1)+","+str(j)
                    else:
                        down+=str(i)+","+str(j)

                    if left != "":
                        leftUtil=0.7*prevUtil[int(left.split(",")[0])][int(left.split(",")[1])]+0.1*(prevUtil[int(right.split(",")[0])][int(right.split(",")[1])]+prevUtil[int(up.split(",")[0])][int(up.split(",")[1])]+prevUtil[int(down.split(",")[0])][int(down.split(",")[1])])
                    if right != "":
                        rightUtil=0.7*prevUtil[int(right.split(",")[0])][int(right.split(",")[1])]+0.1*(prevUtil[int(left.split(",")[0])][int(left.split(",")[1])]+prevUtil[int(up.split(",")[0])][int(up.split(",")[1])]+prevUtil[int(down.split(",")[0])][int(down.split(",")[1])])
                    if up != "":
                        upUtil=0.7*prevUtil[int(up.split(",")[0])][int(up.split(",")[1])]+0.1*(prevUtil[int(right.split(",")[0])][int(right.split(",")[1])]+prevUtil[int(left.split(",")[0])][int(left.split(",")[1])]+prevUtil[int(down.split(",")[0])][int(down.split(",")[1])])
                    if down != "":
                        downUtil=0.7*prevUtil[int(down.split(",")[0])][int(down.split(",")[1])]+0.1*(prevUtil[int(right.split(",")[0])][int(right.split(",")[1])]+prevUtil[int(up.split(",")[0])][int(up.split(",")[1])]+prevUtil[int(left.split(",")[0])][int(left.split(",")[1])])

                    x=max(leftUtil,rightUtil,upUtil,downUtil)

                    currentUtil[i][j]=reward[i][j]+0.9*x

                    
                    if x ==upUtil:
                        policy[i][j]='N'
                    elif x ==downUtil:
                        policy[i][j]='S'
                    elif x ==rightUtil:
                        policy[i][j]='E'
                    elif x ==leftUtil:
                        policy[i][j]='W'


            for i in range(0,grid_s):
                for j in range(0,grid_s):
                    if abs(currentUtil[i][j]-prevUtil[i][j])>(0.1*(1-0.9)/0.5):
                        flag=1
                        break

            if flag == 0 :
                break
            else:
                flag = 0

        op.write(calcValue(m))
                






if __name__ == "__main__":
        start()
        calculateUtil()
        #t_passed = time.time() - startTime
        #print "Completed writing in "+str(t_passed)

            


