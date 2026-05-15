###########################################################################################
### The following code is python-based sage. Written by Yaniv Sadeh.                    ###
### Sage snippets can be run online, e.g. at: https://sagecell.sagemath.org/            ###
###                                                                                     ###
### The code is divided into 6 (7) parts that assume same-dir location and              ###
### call each other in hierarchy. The division is based on the logic:                   ###
### (0) main.sage:                                                                      ###
###       A "hack" to easily run the code in sage (expects '.sage' extension)           ###
###       while editing the rest of the files in a pyhon editor ('.py' extension).      ###
### (1) STTLP-main-and-tests.py: (This part requires Sage)                              ###
###       The top-file that calls the rest of them. Contains all the top-level          ###
###       tests and data generation calls, including explicit examples for              ###
###       generating the outputs mentioned in the paper.                                ###
### (2) STTLP-LPs.py: (This part requires Sage)                                         ###
###       Logic for generating and solving LPs. The main LP, its dual, and              ###
###       few additional LPs that come up in the context of maximizing                  ###
###       integrality gap and approximation ratios.                                     ###
### (3) STTLP-GraphsAndSTT.py: (This part can be fully run in Python3)                  ###
###       This part contains the logic that deals with topologies, STT, etc.            ###
###       It does touch a little on the LPs by defining dictionaries to "name"          ###
###       The variables, but not more than that.                                        ###
### (4) STTLP-BasicUtils.py: (This part can be fully run in Python3)                    ###
###       Basic utilities for printing outputs and doing some basic operations.         ###
### (5) STTLP-HardcodedValues.py: (This part can be fully run in Python3)               ###
###       A bulk of pre-computed data, primary-directions, non-STT vertices, etc.       ###
###       Computing this data ranges from minutes to several hours (depending which     ###
###       part), so we keep it hard-coded to speed up anything that relies on it.       ###
### (6) parse_logs.py: (This part can be fully run in Python3)                          ###
###       This is an ugly ad-hoc script to parse output scripts that are genearated     ###
###       by analysis function in 'STTLP-main-and-tests.py'. No interesting logic here. ###
###                                                                                     ###
###########################################################################################

import glob
import networkx

MODE_GRAPH_INFOS = 1
MODE_GRAPHS_EDGES = 2
MODE_LINE = 3
MODE_PARTIAL_INTEGRALITY = 4

def prepad(s,n): return "\\ "*(n-len(s))+s

def purify_denominators(d, checkMixed23=False):
    result = set()
    for i in d:
        for j in i: result.add(j)
        if checkMixed23 and 2 in i and 3 in i: print ("*"*30+"\n"+"mixed vertex! (assuming this is not a 6-divisible denominator)."+"\n"+"#"*30)
    return result

def parse_log(log_path,table_mode):
    lines = open(log_path,'r').readlines()

    # Initialize variables.
    testId = 0
    graph,v_all,v_int,v_stt,v_frac,h_all,h_stt = None,None,None,None,None,None,None
    d_denominators,xzd_denominators = [],[]
    denominators = [None] * 10 # for TestID=1,...,9 and with a sentinel.
    v_fracs = [[] for i in range(10)]
    exhaustedSpace = True

    # Parse the log. Very custom-made for the logs in their current form.
    temp = log_path.split("_")
    graph_name = "(%s,%s)"%(temp[-3],temp[-2])
    for line in lines:
        if line.startswith("TestI"):
            testId = int(line[len("TestId-"):]) # Have to catch both "TestID" and "TestId".
            if testId > 3: exhaustedSpace = False
        if testId == 1:
            if "Graph:" in line: graph = line.split("edges=[")[-1].split("]")[0]
            if "total number of vertices" in line: v_all = int(line.split(" total")[0].split(" ")[-1])
            if "integer vertices" in line: v_int = int(line.split(" integer")[0].split(" ")[-1])
            if "STT vertices" in line: v_stt = int(line.split(" STT")[0].split(" ")[-1])
            if "fractional vertices" in line: v_frac = int(line.split(" fractional")[0].split(" ")[-1])
            if "denominators fine-grained" in line: d_denominators = eval("{" + line.split("{")[-1].split("}")[0] + "}").keys()
            if "hyperplanes count" in line:
                parts = line.split(" ")
                h_all,h_stt = int(parts[-2]),int(parts[-1])
        else:
            if "denominators fine-grained" in line:
                xzd_denominators += eval("{" + line.split("{")[-1].split("}")[0] + "}").keys()
        if "denominators fine-grained" in line:
            checkMixed23 = (testId in [5,6,7,8,9])
            denominators[testId] = purify_denominators(eval("{" + line.split("{")[-1].split("}")[0] + "}").keys(),checkMixed23)
        if "fractional vertices" in line:
            v_fracs[testId] +=  [int(line.split(" fractional")[0].split(" ")[-1])]
            
    denominatorsD = purify_denominators(d_denominators)
    denominatorsXZD = purify_denominators(xzd_denominators)

    h_planes_string = prepad(str(h_all),5) + (" (%s)"%(str(h_stt)) if h_all != h_stt else "")

    if v_int!=v_stt: print ("interesting!!!",graph_name,v_int-v_stt)
    
    if table_mode == MODE_GRAPH_INFOS:
        print ("%s & %s & %s & %s & %s & %s \\\\"%(
            graph_name,
            prepad(str(v_stt),5),
            h_planes_string,
            prepad(str(v_frac),3),
            str(sorted(denominatorsD)).replace("[","\\{").replace("]","\\}"),
            str(sorted(denominatorsXZD)).replace("[","\\{").replace("]","\\}") + (" {*}" if exhaustedSpace else "")
            ))
    elif table_mode == MODE_GRAPHS_EDGES:
        edges = eval("["+graph+"]")
        diameter = 1+networkx.diameter(networkx.Graph(edges)) # The package computes diameter in edges (weighted/unweighted), we need it in vertices.
        print ("%s & %d & %s \\\\"%(graph_name,diameter,graph))
    elif table_mode == MODE_LINE:
        assert None not in denominators[4:10]
        denominators = [sorted(i) if i is not None else None for i in denominators]
        print ("%s & %s & %s & %s & %s & %s & %s \\\\"%(log_path.split("_")[2],denominators[4],denominators[7],denominators[5],denominators[8],denominators[6],denominators[9]))
    elif table_mode == MODE_PARTIAL_INTEGRALITY:
        purified = []
        for (i,l) in enumerate(v_fracs):
            if len(l) > 0 and min(l)<max(l): purified += [(i,l)]
        if len(purified) > 0:
            print (graph_name, purified)
    else:
        raise Exception("Undefined table mode.")
                
    return (
        graph, v_all, v_int, v_stt, v_frac, sorted(d_denominators), h_all, h_stt, sorted(set(xzd_denominators))
    )

