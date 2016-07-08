
from random import randint

ROBOT='0'
HOLE='*'
FREE_POS='.'
GAMMA = 0.9
ALPHA = 0.1
NO_LINK = -999 #if there is no link between the nodes, the value is -999
TRAINING_SESSIONS = 50

''' Defines initial state/matrices of the problem
'''
def initProblem():
    #creates matrix of environment state
    global mainMatrix
    mainMatrix=[[FREE_POS for y in range(12)] for x in range(4)]
    
    for k in range(10):
        if k>=1 and k<=10:
            mainMatrix[3][k]=HOLE

    mainMatrix[3][0]=ROBOT
    
    #loads reward table
    global rewardMatrix
    with open('reward.txt') as f:
        rewardMatrix = []
        for line in f:
            line = line.split() # to deal with blank 
            if line:            # lines (ie skip them)
                line = [int(i) for i in line]
                rewardMatrix.append(line)
    
    #creates knowledge matrix
    global knowledgeMatrix
    knowledgeMatrix=[[0 for y in range(4)] for x in range(48)]

'''Prints the robot and the possible states 
'''
def printEnvironment(table):
    print()
    for i in range(len(table)):
        for j in range(len(table[i])): 
            print (str(table[i][j]) + "  ", end="")
        print(end="\n")
    print("________________________________________________")
        
def main():
    global mainMatrix
    global rewardMatrix
    global knowledgeMatrix
    initProblem()
    
    trainingSessions = 0
    while(trainingSessions < TRAINING_SESSIONS):
        row = 3
        col = 0
        newRow = 3
        newCol = 0
        trainingSessions +=1
        while(row!=3 or col!=11):
            randAction = randint(0,3) #up 0, down 1, left 2, right 3
            
            if randAction == 0:
                newRow-=1
            elif randAction == 1:
                newRow += 1
            elif randAction == 2:
                newCol -= 1
            else: newCol += 1
            
            #checks if the new position is inside the box
            if(newRow < 4 and newRow >=0 and newCol >= 0 and newCol < 12):
            
                #REDRAWING THE MATRIX
                #mainMatrix[newRow][newCol]="0"
                #printEnvironment(mainMatrix)
                #mainMatrix[newRow][newCol]="."
                
                #getting the Q for every action at the next state
                stateUp = knowledgeMatrix[(3-newRow)*12+newCol][0]
                stateDown = knowledgeMatrix[(3-newRow)*12+newCol][1]
                stateLeft = knowledgeMatrix[(3-newRow)*12+newCol][2]
                stateRight = knowledgeMatrix[(3-newRow)*12+newCol][3]
                
                #getting the max value of all the possible actions for S'
                maxQ = max(stateUp,stateDown,stateLeft, stateRight)
                
                #calculating the Q
                knowledgeMatrix[(3-row)*12+col][randAction] += ALPHA * ((rewardMatrix[newRow][newCol]) + GAMMA 
                                                                     * maxQ - knowledgeMatrix[(3-row)*12+col][randAction])
                
                knowledgeMatrix[(3-row)*12+col][randAction] = int((knowledgeMatrix[(3-row)*12+col][randAction] * 100) + 0.5) / 100.0 #fixing round problems
                
                if(newRow == 3 and newCol>=1 and newCol<=10): #it's a hole
                    row = 3
                    col = 0
                    newRow = 3
                    newCol = 0
                else: #not a hole
                    row = newRow
                    col = newCol
                
            else: #out of bounds
                newRow = row
                newCol = col

    print("MATRIZ DE CONHECIMENTO: \n")
    printEnvironment(knowledgeMatrix)
    print("\n\n")
    
    #Walks greedy through the knowledge matrix in order to generate the result
    print("SEQUENCIA DE PASSOS: \n\n")
    row = 3
    col = 0
    while(row!=3 or col!=11):
        maxN = 0
        for i in range(4):
            if(knowledgeMatrix[(3-row)*12+col][i] > knowledgeMatrix[(3-row)*12+col][maxN] and knowledgeMatrix[(3-row)*12+col][i] != 0):
                maxN = i
        
        if maxN == 0:
            row-=1
        elif maxN == 1:
            row += 1
        elif maxN == 2:
            col -= 1
        else: col += 1
        
        mainMatrix[row][col]="0"
        printEnvironment(mainMatrix)
        #mainMatrix[row][col]="."
            
    
if __name__ == "__main__":
    main()