#encoding=utf-8
import os
import sys
import re
import glob

def checkLine(text, regexObject):
    text = text.strip()
    if(regexObject.search(text)):
        return 1
    else:
        return 0
        
def makeResultsTable(results, unsafeNames, tableFile):
    exportData = ""
    for result in results:
        fileResult = result[0]
        lineResult = result[1].lstrip()
        lineResult = lineResult.replace(";","")
        lineResult = lineResult.replace("\t","")
        ruleResult = ""
        for rule in unsafeNames:
            regex = rule
            regexFunc = re.compile(regex, re.IGNORECASE)
            if regexFunc.search(lineResult):
                ruleResult = rule
                break
        exportData = exportData + fileResult + " ; " + lineResult + " ; " + ruleResult + "\n"
    outputTable = open(tableFile, "w")
    outputTable.write(exportData)
    outputTable.close()

if len(sys.argv) < 4:
    print("Usage: " + sys.argv[0] + " <path to check> <0=TCLprocs, 1=ALLfiles> <0=noTable, 1=createTable> <table file>")
    exit()

path = sys.argv[1]
toolNames = int(sys.argv[2])
makeTable = int(sys.argv[3])
tableFile = ""
if makeTable:
    try:
        tableFile = sys.argv[4]
    except Exception as e:
        print("Missing table file name.")
        raise e

if (toolNames):
    namesFile = open("unsafe_list2.txt", "r")
else:
    namesFile = open("unsafe_list.txt", "r")
unsafeNames = namesFile.read()
namesFile.close()
unsafeNames = unsafeNames.split("\n")
unsafeNames.pop() #Last item is always a blank string

regex = ""
for name in unsafeNames:
    if (toolNames):
        regex = regex + "[\s!#\[\]~`\"'_\-*(+,;)&$|.]" + name + "[\s!#\[\]~`\"'_\-*(+,;)&$|.]" + "|"
    else:
        regex = regex + "[\-_\s]" + name + "[-_\s]" + "|"
    
regex = regex.rstrip("|")
regexFunc = re.compile(regex, re.IGNORECASE)

regex = "^proc\s"
regexProcFunc = re.compile(regex, re.IGNORECASE)

regex = "^[\s]*#"
regexCommentFunc = re.compile(regex, re.IGNORECASE)

occurrences = 0

if (len(path) > 1):
    os.chdir(path)

tclFiles = glob.glob('./**/*.tcl', recursive=True)
if (toolNames): #Extra files extensions that are not images or binaries
    tclFiles = tclFiles + glob.glob('./**/*.cpp', recursive=True)
    tclFiles = tclFiles + glob.glob('./**/*.h', recursive=True)
    tclFiles = tclFiles + glob.glob('./**/*.cc', recursive=True)
    tclFiles = tclFiles + glob.glob('./**/*.hh', recursive=True)
    tclFiles = tclFiles + glob.glob('./**/*.lib', recursive=True)
    tclFiles = tclFiles + glob.glob('./**/*.lef', recursive=True)
    tclFiles = tclFiles + glob.glob('./**/*.def', recursive=True)
    tclFiles = tclFiles + glob.glob('./**/*.sdc', recursive=True)
    tclFiles = tclFiles + glob.glob('./**/*.v', recursive=True)
    tclFiles = tclFiles + glob.glob('./**/*.sh', recursive=True)
    tclFiles = tclFiles + glob.glob('./**/*.py', recursive=True)
    tclFiles = tclFiles + glob.glob('./**/*.txt', recursive=True)
    tclFiles = tclFiles + glob.glob('./**/*.md', recursive=True)
    tclFiles = tclFiles + glob.glob('./**/*.i', recursive=True)
    tclFiles = tclFiles + glob.glob('./**/*.cmake', recursive=True)
    tclFiles = tclFiles + glob.glob('./**/*.in', recursive=True)
results = []
numFiles = 0
print("Files to check: " + str(len(tclFiles)) + ".")

for tclInterface in tclFiles:
    if (not(toolNames) and (("OpenSTA" in tclInterface) or ("resizer" in tclInterface))):
        continue
    try:
        with open(tclInterface, encoding="utf8", errors='ignore') as f:
            textData = f.read().split("\n")
            f.close()
            for line in textData:
                if (toolNames):
                    if regexFunc.search(line):
                        #print("UNSAFE NAME FOUND IN FILE: " + tclInterface + " . VIOLATED LINE: " + line)
                        currentResult = [tclInterface, line]
                        results.append(currentResult)
                        occurrences += 1
                else:
                    if not(checkLine(line, regexCommentFunc)) and checkLine(line, regexProcFunc):
                        parameterStart = line.find("{")
                        if (parameterStart > 0):
                            line = line[0:parameterStart]
                        if regexFunc.search(line):
                            print("UNSAFE NAME FOUND IN FILE: " + tclInterface + " . VIOLATED LINE: " + line)
                            currentResult = [tclInterface, line]
                            results.append(currentResult)
                            occurrences += 1
            numFiles += 1
            if (numFiles % 500 == 0):
                print("Files checked: " + str(numFiles) + ".")
    except:
        print("File reading error! File: " + tclInterface)

print("Number of occurences: " + str(occurrences) + ".")

if (makeTable):
    makeResultsTable(results, unsafeNames, tableFile)
