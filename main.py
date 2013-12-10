import sys
import parser
import grid

def startPuzzle(size, whites, blacks):
 puzzle = grid.Grid(size)

 for n in whites: puzzle.addWhite(n)
 for n in blacks: puzzle.addBlack(n)
  
 puzzle.run()
 puzzle.getResults()


def main():
 #Check argument 1 exist
 if len(sys.argv) != 2:
  print("Error: python main.py _")
  return

 #Open file
 file = open(sys.argv[1], "r")
 lines = file.readlines()
 file.close()

 #Check 3 lines of input
 if len(lines) != 3:
  print("Text File Error: does not contain 3 lines")
  return

 #Validate inputs
 condition1 = not parser.validateLine(lines[0])
 condition2 = not parser.validateLine(lines[1])
 condition3 = not parser.validateLine(lines[2])
 if condition1 or condition2 or condition3:
  print("Text File Error: parsing error in lines")
  return

 #Begin reading lines
 size = parser.readLine1(lines[0])
 whites = []
 blacks = []
 parser.readLine2(lines[1], whites)
 parser.readLine2(lines[2], blacks)

 #Start Puzzle with inputs
 startPuzzle(size, whites, blacks)
 
 
if __name__ == "__main__":
 main()
