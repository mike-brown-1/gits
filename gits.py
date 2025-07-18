import sys

def processDir(rootDir):
   print(f"Processing directory: {rootDir}\n")

if len(sys.argv) <= 1:
   print("You must provide a directory to search")
else:
   processDir(sys.argv[1])
