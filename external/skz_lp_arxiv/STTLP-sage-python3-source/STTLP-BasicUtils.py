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

import time
import math
import random
import os

NUMERIC_ERROR = 10**-7
INFINITY = 10**10

##############################
### Math Utilities (start) ###
##############################
             
def convert_value_to_cost(lp_value, direction):
    """ The STT search cost is (LP value)/(sum(direction)) + 1. We divide by sum(direction) to normalize and get a vector of query frequencies. """
    return 1 + (1.0 * lp_value / sum(direction))

def cartesian_choice(list_of_lists, index):
    """ Returns a cartesian combination from a list of lists. The index determines how to pick an item from each list. """
    items = []
    for L in list_of_lists:
        items += [L[index%len(L)]]
        index //= len(L)
    return items

def scalar_product(v1,v2):
    """ Scalar product between v1 and v2. Assumes both have the same length. """
    return sum([v1[i]*v2[i] for i in range(len(v1))])

def scalar_product_find_smallest(v,vectors):
    """ Returns a vector v1 in vectors such that v*v1 is minimized. """
    best_vec,best_cost = None,INFINITY
    for vec in vectors:
        s = scalar_product(v,vec)
        if s < best_cost: best_vec,best_cost = vec,s
    return best_vec

def scalar_product_find_largest(v,vectors):
    """ Returns a vector v1 in vectors such that v*v1 is maximized. """
    return scalar_product_find_smallest([-i for i in v], vectors)

def generate_positive_rays(n):
    """ Given n, generate all the n-dimensional (positive) standard-base unit vectors. """
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def rational_to_a_over_b(value,max_denominator=1000,err=NUMERIC_ERROR):
    """ Given a value 'value', attempts to present it as a/b for minimal b (both a,b are integer). Assumes that the value is a fraction, with denominator at most max_denominator. """
    for b in range(1,max_denominator):
        a = round(value*b)
        if abs(value*b - a) < err*b: # scale the error as well because we multiply by b (instead of dividing the difference by b).
            return (a,b)
    return (round(value*INFINITY),INFINITY) # approximation, with a large denominator.

def vector_denominators(vector):
    """ Returns all the smallest denominators of the coordinates of the input vector. No counting, just existence of denominators. """
    denominators = set()
    for value in vector:
        denominators.add(rational_to_a_over_b(value)[1]) # value = a/b, only add b to the set.
    return tuple(sorted(denominators))

def is_integer_vector(vec):
    """ Returns true iff all the coordinates are integer. """
    return max([abs(i-round(i)) for i in vec]) <= NUMERIC_ERROR

def clean_vector(vector,max_denominator=20,err=NUMERIC_ERROR):
    """ An artefact of the LP solver, sometimes returns '-0' values, or integers as floats. We also fix (round) numeric-errors. """
    new_vector = list(vector[:])
    for i in range(len(new_vector)):
        v = new_vector[i]
        _,b = rational_to_a_over_b(v,max_denominator,err)
        if b == 1: new_vector[i] = int(round(v)) # integer
        else:      new_vector[i] = 1.0 * round(v*b) / b # float
    return new_vector

############################
### Math Utilities (end) ###
############################



#######################################
### Print/Logging Utilities (start) ###
#######################################

def log_and_print(f,st,sep="\n"):
    "Reports the string 'st' to the screen, as well as to a file f if it exists. f is either None (no file) or an open file handler."
    print (st)
    if f is not None: f.write(st+sep)

def _formatter_general(value):
    if value is None: return ' .    '
    return "%2.3f "%(value)

def _formatter_compact(value):
    if value is None: return ' .  '
    return "%1.1f "%(value)

def _formatter_int(value,digits=2):
    if value is None: return (digits-1)*' ' + '. '
    return ("%"+str(digits)+"d ")%(value)

def print_XZD_solution(XZD_vector, n, dict_ids_to_var_number, formatter_function = _formatter_compact, alsoPrintZ = False):
    """ Neatly prints a solution vector in (X,Z,D) space. X is shown as a matrix, D below it as column-sums. Z to the side, if 'alsoPrintZ' is true. """
    if isinstance(XZD_vector,dict):
        XZD_vector = [XZD_vector[i] for i in range(len(XZD_vector))]

    XZD_vector = clean_vector(XZD_vector)
    s = "X=\n"
    for i in range(1,n+1):
        s += "  ["
        for j in range(1,n+1):
            if j == i:
                s += formatter_function(None)
            else:
                idx = dict_ids_to_var_number[(i,j)]-1
                s += formatter_function(XZD_vector[idx])
        s += "]"
        if alsoPrintZ:
            s += "   Z: "
            for key in dict_ids_to_var_number:
                if isinstance(key,int): continue # skip Ds
                if len(key) < 3: continue # skip Xs
                if key[1] != i: continue # irrelevant Z
                idx = dict_ids_to_var_number[key]-1
                s += "Z_"+"".join(map(str,key))+"="+formatter_function(XZD_vector[idx])+", "
        s += "\n"
    s += "D=["
    for i in range(1,n+1):
        idx = dict_ids_to_var_number[i]-1
        s += formatter_function(XZD_vector[idx])
    s += "]\n"
    print (s)

def sumR_and_printable_RQ_Dual_solution(RQ_vector, n, dict_ids_to_var_number, formatter_function = _formatter_general, printRTriangularOnly = True, printQValues = True):
    """ Returns a printable string of the solution vector in (R,Q) space, and the sum of R variables.
    If 'printRTriangularOnly=True' R is shown as a triangular matrix (Rij only for i<j), otherwise it is a symmetrix matrix (Rij=Rji). Q is to the side of the matrix R. """
    if isinstance(RQ_vector,dict):
        RQ_vector = [RQ_vector[i] for i in range(len(RQ_vector))]

    RQ_vector = clean_vector(RQ_vector)
    Rsum = 0
    s = "R=\n"
    for i in range(1,n+1):
        s += "  ["
        for j in range(1,n+1):
            if j == i:
                s += formatter_function(None)
            else:
                a,b = min(i,j),max(i,j)
                idx = dict_ids_to_var_number[(a,b)]-1
                if j < i: Rsum += RQ_vector[idx]
                if printRTriangularOnly and j < i:
                    s += formatter_function(None)
                else:
                    s += formatter_function(RQ_vector[idx])
                
        s += "]"
        if printQValues: # Print all Qiab for applicable pairs of a,b.
            s += "   Q: "
            for a in range(1,n+1):
                for b in range(1,n+1): # naive check if such Q variable exists, time-wasteful but not too much.
                    key = (i,a,b)
                    if key in dict_ids_to_var_number:
                        idx = dict_ids_to_var_number[key]-1
                        s += "Q_"+"".join(map(str,key))+"="+formatter_function(RQ_vector[idx])+", "        
        s += "\n"
    s += "R-sum: " + formatter_function(Rsum)
    return Rsum,s

#####################################
### Print/Logging Utilities (end) ###
#####################################

################################################################################
# Few calls to ensure that nothing is deeply broken (mini-tests, if you will). #
################################################################################

assert convert_value_to_cost(1.23, [1,2,3]) == ((1.23 / 6) + 1)
assert scalar_product([1,2,3],[4,5,6]) == 32
assert scalar_product_find_smallest([1,2,3],[[4,5,6],[4.5,5.5,6.5],[3.5,4,5]]) == [3.5,4,5]
assert scalar_product_find_largest([1,2,3],[[4,5,6],[4.5,5.5,6.5],[3.5,4,5]]) == [4.5,5.5,6.5]
assert generate_positive_rays(3) == [[1,0,0],[0,1,0],[0,0,1]]
assert is_integer_vector([0,1,2,3]) and not is_integer_vector([0,1.1,2,3])
assert rational_to_a_over_b(2.01,5,err=0.1) == (2,1) and rational_to_a_over_b(1.33333,5,err=0.001) == (4,3)
assert vector_denominators([0.5,0.3333333333,1]) == (1,2,3)
assert clean_vector([-0,1.0001,0.3333333456],max_denominator=5,err=0.001) == [0,1,1/3.]
assert cartesian_choice([[1,2,3],[4,5,6]], 4) == [2,5] and cartesian_choice([[1,2,3],[4,5,6]], 6) == [1,6]


