from copy import deepcopy

BLANK = 0
WHITE = 1
BLACK = 2

def printGrid(grid):
 for i in grid:
   print(i)
 print("")
 
 
class Grid(object):
 running = 0
 solvable = 0
 length = 0
 spaces = 0
 whites = 0
 blacks = 0
 tiles = []
 
 """Initialisation"""
 def __init__(self, length):
  self.length = length
  self.running = 1
  
  #Puzzle is only solvable if given length is > 0 and even
  self.solvable = length > 0 and length % 2 == 0

  #Create grid of given length
  for i in range(length):
   self.tiles.append([])
   for j in range(length):
    self.tiles[i].append(BLANK)

######################PUBLIC METHODS#######################

 """Main Run Loop"""
 def run(self):
  print("start:")
  printGrid(self.tiles)
  
  #Size of grid is not valid
  if (not self.solvable): return

  #No colour added initially, set puzzle to end with default values
  self.spaces = self.countSpaces()
  if self.spaces == self.length*self.length:
   self.setAllDefaultValues()
   return

  #Start the recursive solver
  self.solve()
    
 """The recursion function used to solve the puzzle"""
 def solve(self):
  #Puzzle has been solved
  if not self.running: return
   
  #There is a significant event in the loop, go back.
  if self.gridCheck(): return
  
  self.spaces = self.countSpaces()
  
  #Apply method 1 and 2
  self.method1()
  self.method2()
  
  newSpaces = self.countSpaces()
  
  #No change has been made after applying method 1 and 2
  if self.spaces == newSpaces:
   #Save the state of the grid
   state = deepcopy(self.tiles)

   #Try a white tile and attempt to solve from there
   self.method3(WHITE)
   self.solve()
	
   #Puzzle has been solved
   if not self.running:
    return
	
   #Revert back for a chance to find another path
   self.solvable = 1 
   self.spaces = newSpaces
   self.copyState(state)

   #Try a black tile and attempt to solve from there
   self.method3(BLACK)
   self.solve()
	
   #Neither worked, must go back to an earlier state
   return
  
  #Method 1 or 2 made a change to the grid
  self.spaces = newSpaces
  self.solve()
  return
  

#----------------------------------------------------------#

 """Finalise the puzzle with the result."""
 def getResults(self):
  print("Result:")
  printGrid(self.tiles)
  
  #Puzzle was not solved - print unsolvable
  if not self.solvable or self.countSpaces() > 0:
   print("UNSOLVABLE")
   return
	
  #Puzzle was solved - print the indexed of the white coloured tiles*/
  pos = 1;
  for i in self.tiles:
   for j in i:
    if j == WHITE:
     print(pos),
    pos += 1

	
#----------------------------------------------------------#

 """User input - Adding the colours to the grid"""
 def addWhite(self, pos):
  self.checkPosition(pos-1, WHITE);

 def addBlack(self, pos):
  self.checkPosition(pos-1, BLACK);
  
  
######################PRIVATE METHODS#######################
  
 def setFinished(self):
  self.running = 0
  return 1

 def setSolvable(self, flag):
  self.solvable = flag
  return 1
  
#----------------------------------------------------------#

 """Validate the 'user' number input"""
 def checkPosition(self, pos, colour):
  #Break puzzle if position is out of bounds
  if pos < 0 or pos >= self.length*self.length:
   self.setSolvable(0)
   return

  #Break puzzle if position is taken by the other colour
  i = pos / self.length
  j = pos % self.length
  currentColour = self.tiles[i][j]
  if currentColour != BLANK and currentColour != colour:
   self.setSolvable(0)
   return

  self.tiles[i][j] = colour
  

#----------------------------------------------------------#

 """Check grid status - returns True to stop program, False otherwise."""
 def gridCheck(self):
  #Check every row for a match of 3 coloured tiles and for
  #too much coloured tiles
  for i in range(self.length):
   for j in range(self.length-1):
    if j == 0: continue
    if self.check3inLine(self.tiles[i][j-1], self.tiles[i][j], self.tiles[i][j+1]):
     return self.setSolvable(0)

   #Check every row for too much coloured tiles
   self.countRowColours(i);
   if self.checkColourLimit(): return 1

  #Check every column for a match of 3 coloured tiles
  for j in range(self.length):
   for i in range(self.length-1):
    if i == 0: continue
    if self.check3inLine(self.tiles[i-1][j], self.tiles[i][j], self.tiles[i+1][j]):
     return self.setSolvable(0)
    
   #Check every column for too much coloured tiles
   self.countColumnColours(j);
   if self.checkColourLimit(): return 1

  #Grid full now - no problems encountered so far, puzzle solved!
  if self.spaces == 0:
   return self.setFinished()
    
  return 0

  
#----------------------------------------------------------#

 """Check whether 3 coloured tiles in line match or not"""
 def check3inLine(self, a, b, c):
  row = (a==b) and (b==c)
  return row and (a==WHITE or a==BLACK)


 """Check if one colour count is over the limit of the grid"""
 def checkColourLimit(self):
  limit = self.length/2
  if self.whites > limit or self.blacks > limit:
   return self.setSolvable(0)
  return 0
 
 
 """Count the colours in the indexed row"""
 def countRowColours(self, index):
  self.whites = 0
  self.blacks = 0
  for i in range(self.length):
   colour = self.tiles[index][i]
   if colour == WHITE:
    self.whites += 1
   elif colour == BLACK:
    self.blacks += 1


 """Count the colours in the indexed column"""
 def countColumnColours(self, index):
  self.whites = 0
  self.blacks = 0
  for i in range(self.length):
   colour = self.tiles[i][index]
   if colour == WHITE:
    self.whites += 1
   elif colour == BLACK:
    self.blacks += 1


 """Retrieve the opposite colour to the given colour"""
 def getOppositeColour(self, colour):
  if colour == WHITE:
   return BLACK
  return WHITE


 """Count the remaining blank spaces left in the grid"""
 def countSpaces(self):
  count = 0
  for i in self.tiles:
   for j in i:
    if j == BLANK:
     count += 1
  return count

  
 """Return the grid back to the given state"""
 def copyState(self, state):
  for i in range(self.length):
   for j in range(self.length):
    self.tiles[i][j] = state[i][j]
	

#----------------------------------------------------------#

 """Grid is empty - quick fill, 1's and 0's alternating"""
 def setAllDefaultValues(self):
  colour1 = 1
  for i in range(self.length):
   for j in range(self.length):
    if colour1:
     self.tiles[i][j] = WHITE
    else:
     self.tiles[i][j] = BLACK
    colour1 = not colour1 #Alternate colour
   colour1 = not colour1 #Alternate colour for next row


#----------------------------------------------------------#

 """Method 1 - Fills in blank tiles using pattern matching"""
 def method1(self):
  #Horizontal
  for i in range(self.length):
   for j in range(self.length-1):
    if j == 0: continue
    self.patternRowMatch(i, j)
  
  #Vertical
  for j in range(self.length):
   for i in range(self.length-1):
    if i == 0: continue
    self.patternColumnMatch(i, j)

    
 def patternRowMatch(self, i, j):
  tile_prev = self.tiles[i][j-1]
  tile = self.tiles[i][j]
  tile_next = self.tiles[i][j+1]
  
  if tile != BLANK:
   #Previous and current tile are the same and next tile blank
   #- the next tile must be the opposite colour
   if tile_prev == tile and tile_next == BLANK:
    self.tiles[i][j+1] = self.getOppositeColour(tile);
    #Current and next tile...
   elif tile == tile_next and tile_prev == BLANK:
    self.tiles[i][j-1] = self.getOppositeColour(tile);
   return;

  #Current tile is blank and tiles on both sides have the same colour
  #- current tile must be the opposite colour*/
  if tile_prev == tile_next and tile_prev != BLANK:
   self.tiles[i][j] = self.getOppositeColour(tile_prev);


 def patternColumnMatch(self, i, j):
  tile_prev = self.tiles[i-1][j]
  tile = self.tiles[i][j]
  tile_next = self.tiles[i+1][j]
  
  if not tile == BLANK:
   if tile_prev == tile and tile_next == BLANK:
    self.tiles[i+1][j] = self.getOppositeColour(tile);
   elif tile == tile_next and tile_prev == BLANK:
    self.tiles[i-1][j] = self.getOppositeColour(tile);
   return;

  if tile_prev == tile_next and tile_prev != BLANK:
   self.tiles[i][j] = self.getOppositeColour(tile_prev);

   
#----------------------------------------------------------#
   
 """Method 2 - Fills in the rest of the row/column blanks if 
			   coloured tiles on one side is all used up"""
 def method2(self):
  #Horizontal
  for i in range(self.length):
   self.countRowColours(i)
   self.fillRowPattern(i)
   
  #Vertical
  for j in range(self.length):
   self.countColumnColours(j)
   self.fillColumnPattern(j)


 def fillRowPattern(self, index):
  #Ignore - row is already filled up*/
  if self.whites+self.blacks == self.length:
   return

  #If one colour in the row is at its max capacity, fill the blanks, 
  #fill the rest of the blanks in that row with the opposite colour*/
  if self.whites == self.length/2 or self.blacks == self.length/2:
   colourFill = WHITE
   if (self.blacks < self.whites): colourFill = BLACK
   
   for i in range(self.length):
    if (self.tiles[index][i] == BLANK):
     self.tiles[index][i] = colourFill


 def fillColumnPattern(self, index):
  if self.whites+self.blacks == self.length:
   return
  
  if self.whites == self.length/2 or self.blacks == self.length/2:
   colourFill = WHITE
   if self.blacks < self.whites: colourFill = BLACK
  
   for i in range(self.length):
    if self.tiles[i][index] == BLANK:
     self.tiles[i][index] = colourFill;

	 
#----------------------------------------------------------#

 """Method 3 - Find the next blank tile to place colour"""
 def method3(self, colour):
  #Find the position of the next blank tile
  endCheck = 0
  for i in range(self.length):
   for j in range(self.length):
    if self.tiles[i][j] == BLANK:
     endCheck = 1
     break
   if endCheck: break

  self.tiles[i][j] = colour
  
  