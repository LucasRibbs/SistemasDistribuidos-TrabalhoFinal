from pyDF import *
import os
import time
import re
import sys

def split(a, n):
    result = []
    k, m = divmod(len(a), n)
    for i in range(n):
        result.append(a[i*k+min(i, m):(i+1)*k+min(i+1, m)])
    return result

def sortFiles(args):
    dirs = args[0]
    for dir in dirs:
        with open(dir, 'r') as f:
            names = f.read().split("\n")
            names.sort()

def filesfrom(rootdir):
	filesname=[]
	
	for current, directories, files in os.walk(rootdir):
		for f in files:
			filesname.append(current + '/' + f)
	
	filesname.sort()
	
	return filesname

for nprocs in [1, 2, 4, 8]:
    for nfiles in [2, 4, 8]:
        sourcefiles = filesfrom("./source files")[:nfiles]
        # print(sourcefiles)
        sourcefiles = split(sourcefiles, nprocs)
        print(nprocs, " - ", nfiles, "  ->  ", sourcefiles)

        # continue

        graph = DFGraph()
        scheduler = Scheduler(graph, nprocs, mpi_enabled = False)

        feed_files = Source(sourcefiles)
        find_word_in_files = FilterTagged(sortFiles, 1)
        # matches = Serializer(print_name, 1)

        graph.add(feed_files)
        graph.add(find_word_in_files)
        # graph.add(pname)

        feed_files.add_edge(find_word_in_files, 0)

        t0 = time.time()
        scheduler.start()
        t1 = time.time()

        t_decorrido = t1 - t0

        logFile = open("./log10.txt", "a")
        logFile.write(
            "\n\n----\n" +
            "nprocs : " + str(nprocs) + "\n" +
            "nfiles : " + str(nfiles) + "\n" +
            "duracao: " + str(t_decorrido) + "\n"
            "files  : " + str(sourcefiles) + "\n" 
        )

