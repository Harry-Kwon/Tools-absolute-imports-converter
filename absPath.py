import sys, os
fileName = sys.argv[1]
projectRoot=""
if len(sys.argv)>2:
    projectRoot = sys.argv[2]

filePath = os.path.abspath(fileName)
fileDir = os.path.dirname(filePath)

def convertFile(fileName, lineModifier):
    with open(fileName, "r") as f:
        lines = f.readlines()

    lines = [lineModifier(line) for line in lines]

    with open(fileName, "w") as f:
        for data in lines:        
            f.write(data)

def toAbsImports(line, prefix="import", startKey="from '.", endKey="';", pathRoot=""):
    if (line[:len(prefix)] == prefix) and (startKey in line) and (endKey in line):
        modified = toAbsPath(line[line.index(startKey)+len(startKey)-1:line.index(endKey)])
        if modified[:len(pathRoot)] == pathRoot:
            modified = modified[len(pathRoot):]
            if modified[0] == "/":
                modified = modified[1:]
            modified = line[:line.index(startKey)+len(startKey)-1] + modified + line[line.index(endKey):]
            return modified
    return line

def toAbsPath(path):
    absPath = relJoin(fileDir, path.split("/")[:-1])
    absPath += "/" + path.split("/")[-1]
    return absPath 

def relJoin(root, relPath):
    if len(relPath)==0:
        return root
    
    if relPath[0] ==  ".":
        return relJoin(root, relPath[1:])
    if relPath[0] == "..":
        return relJoin(root[:-len(root.split("/")[-1])][:-1], relPath[1:])
    else:
        return relJoin(root + "/" + relPath[0], relPath[1:])

if __name__ == "__main__":
    convertFile(fileName, lambda x : toAbsImports(x, pathRoot=projectRoot))
