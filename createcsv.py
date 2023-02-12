import os
import math

def filesfrom(rootdir):
	filesname=[]
	
	for current, directories, files in os.walk(rootdir):
		for f in files:
			filesname.append(current + '/' + f)
	
	filesname.sort()
	
	return filesname

def idx(nfiles):
    return int(math.log(nfiles,2)) - 1

def invertIdx(i):
    return (2)**(i+1)


report = {
    1:[0.0, 0.0, 0.0],
    2:[0.0, 0.0, 0.0],
    4:[0.0, 0.0, 0.0],
    8:[0.0, 0.0, 0.0]
}

logsList = filesfrom("./logs")

for log in logsList:
    log = logsList[0]
    f = open(log, "r")
    testes = f.read().split("\n\n----")[1:]

    for i in range(0, len(testes)):
        teste = testes[i].split("\n")
        nprocs = int(teste[1].split(":")[1])
        nfiles = int(teste[2].split(":")[1])
        duracao = float(teste[3].split(":")[1])

        report[nprocs][idx(nfiles)] += duracao

print(report)

for key in report.keys():
    # for i in range(0,len(report[key])):
    report[key] = [duracao/10 for duracao in report[key]]

print(report)

f = open("./report.csv", "w")
text = "num_files_sorted,num_workers,execution_time\n"
for i in range(0,3):
    for key in report.keys():
        text = text+str(invertIdx(i))+","+str(key)+","+str(report[key][i])+"\n"

f.write(text)
