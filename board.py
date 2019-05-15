import numpy as np
import characters as char

boardRows=15
boardCols=15

def createBoard():
	return np.array(np.random.randint(1,6,(boardRows,boardCols)))

def checkClick(posRow,posCol):
	clickVal=board[posRow][posCol]
	if clickVal>=2:
		#print ('clicked',clickVal,"at ",posRow,posCol)
		return clickVal
	else:
		#print ("unclickable",clickVal)
		return None

def checkEdges(matchBoard,boolBoard):
	for row in range(0,len(matchBoard)):
		curRow=matchBoard[row]
		#ignore rows that are all 0s
		if np.count_nonzero(curRow):
			for col in range(0,len(curRow)):
				#ignore 0s in the row
				if curRow[col]==1:
					#Check for adjacent matches and copy matches then delete from boolBoard
					if row>0:
						if boolBoard[row-1][col]==1:
							#print "match above"
							matchBoard[row-1][col]=1
							boolBoard[row-1][col]=0
						else:
							pass
					if row<boardRows-1:
						if boolBoard[row+1][col]==1:
							matchBoard[row+1][col]=1
							boolBoard[row+1][col]=0
						else:
							pass
					if col>0:
						if boolBoard[row][col-1]==1:
							matchBoard[row][col-1]=1
							boolBoard[row][col-1]=0
						else:
							pass
					if col<boardCols-1:
						if boolBoard[row][col+1]==1:
							matchBoard[row][col+1]=1
							boolBoard[row][col+1]=0
						else:
							pass
					matchBoard[row][col]=2
	if 1 in matchBoard:
		return checkEdges(matchBoard,boolBoard)
	else:
		return matchBoard
		pass

def createMatchBoard(clickVal,Row,Col):
	boolBoard=np.where(board==clickVal,1,0)
	matchBoard=np.zeros((boardRows,boardCols), dtype=np.int)
	matchBoard[Row][Col]=1
	matchBoard=checkEdges(matchBoard,boolBoard)
	return matchBoard

def updateBoard(matchBoard):
	for row in range(0,len(matchBoard)):
		curRow=matchBoard[row]
		tempRow=[]
		if 2 in curRow:
			matches=np.where(curRow==2)[0]
			for n in range(0,len(curRow)):
				if n not in matches:
					tempRow.append(board[row][n])
			for n in range(0,len(matches)):
				tempRow.append(0)
		else:
			tempRow=board[row]
		board[row]=np.array(tempRow)
	#print (board,'\n\n')

def handleClick(row,column):
	clickVal=checkClick(row,column)
	if clickVal:
		manaStart=np.count_nonzero(board)
		matchBoard=createMatchBoard(clickVal,row,column)
		updateBoard(matchBoard)
		manaCount=manaStart-np.count_nonzero(board)
		#print (clickVal,manaCount)
		char.playerChars[clickVal-2].manaGain(manaCount)
		#print (board,"\n\n")

def wildfire():
	#select 3 unique non-empty cols
	wfCols=wildfireColSelect([])
	#destory cols
	manaCounts={2:0,3:0,4:0,5:0}
	for colIndex in wfCols:
		#count values first
		unique, counts = np.unique(board[colIndex], return_counts=True)
		colManaCount=dict(zip(unique, counts))
		for n in range(2,6):
			try:
				manaCounts[n]+=colManaCount[n]
			except KeyError:
				pass
		board[colIndex]=np.zeros((boardRows,), dtype=int)
	return manaCounts

def wildfireColSelect(cols):
	while len(cols)<5:
		colIndex=np.random.randint(0,boardCols)
		if colIndex not in cols and board[colIndex].any():
			cols.append(colIndex)
		else:
			return wildfireColSelect(cols)
	return cols

board=createBoard()