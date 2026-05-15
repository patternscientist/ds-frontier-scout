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

exec(open("./STTLP-GraphsAndSTT.py").read())

try: # Skip sage parts in case we run in python and do not need the sage parts.
    from sage.numerical.mip import MIPSolverException
    is_sage = True
except:
    is_sage = False

####################################
### Generic LP Utilities (start) ###
####################################

def solve_LP(f,ineq_matrix,equalities_matrix=[]):
    """ Solves a linear program subject to Ax >= b and Cx = d, minimizing f*x. A,C are matrices, b,d,f are vectors:
     'ineq_matrix':         b  is the first column, A is the rest of the columns.
     'equalities_matrix': (-d) is the first column, D is the rest of the columns. By default we only have inequalities so eqaulities_matrix is empty. """

    prog = MixedIntegerLinearProgram(maximization=False) # Can we reuse the object 'prog' over multiple LP solutions and just change objectives? or does 'solve' changes it? For now, just build it anew when called. (Solving takes more time anyway.)
    x = prog.new_variable()
    n_vars = len(ineq_matrix[0])-1 # the first column of ineq_matrix is 'b', the other columns form the matrix 'A'.
    for line in ineq_matrix:
        free,coefficients = line[0],[-i for i in line[1:]] # free + sum(coef[i]*x[i]) >= 0 <=> sum(-coef[i]*x[i]) <= free. The sage object only accepts 'less-or-equal' inequalities.
        prog.add_constraint(prog.sum(coefficients[i] * x[i] for i in range(n_vars)) <= free)
    for line in equalities_matrix:
        free,coefficients = -line[0],line[1:] # free + sum(coef[i]*x[i]) = 0 <=> sum(coef[i]*x[i]) = (-free).
        prog.add_constraint(prog.sum(coefficients[i] * x[i] for i in range(n_vars)) == free)
    prog.set_objective(prog.sum(f[i] * x[i] for i in range(n_vars))) # minimize(f*x)
    prog.solve()
    result = prog.get_values(x)
    return result

def get_D_vector_from_LP_solution(solution, dict_ids_to_var_number,n):
    """ Extracts only the coordinates of the D variables out of an (X,Z,D) solution. """
    return [solution[dict_ids_to_var_number[i]-1] for i in range(1,n+1)] # '-1' to convert from 1-indexing (variable names) to 0-indexing (index).

def get_X_matrix_from_LP_solution(solution, dict_ids_to_var_number,n):
    """ Extracts only the coordinates of the X variables out of an (X,Z,D) solution. Returns a matrix: n-tuple of n-tuples. """
    Xvec = [[0]*n for i in range(n)]
    for i in range(1,n+1):
        for j in range(1,n+1):
            if i != j: Xvec[i-1][j-1] = solution[dict_ids_to_var_number[(i,j)]-1] # '-1' to convert from 1-indexing (variable names) to 0-indexing (index).
    return tuple([tuple(line) for line in Xvec])


def extract_X_coordinates_as_dict_of_pairs(xzd_vector, n, dict_ids_to_var_number):
    """ Extracts only the coordinates of the X variables out of an (X,Z,D) solution, as a dictionary that maps (i,j) to their value. """
    X = {}
    for i in range(1,n+1):
        for j in range(1,n+1):
            if j != i: X[(i,j)] = xzd_vector[dict_ids_to_var_number[(i,j)]-1] # '-1' to convert from 1-indexing (variable names) to 0-indexing (index).
    return X

##################################
### Generic LP Utilities (end) ###
##################################



###################################
### Primal and Dual LPs (start) ###
###################################

# Modes for generating the primal LP. Some of the names are obvious (e.g. upperBoundOf1), others are better explained in the paper (e.g. LCAseparation).
ALL_PRIMAL_MODES = set(
    ['noZVariables', # The LP version without Z variables. NOTE: if 'noZVariables' is present, we override (delete modes): 'exactAncestryConstraints', 'refinedZ'.
     'upperBoundOf1', # Every variables is bounded by <=1.
     'exactAncestryConstraints', # An equality constraint Xij+Xji+sum(...) = 1; otherwise, we have >= 1.
     'exactDepthsConstraints', # An equality constraint Di=sum_j(Xji); otherwise, we have Di >= sum_j(Xji).
     'pathMonotonicity', # Add constraints such that for nodes a-b-c on a path, Xab>=Xac.
     'AncestryTransitivity', # For every triplet i,j,k we have Xij+Xjk <= Xik+1.
     'LCAseparation', # For every k between i and j (could be k=j) we have Xki+Xij <= 1.
     'refinedZ', # Not only that Zkij <= Xki,Xkj, we add that Zkij >= Xki+Xkj-1.
     ])

# Custom modes collections
modes_vanilla = [] # empty list, with Z and constraints are all inequalities.
modes_noZ = ['noZVariables']
modes_noZ_monotone = ['noZVariables','pathMonotonicity']

def construct_constraints_primal(searchTreeUtilities, modes = []):
    """ Construct the equations for the LP polytope.
    'searchTreeUtilities' has all the topological information of the underlying tree and the 'names' of the variables.
    'modes' is a subset of 'ALL_PRIMAL_MODES': a set/list of strings that customizes the constraints.
    """
    assert len(set(modes)-ALL_PRIMAL_MODES) == 0 # No unknown mode

    n,dict_ids_to_var_number = searchTreeUtilities.n,searchTreeUtilities.dict_ids_to_var_number # shortening

    equalities,inequalities,bounds = [],[],[]
    width = len(dict_ids_to_var_number)+1

    ### Ancestry (and LCA) constraints generation. ###
    if 'noZVariables' in modes: # In this case, for each (i,j) pair we generate 2^d inequalities Xij+Xji+sum(X[k,f(k)]) >= 1 for all possible 2^d functions f:(i,j)->{i,j}.
        for mode in ['exactAncestryConstraints','refinedZ']:
            if mode in modes: modes.remove(mode)
            
        for i in range(1,n+1):
            for j in range(i+1,n+1):
                between_ij = searchTreeUtilities.betweenNodes(i,j)
                d = len(between_ij)
                all_functions = [(i,j)]*d
                for case_idx in range(2**d):
                    f = cartesian_choice(all_functions,case_idx) # specific index-mapping function 'f'    
                    neq = [0]*width # holds the inequality Xij+Xji+sum(X[k,f(k)]) >= 1 as: "-1 + Xij + Xji + sum(X[k,f(k)] >= 0".
                    var_ij,var_ji = dict_ids_to_var_number[(i,j)],dict_ids_to_var_number[(j,i)]
                    neq[0],neq[var_ij],neq[var_ji] = -1,1,1 # free coefficient, Xij, Xji
                    for k_idx in range(d):
                        k,fk = between_ij[k_idx],f[k_idx] # coefficients of the sum
                        neq[dict_ids_to_var_number[(k,fk)]] = 1
                    inequalities += [tuple(neq)]
    else: # In this case, for each (i,j) pair we generate 1 main (in)equality Xij+Xji+sum(Zkij) (>)= 1 and two-three additional LCA constraints for each Zkij.
        refinedZflag = ('refinedZ' in modes)
        ancestry_constraints = []
        for i in range(1,n+1):
            for j in range(i+1,n+1):
                eq = [0]*width # 'eq' holds the (in)equality Xij+Xji+sum(Zkij) (>)= 1 as: "-1 + Xij + Xji + sum(Zkij) (>)= 0".
                var_ij,var_ji = dict_ids_to_var_number[(i,j)],dict_ids_to_var_number[(j,i)]
                eq[0],eq[var_ij],eq[var_ji] = -1,1,1
                for k in searchTreeUtilities.betweenNodes(i,j):
                    var_kij = dict_ids_to_var_number[(k,i,j)]
                    var_ki = dict_ids_to_var_number[(k,i)]
                    var_kj = dict_ids_to_var_number[(k,j)]
                    eq[var_kij] = 1
                    neqZki = [0]*width # holds the inequality of Zkij <= Xki as "Xki - Zkij >= 0".
                    neqZkj = [0]*width # holds the inequality of Zkij <= Xkj as "Xkj - Zkij >= 0".
                    neqZki[var_kij],neqZki[var_ki] = -1,1
                    neqZkj[var_kij],neqZkj[var_kj] = -1,1
                    inequalities += [tuple(neqZki)]
                    inequalities += [tuple(neqZkj)]

                    if refinedZflag:
                        neqZrefined = [0]*width # holds the inequality of 1 + Zkij - Xki - Xkj >= 0.
                        neqZrefined[0],neqZrefined[var_kij],neqZrefined[var_ki],neqZrefined[var_kj] = 1,1,-1,-1
                        inequalities += [tuple(neqZrefined)]
                        
                ancestry_constraints += [tuple(eq)]
        if 'exactAncestryConstraints' in modes:
            equalities += ancestry_constraints[:]
        else:
            inequalities += ancestry_constraints[:]

    ### More modes of constraints. ###
    if 'pathMonotonicity' in modes: # Add constraints such that for nodes a-b-c on a path, Xab>=Xac.
        for i in range(1,n+1):
            for j in range(1,n+1):
                if j == i: continue
                ks = set(searchTreeUtilities.betweenNodes(i,j))
                if len(ks) == 0: continue
                
                jneighbours = set(searchTreeUtilities.G.neighbors(j))
                ks &= jneighbours
                assert len(ks) == 1
                k = list(ks)[0]
                
                var_ik,var_ij = dict_ids_to_var_number[(i,k)],dict_ids_to_var_number[(i,j)]
                ineq = [0]*width
                ineq[var_ik],ineq[var_ij] = 1,-1 # Xik-Xij >= 0 [<=> Xik >= Xij]
                inequalities += [tuple(ineq)]

    if 'LCAseparation' in modes: # For every k between i and j (could be k=j) we have Xki+Xij <= 1.
        for i in range(1,n+1):
            for j in range(1,n+1):
                if j == i: continue
                for k in searchTreeUtilities.betweenNodes(i,j) + [j]:
                    var_ki,var_ij = dict_ids_to_var_number[(k,i)],dict_ids_to_var_number[(i,j)]
                    ineq = [0]*width
                    ineq[0],ineq[var_ki],ineq[var_ij] = 1,-1,-1 # 1-Xki-Xij >= 0
                    inequalities += [tuple(ineq)]

    if 'AncestryTransitivity' in modes: # For every triplet i,j,k we have Xij+Xjk <= Xik+1 since if Xij=Xjk=1 then Xik=1, and if Xij=0 or Xkj=0 then anything is possible (Xik >= 0).
        for i in range(1,n+1):
            for j in range(1,n+1):
                if j == i: continue
                for k in range(1,n+1):
                    if k == i or k == j: continue
                    var_ij = dict_ids_to_var_number[(i,j)]
                    var_jk = dict_ids_to_var_number[(j,k)]
                    var_ik = dict_ids_to_var_number[(i,k)]
                    eq = [0]*width
                    eq[0],eq[var_ik],eq[var_ij],eq[var_jk] = 1,1,-1,-1 # 1+Xik-Xij-Xjk >= 0
                    inequalities += [eq]

    ### Bounds constraints. ###
    # Note that we generate bounds for Z even if the mode 'noZVariables' applies, since it is simple to code, and does not matter.
    for i in range(1,len(dict_ids_to_var_number)+1):
        arr = [0]*width
        arr[i] = 1
        bounds += [tuple(arr)] # bound of 'variable >= 0'.
        if 'upperBoundOf1' in modes:
            arr = [0]*width
            arr[0],arr[i] = 1,-1
            bounds += [tuple(arr)] # bound of '1 - variable >= 0'.

    ### Depths constraints. ###
    depth_constraints = []
    for i in range(1,n+1): # Add the depths (in)equality: Di (>)= sum(Xji) as "Di - sum(Xji) (>)= 0".
        arr = [0]*width
        arr[dict_ids_to_var_number[i]] = 1
        for j in range(1,n+1):
            if j != i: arr[dict_ids_to_var_number[(j,i)]] = -1
        depth_constraints += [tuple(arr)]
    if 'exactDepthsConstraints' in modes:
        equalities += depth_constraints[:]
    else:
        inequalities += depth_constraints[:]

    return inequalities,equalities,bounds

def construct_constraints_dual(searchTreeUtilities, frequencies_input, doCappingEquationsAsInequality = False):
    """ Construct the equations for the Dual LP. searchTreeUtilities has all the topological information of the underlying tree and the 'names' of the variables. """
    n,dict_ids_to_var_number = searchTreeUtilities.n,searchTreeUtilities.dict_ids_to_var_number_DUAL # shortening

    cappingConstraints, freqConstraints, bounds = [],[],[]
    width = len(dict_ids_to_var_number)+1
    freqs = [0] + frequencies_input # adding a sentinel for indexing fj in index j etc.

    for i in range(1,n+1):
        for j in range(i+1,n+1):
            var_Rij = dict_ids_to_var_number[(i,j)]
            
            # Capping inequalities
            for k in searchTreeUtilities.betweenNodes(i,j):
                eq = [0]*width # Rij <= Qikj + Qjki [<=> 0 <= Qikj + Qjki - Rij]
                var_Qikj = dict_ids_to_var_number[(i,k,j)]
                var_Qjki = dict_ids_to_var_number[(j,k,i)]
                eq[var_Qikj] = 1
                eq[var_Qjki] = 1
                eq[var_Rij] = -1
                cappingConstraints += [tuple(eq)]

            # Frequency inequalities
            for (ii,jj) in [(i,j),(j,i)]: # two "symmetric" inequalities.
                eq = [0]*width # Rij + sum_a{Qjia} <= fj [<=> 0 <= fj -Rij + sum_a{-Qjia}]
                eq[0] = freqs[jj]
                eq[var_Rij] = -1
                for a in range(1,n+1):
                    if a == jj: continue
                    if ii in searchTreeUtilities.betweenNodes(a,jj):
                        var_Qjia = dict_ids_to_var_number[(jj,ii,a)]
                        eq[var_Qjia] = -1
                freqConstraints += [tuple(eq)]

    # Capping as equalities/inequalities.
    inequalities = freqConstraints
    equalities = cappingConstraints
    if doCappingEquationsAsInequality:
        inequalities += equalities
        equalities = []

    # Generates bounds variables >= 0.
    for i in range(1,len(dict_ids_to_var_number)+1):
        arr = [0]*width
        arr[i] = 1
        bounds += [tuple(arr)] # bound of 'variable >= 0'.
            
    return inequalities,equalities,bounds


def solve_Dual_LP(searchTreeUtilities, frequencies, returnResultsAsIs=False, ObjectiveCoefficient = {"defaultR":-1}, extraEqualities = [], extraInequalities = [], debugPrints=False):
    """ Construct and solve the Dual-LP, for a given underlying tree and frequencies.
    This function reports (prints) the resulting solution, as well as the corresponding optimal STT.
    'ObjectiveCoefficient' lets us fine-tune the objective with respect to the R variables.
       By default it should be -1 for all of them. specified (i,j) keys for i<j tuples give explicit values, and 'defaultR' key determines
       the coefficients for the rest of the unspecified pairs. As noted, by default all should be -1, so non is specified and the default is -1.
    'extraEqualities' and 'extraInequalities' can be used to "inject" extra (in)equality constraints to the LP we construct.
    """
    n,dict_ids_to_var_number = searchTreeUtilities.n,searchTreeUtilities.dict_ids_to_var_number_DUAL    
    
    cappingAsInequality = False # Without loss of generality, we can enforce equalities here, so let us do so.
    inequalities,equalities,bounds = construct_constraints_dual(searchTreeUtilities, frequencies, doCappingEquationsAsInequality = cappingAsInequality)
    assert ((len(equalities) == 0) or (not cappingAsInequality))

    inequalities_LP = inequalities + bounds + extraInequalities # The bounds 'var >= 0' are also inequalities.
    equalities_LP = equalities + extraEqualities
    
    objective_vector_of_LP = [0] * len(dict_ids_to_var_number)
    for i in range(1,n+1):
        for j in range(i+1,n+1):
            index_Rij = dict_ids_to_var_number[(i,j)] - 1 # off-by-1 due to '0' kept for the free coefficient.
            if (i,j) in ObjectiveCoefficient:
                c = ObjectiveCoefficient[(i,j)]
            else:
                c = ObjectiveCoefficient["defaultR"]
            objective_vector_of_LP[index_Rij] = c # We need to maximize the sum over all Rij, or minimize the sum over their negation. In the dual, the coefficients in the objective are fixed 1s (for R) and fixed 0s (for Q).

    # Solve, clean the result, and return or print it.
    result = solve_LP(objective_vector_of_LP,inequalities_LP,equalities_LP)
    result = clean_vector([result[i] for i in result])

    if returnResultsAsIs:
        return result

    if debugPrints: print ("\n"+"#"*10+"\n"+"Freqs = ",frequencies)
    Rsum,printableMatrix = sumR_and_printable_RQ_Dual_solution(result, n, dict_ids_to_var_number, formatter_function = _formatter_general) # Note: consider allowing here '_formatter_int' and 'printRTriangularOnly = False', may be a matter of taste.
    if debugPrints: print(printableMatrix)
    stt_opt = searchTreeUtilities.find_best_search_tree(frequencies)
    stt_value = scalar_product(stt_opt,frequencies)
    if debugPrints: print ("best stt (in primal LP): %s (value=%2.3f == Rsum=%2.7f? %s)"%(stt_opt,stt_value,Rsum,stt_value==Rsum))

#################################
### Primal and Dual LPs (end) ###
#################################



#################################################################
### LPs for Rounding, Integrality Gap, Approximations (start) ###
#################################################################
 
def compute_gaps_or_vectors_for_direction(direction, searchTreeUtilities, returnVectors=False, returnLPResultAsIs=False, nonNegativeVariables=True):
    """ Solve the LP for a topology, in a given direction. Computes 4 main depth vectors:
    (1) LP OPT (the D variables) ; (2) Best STT in that direction ; (3) Best  rounded-STT of the (fractional) solution ; (4) Worst rounded-STT of the (fractional) solution
    If 'returnVectors=True', we return the four vectors. Otherwise, we compute the following gaps and return them:
    integrality-gap (2 vs 1), approximation-ratio-best-rounding (3 vs 2), approximation-ratio-worst-rounding (4 vs 2). """
    n,dict_ids_to_var_number = searchTreeUtilities.n,searchTreeUtilities.dict_ids_to_var_number
    stt_opt = searchTreeUtilities.find_best_search_tree(direction)
    
    ### Solve the LP in the direction ###
    inequalities,equalities,bounds = construct_constraints_primal(searchTreeUtilities, modes_vanilla)
    assert len(equalities) == 0
    if nonNegativeVariables:
        inequalities_LP = inequalities + bounds # The bounds 'var >= 0' are also ineuqalities.
    else:
        inequalities_LP = inequalities

    objective_vector_of_LP = [0] * len(dict_ids_to_var_number)
    for i in range(1,n+1):
        objective_vector_of_LP[dict_ids_to_var_number[i] - 1] = direction[i-1] # Put it in the coordinates that corresponds to the depth vector D.
    result = solve_LP(objective_vector_of_LP,inequalities_LP)
    if returnLPResultAsIs: return result

    ### Round the solution to get the best and worst rounded STTs. ###
    D = get_D_vector_from_LP_solution(result,dict_ids_to_var_number,n)
    X = extract_X_coordinates_as_dict_of_pairs(result, n, dict_ids_to_var_number)
    
    possible_rounded_stts = round_to_STT(X,searchTreeUtilities.G,isFirstCall=True)
    stt_rounded_best  = scalar_product_find_smallest(direction,possible_rounded_stts)
    stt_rounded_worst = scalar_product_find_largest (direction,possible_rounded_stts)

    # Return the vectors, or the integrality gap and two approximation ratios
    if returnVectors: return D,stt_opt,stt_rounded_best,stt_rounded_worst
    
    value_lp    = scalar_product(direction,D)
    value_opt   = scalar_product(direction,stt_opt)
    cost_opt    = convert_value_to_cost(value_opt,direction)
    cost_best   = convert_value_to_cost(scalar_product(direction,stt_rounded_best) ,direction)
    cost_worst  = convert_value_to_cost(scalar_product(direction,stt_rounded_worst),direction)

    return 1.0*value_opt/value_lp , 1.0*cost_best/cost_opt , 1.0*cost_worst/cost_opt

def compute_integrality_and_approximation_gap_for_graphs(log_dir, graph_ids = None, doLogAndPrint=True):
    """ Compute the integrality gap of the graphs whose LP yields non-integer vertices in D-space (one for size n=7, multiple for n=8),
    and their approximation ratios, using the specific STT-rounding scheme proposed by Golinsky.
    CRITICAL: we only test 'primary directions', so we get lower bounds to the actual integrality gap and approximation ratios.
    We later have another approach, see function 'gaps_maximize_with_LP', to get lower bounds differently, by solving an LP that approximates these gaps/ratios. """
    if log_dir is None: f = None
    else: f = open(log_dir + os.path.sep + "gaps_primary_directions_summary_%d.txt"%(int(time.time())),'w')
    
    map_graph_to_direction = {} # up to 3 directions, one for each worst-case of: integrality gap, approximation ratio when best-rounding, approximation ratio when worst-rounding.
    
    if graph_ids is None: graph_ids = PRIMARY_DIRECTIONS.keys()
    for n,i in graph_ids:
        # initialize important variables
        graph = ALL_SMALL_GRAPHS[n][i]
        searchTreeUtilities = SearchTreeUtilities(graph)
        directions = PRIMARY_DIRECTIONS[(n,i)]
        map_graph_to_direction[(n,i,'int_gap')] = (1,None)
        map_graph_to_direction[(n,i,'approx_best')] = (1,None)
        map_graph_to_direction[(n,i,'approx_worst')] = (1,None)

        # Compute the depth-vectors tuples for all the directions
        map_directions_to_depths = {}
        for direction in directions:
            assert len(direction) == n
            int_gap, approx_best, approx_worst = compute_gaps_or_vectors_for_direction(direction,searchTreeUtilities,False)
            if map_graph_to_direction[(n,i,'int_gap')][0]      < int_gap:      map_graph_to_direction[(n,i,'int_gap')]      = (int_gap,     direction)
            if map_graph_to_direction[(n,i,'approx_best')][0]  < approx_best:  map_graph_to_direction[(n,i,'approx_best')]  = (approx_best, direction)
            if map_graph_to_direction[(n,i,'approx_worst')][0] < approx_worst: map_graph_to_direction[(n,i,'approx_worst')] = (approx_worst,direction)

    # Now report in tandem all the worst directions, for a given gap.
    for criteria in ['int_gap','approx_best','approx_worst']:
        if doLogAndPrint: log_and_print(f,criteria)
        for n,i in graph_ids:
            gap,direction = map_graph_to_direction[(n,i,criteria)]
            if direction is None: continue # In this case, all the ratios are exactly 1, so we did not update the default (1,None) value in the dictionary.
            
            searchTreeUtilities = SearchTreeUtilities(ALL_SMALL_GRAPHS[n][i])
            d_lp,d_opt,d_best,d_worst = compute_gaps_or_vectors_for_direction(direction, searchTreeUtilities,returnVectors=True) # d_xxx for depths.

            dsum = sum(direction)
            v_lp, v_opt, v_best, v_worst = [scalar_product(direction,d_vector) for d_vector in [d_lp,d_opt,d_best,d_worst]]
                
            if criteria == 'int_gap':
                vv_str = []
                for vv in [v_opt,v_lp]:
                    a,b = rational_to_a_over_b(vv,max_denominator=10,err=NUMERIC_ERROR) # value_lp;  try very small denominators to ensure true value.
                    if b == 1:    vv_str += ["%d"%(vv)]
                    elif b <= 10: vv_str += ["%d/%d"%(a,b)]
                    else:         vv_str += ["%2.5f"%(vv)]
                numerator_string,denominator_string = vv_str
               
            else:
                v_stt = (v_best if criteria == 'approx_best' else v_worst)
                if int(dsum) == dsum: # present as fractions
                    numerator_string   = "%d/%d"%(v_stt+dsum,dsum) # cost of rounded-STT
                    denominator_string = "%d/%d"%(v_opt+dsum,dsum) # cost of optimal STT
                else:
                    numerator_string   = "%2.5f"%(convert_value_to_cost(v_stt,direction))
                    denominator_string = "%2.5f"%(convert_value_to_cost(v_opt,direction))
            
            output_line_parts = [ # graph-name, direction, numerator, denominator, gap,
                str((n,i)),
                str(direction) if direction is not None else 'any',
                numerator_string,
                denominator_string,
                "%2.5f"%(gap),
                ]
            if doLogAndPrint: log_and_print(f," & ".join(output_line_parts) + "\\\\ \n \\hline")
        if doLogAndPrint: log_and_print(f,"\n"+"#"*30+"\n")
    if f is not None: f.close()

def gaps_maximize_with_LP(log_dir, graph_ids = None, doLogAndPrint=True):
    """ Runs the LP to approximate the largest integrality gap and approximation ratios for each of the graph ids (given as (n,i) names). Set the list to None to run on all of them.
    Note that the integrality-gap computation is pretty quick (< minute), the best-approx-ratio is feasible but slow (hours), and the worst-case-approx-ratio only finished for the graph (7,3). """

    if log_dir is None: f = None
    else: f = open(log_dir + os.path.sep + "gaps_via_LP_summary_%d.txt"%(int(time.time())),'w')
    
    start_time = time.time()
    if graph_ids is None: graph_ids = PRIMARY_DIRECTIONS.keys()
    
    for kind in ["int-gap","best-approx","worst-approx"]:
        if doLogAndPrint: log_and_print(f,"~~~ " + kind + " ~~~ " + str(time.time()))
        
        if kind in ["int-gap"]:
            for (n,i) in graph_ids:
                gap,direction,stt_value,lp_value = optimize_integrality_gap((n,i))
                if doLogAndPrint: log_and_print(f," ".join(map(str,[(n,i), gap,(stt_value,lp_value),direction,int(time.time()-start_time)])))
                
        if kind in ["best-approx","worst-approx"]:
            
            for (n,i) in graph_ids:
                sttUtil = SearchTreeUtilities(ALL_SMALL_GRAPHS[n][i])
                int_vertices = sttUtil.get_all_search_trees()
                collected = []
                for frac_vertex in NON_INT_VERTICES_REDUCED[(n,i)]:
                    temp = [i for i in NON_INT_VERTICES_REDUCED_WHOLE_REPRESENTATION[(n,i)] if i[0]==frac_vertex]
                    assert len(temp) == 1
                    
                    full_frac_vertex = temp[0][1]
                    X = extract_X_coordinates_as_dict_of_pairs(full_frac_vertex, n, sttUtil.dict_ids_to_var_number)

                    possible_rounded_stts = round_to_STT(X,sttUtil.G,isFirstCall=True)
                    collected += [optimize_approximation_ratio(int_vertices,frac_vertex,possible_rounded_stts,isCaseBestRounding=(kind=="best-approx"))]

                z = max([i[0] for i in collected]) # item[0] is the ratio we maximize
                direction = [i for i in collected if i[0]==z][0][1]
                if doLogAndPrint: log_and_print(f," ".join(map(str,[(n,i), z,rational_to_a_over_b(z,1000,err=10**-9),direction,int(time.time()-start_time)])))

        if doLogAndPrint: log_and_print(f,"\n"+kind+"---"*10+"\n")

def optimize_integrality_gap(topology_name):
    """
    Given a topology (by 'topology_name'), we enumerate all the primary directions and check which yields a largest integrality gap.
    It can be shown that such enumerate finds the largest additive gap of the form D*h-S*h where:
    D is an STT depths-vector, V is a non-STT-depths-vector, and h is a primary direction normalized to coordinates-sum of 1.
    Since we look for integrality gap (ratio) among such options, we simply compute D*h/S*h without normalization (not needed).
    This gives a lower-bound to gap (ratio).

    An alternative function named 'optimize_integrality_gap_by_LP' gets all the options for STT-vertices and non-STT-vertices,
    and constructs an LP to find a direction that maximizes the additive gap. It is slower, given that we have the primary directions pre-computed. """

    assert topology_name in NON_INT_TOPOLOGY_NAMES
    n = topology_name[0]
    
    bestGap,items = 0,None # The gap is at least 1, so even if there was no gap, 'items' will be not-None when we are done.
    
    for normal,stt_value,v_idx in PRIMARY_DIRECTIONS_FULL_INFO[topology_name]: # 'stt_value' is already the scalar product of 'normal' with the best STT.
        non_int_vertex = MAPPER_INDEX_TO_FULL_VERTEX[topology_name][v_idx][-n:] # 'v_idx' is used to get the actual non-STT vertex. By how we defined the coordinates, the last n entries are the depths-vector.
        lp_value = scalar_product(non_int_vertex,normal)
        gap = 1.0*stt_value/lp_value
        if gap > bestGap:
            bestGap,items = gap,(normal,stt_value,lp_value)

    normal,stt_value,lp_value = items
    return (bestGap, normal, stt_value, lp_value) # The direction ('normal') is not normalized to coordinate-sum of 1, no need.
    
def optimize_integrality_gap_by_LP(int_vertices,frac_vertex):
    """ We have D1,...,DN integer vertices ('int_vertices'), and V fractional vertex ('frac_vertex'). Look for vector f such that min_i(Di*f)-V*f is maximized.
    This is a crude approximation to maximizing the [min_i(Di*f)]/[V*f], which is the integrality gap due to V, because V*f depends on f, and it is possible that a smaller difference will result in a higher ratio.

    ### Note: we can optimize the additive gap not only by solving an LP. The alternative uses the primary directions by which we originally find each fractional vertex.
    ### Then, it suffices to enumerate only primary directions that correspond to each fractional vertex, rather than solving an LP. The alternative is likely quicker, but solving the LP is not too slow.

    We determine f by solving the following LP:
    - Variables: (x,f).
    - Inequalities: (a) x <= Di*f; (b) fi >= 0; (c) sum(fi) = 1.
    - Objective: maximize x-V*f <=> minimize V*f-x. """
    n = len(int_vertices[0])
    # Vector indices: free coefficient, x, f1, ..., fn.
    ineq_D = [[0,-1] + list(D) for D in int_vertices] # inequality for (-1,D) * (x,f) >= 0 <=> D*f >= x
    ineq_f = [[0,0] + [(1 if i == j else 0) for i in range(n)] for j in range(n)] # inequalities (0,ei)*(x,f) >= 0 <=> fi >= 0
    ineq_matrix = ineq_D + ineq_f
    eq_f = [-1,0] + [1]*n # f1+...+fn = 1
    objective = [-1] + list(frac_vertex) # minimize (-1*x + v*f) (our solver is written for minimization, use it).
    result = solve_LP(objective,ineq_matrix,[eq_f])
    x,f = result[0],[result[i] for i in range(1,len(result))]
    v1 = scalar_product(f,scalar_product_find_smallest(f,int_vertices))
    assert NUMERIC_ERROR > abs(v1-x)
    v2 = scalar_product(f,frac_vertex)
    return (1.0*v1/v2, f,v1,v2) # f is the direction, v1 = min_i(Di*f) , v2 = V*f. NOTE: here since f is found by LP, it is normalized to coordinate-sum of 1.

def optimize_approximation_ratio(int_vertices,frac_vertex,rounded_vertices, isCaseBestRounding, minIntGap=0):
    """ We have D1,...,DN integer vertices ('int_vertices'), V fractional vertex ('frac_vertex') with all rounded-vertices of V (to STT vertices) denoted by S1,...,SM ('rounded_vertices').
    Note that {S1,...,SM} is a subset of {D1,...,DN}.
    Look for vector f such that b-min_i(Di*f) is maximized, subject to min_i(Di*f) >= V*f + minIntGap. if isCaseBestRounding=True: b = min_j(Sj*f). Otherwise: b = max_j(Sj*f).

    Notes:
    (1) In either case of 'isCaseBestRounding', we approximate the approximation ratio which is actually of the form b/a rather than b-a, and this is not equivalent because a=min_i(Di*f) depends on f.
    (2) using 'minIntGap=0' mostly works fine, but it happened to fail for the graph (8,13), where the best additive gap of the LP turns out to give a 0 integrality gap,
        which means that when we solve the original LP in the found direction, we get an integer (STT) vertex without roundings. Therefore, use 'minIntGap>0' to ensure no ties.
        
    The LP we solve to determine the vector 'f' is defined as follows.
    If isCaseBestRounding=True, we solve one LP for each Di as a candidate for being the argmin of min_i(Di*f). Denote this special Di by D':
    - Variables: (x,f).
    - Inequalities: (a1) V*f <= D'*f; (a2) D'*f <= Di*f; (b) fi >= 0; (c) sum(fi) = 1; (d1) x <= Sj*f;
    - Objective: maximize x-(D'*f) <=> minimize D'*f-x.
    If isCaseBestRounding=False (worst-case rounding), we replace (d1) by (d2) below and also solve multiple copies depending on the argmax of max_j(Sj*f), denote it S':
    - Inequalities: (a1) V*f <= D'*f; (a2) D'*f <= Di*f; (b) fi >= 0; (c) sum(fi) = 1; (d2) Sj*f <= S'*f;
    - Objective: maximize (S'*f)-(D'*f) <=> minimize (D'*f)-(S'*f) = (D'-S')*f
    
    Overall very inefficient, but we only use this as a one-time run, over known vertices and roundings of the small graphs. """
    n = len(int_vertices[0])
    
    best = (1,None,None,None) # ratio, f, b, a (where we approximately-optimize b/a by considering b-a).

    for Dprime in int_vertices:
        ineq_a1 = [[-minIntGap,0] + [Dprime[i]-frac_vertex[i] for i in range(n)]] # 0 <= 0*x + (D'-V)*f <=> V*f <= D'*f.
        ineq_a2 = [[0,0] + [D[idx]-Dprime[idx] for idx in range(n)] for D in int_vertices if D != Dprime] # Similarly, inequality for D'*f <= D*f.
        ineq_b = [[0,0] + [(1 if i == j else 0) for i in range(n)] for j in range(n)] # inequalities (0,ei)*(x,f) >= 0 <=> fi >= 0
        eq_c = [-1,0] + [1]*n # f1+...+fn = 1

        specialized_options = []
        
        if isCaseBestRounding: # Only one case per Dprime.
            ineq_d = [[0,-1] + list(S) for S in rounded_vertices] # inequality for (-1,Sj) * (x,f) >= 0 <=> Sj*f >= x
            objective = [-1] + list(Dprime) # minimize (-1*x + D'*f) (our solver is written for minimization, use it).
            specialized_options = [(ineq_d,objective,None)]

        else: # Worst-case rounding. Variables: effectively only f, but keep a place-holder for x for consistency.
            for Sprime in rounded_vertices: # Multiple cases per Dprime, all options for Sprime.
                ineq_d = [[0,0] + [Sprime[idx]-S[idx] for idx in range(n)] for S in rounded_vertices if S != Sprime] # inequality for Sj*f <= S'*f <=> 0 <= (S'-Sj)*f.
                objective = [0] + [Dprime[idx]-Sprime[idx] for idx in range(n)] # minimize (D'-S')*f (our solver is written for minimization, use it).
                specialized_options += [(ineq_d,objective,Sprime)] # different options depending on the choice of Sprime

        for ineq_d,objective,Sprime in specialized_options:
            ineq_matrix = ineq_a1 + ineq_a2 + ineq_b + ineq_d
            try:
                result = solve_LP(objective,ineq_matrix,[eq_c])
            except MIPSolverException:
                continue # This is fine, in some configurations (when we choose Dprime and/or Sprime wrong) we may have no solution, so we skip these cases.
            x,f = result[0],[result[i] for i in range(1,len(result))]

            if isCaseBestRounding:
                v1 = scalar_product(f,scalar_product_find_smallest(f,rounded_vertices))
                assert NUMERIC_ERROR > abs(v1 - x) # ensure that x indeed minimizes Sj*f, yet is largest possible (results from the LP's constraints).
            else:
                v1 = scalar_product(f,Sprime)
                assert NUMERIC_ERROR > abs(v1 - scalar_product(f,scalar_product_find_largest(f,rounded_vertices))) # ensure that Sprime indeed maximizes Sj*f.
            v2 = scalar_product(f,Dprime)
            assert NUMERIC_ERROR > abs(v2 - scalar_product(f,scalar_product_find_smallest(f,int_vertices))) # ensure that Dprime indeed minimizes Di*f.
            ratio = (v1+1.0)/(v2+1.0) # recall that cost(STT) = value(STT)+1 because the depths variables are 1 less than the depth (the LP ignores a node as its own parent).
            if ratio > best[0]:
                best = (ratio, f, v1+1.0, v2+1.0) # v1+1 is cost(ROUNDED-STT), v2+1 is cost(OPT-STT).

    return best # tuple of best ratio, f (the direction that maximizes v1/v2 among solutions to the LP), v1 = min_j(Sj*f) for some j, and v2 = min_i(Di*f) (such that v2 >= V*f) for some i.

###############################################################
### LPs for Rounding, Integrality Gap, Approximations (end) ###
###############################################################



################################################################################
# Few calls to ensure that nothing is deeply broken (semi-tests, if you will). #
################################################################################

compute_integrality_and_approximation_gap_for_graphs(log_dir = None, graph_ids = [(7,3)], doLogAndPrint=False) # ~1 second.
# gaps_maximize_with_LP(log_dir = None, graph_ids = [(7,3)], doLogAndPrint=False) # ~15-20 minutes, do not run it by default as part of the tests.
for G in ALL_SMALL_GRAPHS[7]:
    STU = SearchTreeUtilities(G)
    inequalities,equalities,bounds = construct_constraints_primal(STU,ALL_PRIMAL_MODES) # Functionality-test, no values assertion.
    inequalities,equalities,bounds = construct_constraints_dual(STU,[i for i in range(1,STU.n+1)],True) # Functionality-test, no values assertion.
    if is_sage:
        direction = [1]*STU.n
        solve_Dual_LP(STU, direction, returnResultsAsIs=False, ObjectiveCoefficient = {"defaultR":-1}, extraEqualities = [], extraInequalities = []) # Functionality-test, no values assertion.

