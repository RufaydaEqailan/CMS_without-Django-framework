import re

def solve(s):
   pat = "^[a-zA-Z0-9-_.rufayda]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
   if re.match(pat,s):
      return True
   return False

s = input("what is yor email?  ")
print(solve(s))