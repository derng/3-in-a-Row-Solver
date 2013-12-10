def constructN(n, c):
 digit = ord(c) - ord('0')
 n *= 10
 return n + digit

def isDigit(c):
 n = ord(c) - ord('0')
 return n >= 0 and n <= 9 

def readLine1(line):
 n = 0
 for c in line:

  if c.isdigit():
   n = constructN(n, c)
  else:
   break
  
 return n


def validateLine(line):
 hasDigit = 0
 
 for c in line:
  if c == '\r' or c == '\n' or c == ' ':
   continue
  elif not isDigit(c):
   return 0
  hasDigit = 1
  
 return hasDigit

def readLine2(line, indexes):
 n = 0
 for c in line:
  if c == '\r' or c == '\n': break

  if isDigit(c):
   n = constructN(n, c)
   if n == 0: break
   
  else:
   if (n == 0): continue
   indexes.append(n)
   n = 0
   
 if (n != 0):
  indexes.append(n)
