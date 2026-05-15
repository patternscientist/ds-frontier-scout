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

# This is a hack so I can run the sage code from linux without changing the '.py' extension.
exec(open("./STTLP-main-and-tests.py").read())
