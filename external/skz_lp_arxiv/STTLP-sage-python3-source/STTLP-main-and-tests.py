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

exec(open("./parse_logs.py").read())
exec(open("./STTLP-LPs.py").read())

REPORT_INTERVAL_IN_SECONDS = 30 # a compromise between log-spamming and progress tracking.
LOG_DIR = "/mnt/c/temp/"  # runs in windows' WSL so we need a linux path.

##################################
### Analysis Functions (start) ###
##################################

def enrich_D_space_vertices(searchTreeUtilities,debugPrints=False,maxIteration=None,maxMemSize=10**8):
    """ Working in Depths-space: Given a 'searchTreeUtilities' object, we begin from the polytope spanned by all the STTs and positive rays.
    Then we iteratively refine as follows: span the polytope, solve the LP for each normal to a hyperplane (facet), and if a new vertex is encountered,
    add it to the list of vertices for the next iteration. Proceed in iteration until no additional vertices are found, or up to 'maxIteration' if it is not None.
    Conversion from vertices to hyperplanes is a blackbox usage of sage, by defining a polytope as V-representation and then working on it as H-representation.

    @@@ Returns a two dictionaries:
    (1) dictionary of all enriched (non-STT) vertices. The key is the iteration in which each vertex was found, the values are sets, each is of tuple of (vertex,direction,value) for the found vertices. value is the LP value of any point on the false-facet, with respect to the direction.
    (2) dictionary of the hyperplanes count in each iteration, the number of normals we tested for enrichment in that iteration.
    
    Concretely, for each hyperplane we have a normal vector Ni of positive coefficients such that Ni*D >= ci for a non-negative constant ci. (Ni is the 'direction', ci is the 'value'.)
    We pick each of these normals as the depths coefficients, and solve for it the original LP over (X,Z,D) to see if the resulting optimum is one of the search-tree vertices, or a new one.
    (We take the normal as-is, because normalization will only affect the objective function by a fixed constant factor.) """
    # Output dictionaries
    iteration_to_new_vertices_and_directions = {}
    iteration_to_hyperplanes_count = {}

    # Initialization
    time_start = time.time()
    time_last_progress_report = time_start

    # The LP to solve is always the same, so we compute it once in advance.
    dict_ids_to_var_number = searchTreeUtilities.dict_ids_to_var_number
    inequalities,equalities,bounds = construct_constraints_primal(searchTreeUtilities, modes_vanilla)
    assert len(equalities) == 0
    inequalities_LP = inequalities + bounds # The bounds 'var >= 0' are also inequalities.


    new_vertices = set(searchTreeUtilities.get_all_search_trees())
    all_vertices = set([])
    iteration = 0
    if maxIteration == None: maxIteration = INFINITY

    print ("Graph:",sorted(searchTreeUtilities.G.edges()))
    solved_directions = set() # recall directions which we solved, to skip LP-solving.
    while len(new_vertices) > 0 and iteration < maxIteration:
        iteration += 1
        all_vertices |= new_vertices
        new_vertices = set([])
        print ("pre-iteration  %d: known vertices = %d"%(iteration,len(all_vertices)))
        
        # Compute the depth-polytope
        p = Polyhedron(vertices = all_vertices, rays = generate_positive_rays(searchTreeUtilities.n))

        # Convert to special directions and solve the LP for each of them.
        #if debugPrints: print ("Iteration: %d: started looping half-spaces, %d to go..."%(iteration, p.n_Hrepresentation()))

        counter = 0
        for h in p.Hrepresentation(): # The call to 'p.Hrepresentation()' may be very heavy since it computes the cnovertsion from V-representation to H-representation.
            counter += 1
            lp_value,direction = (-h[0]),h[1:] # The desired direction is h[1:]. Any point on the facet has value of h[0] in that direction.
            assert lp_value >= 0 # must always be non-negative, since the halfspaces are non-negative and the inequality is of the form: h[1]*var[1]+... >= h[0] >= 0.
            
            if debugPrints and time.time() - time_last_progress_report > REPORT_INTERVAL_IN_SECONDS:
                time_last_progress_report = time.time()
                print ("progress: counter = %d (time passed: %5.3f seconds)"%(counter,time_last_progress_report-time_start))

            if tuple(direction) in solved_directions:
                continue
            if len(solved_directions) < maxMemSize: # Memory-overflow failsafe
                solved_directions.add(tuple(direction))
            
            # Solve the LP: same inequalities, new direction.
            objective_vector_of_LP = [0] * len(dict_ids_to_var_number)
            for i in range(1,searchTreeUtilities.n+1):
                objective_vector_of_LP[dict_ids_to_var_number[i] - 1] = direction[i-1] # Put it in the coordinates that corresponds to the depth vector D.
            result = solve_LP(objective_vector_of_LP,inequalities_LP)
            depths_vector = clean_vector([result[dict_ids_to_var_number[i] - 1] for i in range(1,searchTreeUtilities.n+1)])

            cost_solution = scalar_product(direction,depths_vector)
            if cost_solution + NUMERIC_ERROR < lp_value:
                if iteration not in iteration_to_new_vertices_and_directions: iteration_to_new_vertices_and_directions[iteration] = set() # initialization
                iteration_to_new_vertices_and_directions[iteration].add((tuple(depths_vector),tuple(direction),lp_value))
                new_vertices.add(tuple(depths_vector))
                if debugPrints: print ("NEW VERTEX FOUND! Iteration: %d, Direction (objective): %s, Depths-vector: %s)."%(iteration,direction,depths_vector))

        print ("post-iteration %d: scanned h-planes = %d"%(iteration,counter))
        iteration_to_hyperplanes_count[iteration] = counter
        
    return iteration_to_new_vertices_and_directions,iteration_to_hyperplanes_count

def enumerate_all_vertices(key=(5,0),withMonotonicity=False,withZ=False,printNonIntVertices=False):
    """ The LP polytope for the path with n=5 nodes has 165 non-integer vertices, only 4 if we add monotonicity constraints.
    However, the 'T' topology with 5 nodes is integer, but becomes non-integer if we add monotonicity constraints.
    if 'printNonIntVertices=True', prints all the non-integer vertices nicely. """
    n,i = key
    
    searchTreeUtilities = SearchTreeUtilities(ALL_SMALL_GRAPHS[n][i])
    n,betweenListOracle = searchTreeUtilities.n,searchTreeUtilities.betweenNodes

    if withZ:
        modes_list = modes_vanilla
    elif withMonotonicity:
        modes_list = modes_noZ_monotone
    else:
        modes_list = modes_noZ
        
    inequalities,equalities,bounds = construct_constraints_primal(searchTreeUtilities, modes_list)
    assert len(equalities) == 0
    p = Polyhedron(ieqs = inequalities + bounds, eqns = equalities)
    
    counter = 0
    denominators_counters = {}
    all_vertices = [v for v in p.Vrepresentation() if v.is_vertex()] # collect all the vertices, skip the rays.
    
    for v in all_vertices:
        temp = vector_denominators(v)
        if temp not in denominators_counters: denominators_counters[temp] = 0
        denominators_counters[temp] += 1
        
        if vector_denominators(v) != (1,): # integer, only 'denominators of 1'.
            counter += 1
            if printNonIntVertices:
                print (counter)
                print_XZD_solution(v,n,searchTreeUtilities.dict_ids_to_var_number,_formatter_compact,False)
    if (not withZ) and key in [(5,0),(5,1)]:
        if key == (5,0):
            if withMonotonicity: assert counter == 4 # In this case, adding the constraints "mostly helps"
            else:                assert counter == 165
        if key == (5,1):
            if withMonotonicity: assert counter == 82 # Adding the constraints makes the polytope non-integer
            else:                assert counter == 0
    print ("      Summary of vertex denominators:",denominators_counters)

def vertices_statistics(vertex_list,stt_count=None):
    """ vertex_list is a list of tuples, each represents a vertex in arbitrary dimension. We compute the following:
    #total, #integer-vertices, #fractional, and a dictionary of vertices with fractional denominators (keys are tuples of denominators, values are counters). """
    vertex_list = list(set(vertex_list)) # remove duplicates
    INTEGER_KEY = (1,)

    count_total = len(vertex_list)
    count_int = 0
    count_frac = 0
    count_frac_special_int = 0
    
    denominators_counters = {}
    for v in vertex_list:
        key = vector_denominators(v)
        
        if key not in denominators_counters: denominators_counters[key] = 0
        denominators_counters[key] += 1
        if key == INTEGER_KEY: count_int += 1
        else: count_frac += 1
    assert count_int+count_frac == count_total and sum(denominators_counters.values()) == count_total

    report_string = ''
    report_string += "... %6d total number of vertices\n"%(count_total)
    report_string += "...... %6d integer vertices\n"%(count_int)
    if stt_count is not None:
        report_string += "......... %6d STT vertices\n"%(stt_count)
    report_string += "...... %6d fractional vertices\n"%(count_frac)
    report_string += "denominators fine-grained: %s\n"%(str(denominators_counters))
    return (count_total,count_int,count_frac,denominators_counters,report_string)

def exhaustive_analysis(graph, tests_to_run, output_log, sampling_steps = 1000, debugPrintEnrichmentFunction=False, reportPartialIntegerVertices=True):
    """
    Runs multiple analyses on a given tree (graph). List of possible tests:

    test_id=1: analyze all the vertices in D-space (repeated normal-method enrichment).
    test_id=2: enumerate all the vertices of the LP in XZD-space (define the polytope, and enumerate; no LP-solving). Defined as usual, relaxed form.
    test_id=3: enumerate all the vertices of the LP in XZD-space (define the polytope, and enumerate; no LP-solving). Defined without Z-coordinates, using the end-result of a Fourier-Motzkin elimination.

    test_id=[4,...,9]: No enumeration, only sampling of vertices in XZD-space. Because we cannot enumerate, we study the sampled vertices in XZD-space, XD-space, and D-space (when computing statistics).
    test_id=4: Usual LP form,      Fully-arbitrary objective direction.
    test_id=5: Usual LP form,      XD-only objective direction.
    test_id=6: Usual LP form,      D-only objective direction.
    test_id=7: LP Fourier-Motzkin, Fully-arbitrary objective direction.
    test_id=8: LP Fourier-Motzkin, XD-only objective direction.
    test_id=9: LP Fourier-Motzkin, D-only objective direction.

    Information that we report (depending on the test and what we have at hand):
        - Vertices analysis: #total-number, #fractional-vertices, fine-grained-about-fractions: counts for each denominator (2, 3, ...).
        - (test_id=1) Hyperplanes: #hyper-planes, #total-hyperplanes
        - (test_id=1) integrality-gap: (best fractional-vertex  vs. best STT, for _some_ objective).
    """

    if output_log is not None: f = open(output_log,'w')
    else: f = None

    start_time = time.time()
    log_and_print(f,"[time=0]")

    searchTreeUtilities = SearchTreeUtilities(graph)
    n,dict_ids_to_var_number = searchTreeUtilities.n,searchTreeUtilities.dict_ids_to_var_number
    n_vars = len(dict_ids_to_var_number)
    coordinates_X = sorted([dict_ids_to_var_number[(i,j)]-1 for i in range(1,n+1) for j in range(1,n+1) if j != i]) # -1 because dict reserves 0 for the free coefficient.
    coordinates_D = sorted([dict_ids_to_var_number[i]-1 for i in range(1,n+1)]) # -1 because dict reserves 0 for the free coefficient.

    if 1 in tests_to_run:
        maxIter = (None if n <= 7 else 1) # Cap to a single iteration for graphs with n nodes, to side-step sage's memory-allocation-exception.
        new_vertices,h_counts = enrich_D_space_vertices(searchTreeUtilities,debugPrintEnrichmentFunction,maxIteration=maxIter)
        log_and_print(f,"[time=%3.3f] (enriched)"%(time.time()-start_time))
        
        all_stts = searchTreeUtilities.get_all_search_trees()
        all_vertices = set(all_stts[:])
        integrality_gap = 1
        for i in new_vertices.keys():
            for (vertex,direction,lp_value) in new_vertices[i]:
                all_vertices.add(vertex)
                cost_solution = scalar_product(direction,vertex)
                if i == 1: # iteration=1, then all the facets are due to STTs, and we can short-cut.
                    cost_stt = lp_value
                else: # In this case we are no longer sure that the facet is due to STTs, so we check all of them. (Effectively, we don't have iterations above 1, so this never gets executed.
                    bestSTT = find_best_search_tree(direction, searchTreeUtilities)
                    cost_stt = scalar_product(direction,bestSTT)
                integrality_gap = max(1.*cost_stt/cost_solution , integrality_gap)

        _,_,_,_,vertex_report_string = vertices_statistics(all_vertices, len(all_stts))
        log_and_print(f,"[time=%3.3f] (vertex statistics)"%(time.time()-start_time))
        
        hyperplanes_stt = h_counts[1] # The number of hyperplanes tested in the first iteration. Equivalent to: 'Polyhedron(vertices = all_stts, rays = generate_positive_rays(n)).n_Hrepresentation()'
        hyperplanes_all = max(h_counts.values()) # The number of hyperplanes tested in the final iteration. Equivalent to (memory-allocation exception for n=8 graphs): 'hyperplanes_all = Polyhedron(vertices = all_vertices, rays = generate_positive_rays(n)).n_Hrepresentation()'
            
        log_and_print(f,"[time=%3.3f] (H-count) "%(time.time()-start_time))
        log_and_print(f,"\n\n\nTestID-1")
        log_and_print(f,"Graph: size=%d , edges=%s"%(searchTreeUtilities.n,searchTreeUtilities.G.edges()))
        log_and_print(f,"integrality gap: %3.5f"%(integrality_gap))
        log_and_print(f,vertex_report_string)
        log_and_print(f,"hyperplanes count: all/stt-only: %d %d"%(hyperplanes_all,hyperplanes_stt))
        if len(new_vertices) == 0:
            log_and_print(f,"NO enriched vertices fine-grained.")
        else:
            log_and_print(f,"enriched vertices fine-grained:")
            for i in range(1,max(new_vertices.keys())+1):
                log_and_print(f,"... iteration=%d: +%d: %s"%(i,len(new_vertices[i]),new_vertices[i]))
        log_and_print(f,"[time=%3.3f] (Level-1 done)"%(time.time()-start_time))

    for test_id in [2,3]:
        if test_id not in tests_to_run: continue
        
        if test_id == 2:
            modes_list = modes_vanilla
        else: # test_id == 3
            modes_list = modes_noZ
        
        inequalities,equalities,bounds = construct_constraints_primal(searchTreeUtilities,modes_list)
        assert len(equalities) == 0
        p = Polyhedron(ieqs = inequalities + bounds, eqns = equalities)
        n_hyperplanes = p.n_Hrepresentation()
        log_and_print(f,"[time=%3.3f] (H-count)"%(time.time()-start_time))

        all_stts = searchTreeUtilities.get_all_search_trees()
        all_vertices = [v for v in p.Vrepresentation() if v.is_vertex()] # collect all the vertices, skip the rays.
        special_coordinates = [dict_ids_to_var_number[i]-1 for i in range(1,n+1)]
        _,_,_,_,vertex_report_string = vertices_statistics(all_vertices,len(all_stts))
        log_and_print(f,"[time=%3.3f] (V-stats)"%(time.time()-start_time))
        log_and_print(f,"\n\n\nTestID-%d"%test_id)
        log_and_print(f,"Graph: size=%d , edges=%s"%(searchTreeUtilities.n,searchTreeUtilities.G.edges()))
        log_and_print(f,vertex_report_string)
        log_and_print(f,"hyperplanes count: %d"%(n_hyperplanes))
        log_and_print(f,"[time=%3.3f] (TestID-%d done)"%(time.time()-start_time,test_id))
 
    for test_id in [4,5,6,7,8,9]: # These are sampling versions of test_id 2,3, when we do not have anough time/memory to exhaust the polytope.
        if test_id not in tests_to_run: continue

        if test_id in [4,5,6]:   modes_list = modes_vanilla
        elif test_id in [7,8,9]: modes_list = modes_noZ
        else: raise Exception("unexpected test id: %d"%test_id)
        
        max_rand = 100000    
        collected_vertices_D = set()
        collected_vertices_XD = set()
        collected_vertices_XZD = set()

        inequalities,equalities,bounds = construct_constraints_primal(searchTreeUtilities,modes_list)
        assert len(equalities) == 0
        inequalities_LP = inequalities + bounds # The bounds 'var >= 0' are also inequalities.

        for i in range(sampling_steps):
            random.seed(i) # seed each step so that it would be easier to reproduce each test independently (instead of re-generating all the random calls).
            objective_vector_of_LP = [random.randint(0,max_rand) for i in range(n_vars)] # No need to normalize the vectors or the coordinates.

            # zero-out some of the coordinates.
            if test_id in [4,7]: # all coordinates can be non-zero
                pass
            elif test_id in [5,8]: # zero Z coordinates
                for coord in range(n_vars):
                    if coord not in coordinates_X+coordinates_D: objective_vector_of_LP[coord] = 0
            elif test_id in [6,9]: # zero X,Z coordinates, keep only D-objective.
                for coord in range(n_vars):    
                    if coord not in coordinates_D: objective_vector_of_LP[coord] = 0
            else:
                raise Exception("unexpected test id: %d"%test_id)
            
            result_as_dict = solve_LP(objective_vector_of_LP,inequalities_LP)
            vec = clean_vector([result_as_dict[i] for i in result_as_dict])

            # Collect vectors, full coordinates or partial.
            vec_X_D = [vec[i] for i in sorted(coordinates_X + coordinates_D)]
            vec_D = [vec[i] for i in sorted(coordinates_D)]
            collected_vertices_XZD.add(tuple(vec))
            collected_vertices_XD.add(tuple(vec_X_D))
            collected_vertices_D.add(tuple(vec_D))

            if reportPartialIntegerVertices:
                if is_integer_vector(vec_D) and not is_integer_vector(vec):
                    log_and_print(f,"Partial-int Vertex (intXZD=%s | intXD=%s | intD=%s). D=%s, XZD=%s"%(is_integer_vector(vec),is_integer_vector(vec_X_D),is_integer_vector(vec_D),str(vec_D),str(vec)))
                    print_XZD_solution(vec, n, dict_ids_to_var_number, formatter_function = _formatter_compact, alsoPrintZ = False)
                    print ("LP Direction:",objective_vector_of_LP)

            if modes_list == modes_noZ: # Report fractional vertices that are not half-integer, in the case where we replaced Z variables (having Z seems to create many extra fractional variables).
                if not is_integer_vector([2*i for i in vec_X_D]):
                    log_and_print(f,"Small-fractions Vertex.")
                    print_XZD_solution(vec, n, dict_ids_to_var_number, formatter_function = _formatter_compact, alsoPrintZ = False)
                    print ("LP Direction:",objective_vector_of_LP)

        _,_,_,_,vertex_report_string_D = vertices_statistics(collected_vertices_D,None)
        _,_,_,_,vertex_report_string_XD = vertices_statistics(collected_vertices_XD,None)
        _,_,_,_,vertex_report_string_XZD = vertices_statistics(collected_vertices_XZD,None)
        log_and_print(f,"[time=%3.3f] (V-stats [x3])"%(time.time()-start_time))
        log_and_print(f,"\n\n\nTestId-%d"%(test_id))
        log_and_print(f,"Graph: size=%d , edges=%s"%(searchTreeUtilities.n,searchTreeUtilities.G.edges()))
        log_and_print(f,"XZD-space vertex-analysis:")
        log_and_print(f,vertex_report_string_XZD)
        log_and_print(f,"XD-space vertex-analysis:")
        log_and_print(f,vertex_report_string_XD)
        log_and_print(f,"D-space vertex-analysis:")
        log_and_print(f,vertex_report_string_D)

    if f is not None: f.close()

def analyze_bulk_small_graphs(n_range = range(3,9),log_dir=LOG_DIR):
    """ A 'wrapper' function to analyze each of the small graphs with n<=8 nodes. """
    for n in n_range:
        for j in range(len(ALL_SMALL_GRAPHS[n])):
            tests_list = [1]
            if n <= 5: tests_list += [2,3]
            else:      tests_list += [4,5,6,7,8,9]
            log_full_name = (None if log_dir is None else log_dir + os.path.sep + "graph_%d_%d_%d.txt"%(n,j,int(time.time())))
            exhaustive_analysis(ALL_SMALL_GRAPHS[n][j],tests_list,log_full_name,sampling_steps = 1000)

def analyze_path_graphs(n_values = range(6,16),log_dir=LOG_DIR):
    """ A 'wrapper' function to analyze path graphs. """
    steps_per_n = {9: 400, 10: 200, 11: 100, 12: 50}
    for n in n_values:
        graph_linear = make_graph_path(n)
        if n < 9:     steps = 1000 # small graphs, can sample many
        elif n < 12:  steps = steps_per_n[n]
        else:         steps = 50 # large graph, sample few
        tests_list = [4,5,6,7,8,9]
        log_full_name = (None if log_dir is None else log_dir + os.path.sep + "graph_%d_line_%d.txt"%(n,int(time.time())))
        exhaustive_analysis(graph_linear,tests_list,log_full_name,sampling_steps = steps)

def analyze_enrichment_only_for_graphs(graph_ids=None,log_dir=LOG_DIR):
    """ A 'wrapper' function to run the enrichment test for every specified graph.
    By default, the test only revisits the graphs where we already identified non-integer vertices so that we may rerun additional iterations or compute extra info, without checking un-interesting graphs. """
    if graph_ids is None: graph_ids = PRIMARY_DIRECTIONS.keys()
    for n,i in graph_ids:
        graph = ALL_SMALL_GRAPHS[n][i]
        tests_list = [1]
        log_full_name = (None if log_dir is None else log_dir + os.path.sep + "enriching_%d_%d_%d.txt"%(n,i,int(time.time())))
        exhaustive_analysis(graph,tests_list,log_full_name)

################################
### Analysis Functions (end) ###
################################    


################################################
### Functions to Generate Paper Data (start) ###
################################################

def table1_table6_generation(nMaxGeneration=5,genLogU73=False):
    # nMaxGeneration=5 takes ~10 seconds.
    # For larger options, it is recommended to generate the logs once and reuse them if necessary:
    #   - nMaxGeneration=6 takes ~9-10 minutes.
    #   - genLogU73=True   takes   ~15 minutes.
    #   - nMaxGeneration=8 will take days to complete.
    assert nMaxGeneration <= 8 # more than 8 is infeasible.
    
    print ("# Note1: Generating ALL the data is slow. Therefore, by default this example only generates the rows for n<=5 and U(7,3). #")
    print ("# Note2: Tables 1+6 are generated from the logs without 'False Facets' and 'Frac Vs Classes' columns. These are analyzed separately. #")
    LOG_DIR = "/mnt/c/temp/"

    print ("#######################################################")
    print ("###   Generating Logs... If Applicable...           ###")
    print ("#######################################################")
    if nMaxGeneration < 7 and genLogU73:
        exhaustive_analysis(ALL_SMALL_GRAPHS[7][3], tests_to_run=[1,4,5,6,7,8,9], output_log = LOG_DIR + os.path.sep + "graph_7_3_%d.txt"%(int(time.time())), sampling_steps = 1000)

    ns = [i for i in range(3,nMaxGeneration+1)]
    if len(ns) >= 1:
        analyze_bulk_small_graphs(ns, log_dir=LOG_DIR)
        
    print ("#######################################################")
    print ("###   Parsing Logs to Generate Table Information    ###")
    print ("#######################################################")
    all_logs = [path for path in glob.glob(LOG_DIR + os.path.sep + "graph_*") if "_line_" not in path]
    print (len(all_logs))
    for log in sorted(all_logs):
        z = parse_log(log,MODE_GRAPH_INFOS)
        print ("\\hline")
    print ("\n\n"+"#"*30+"\n\n")

def table1_table6_extra_columns():
    assert set(NON_INT_VERTICES.keys()) == set(NON_INT_TOPOLOGY_NAMES)
    assert set(PRIMARY_DIRECTIONS.keys()) == set(NON_INT_TOPOLOGY_NAMES)
    DEDUPED = dedup_automorphism_vertices(vertex_dict = NON_INT_VERTICES)
    print ("Topology & Primary Directions & Frac Vs & Frac Vs Classes")
    for key in sorted(NON_INT_TOPOLOGY_NAMES):
        print (key,"&",len(PRIMARY_DIRECTIONS[key]),"&",len(set(NON_INT_VERTICES[key])),"&",len(DEDUPED[key]))

def table2_info_integrality_gap():
    """ Compute and print in latex-source format the integrality gap information of chosen (fixed) directions. """
    for n,i in INT_GAP_DIRECTIONS:
        sttutil = SearchTreeUtilities(ALL_SMALL_GRAPHS[n][i])
        d = INT_GAP_DIRECTIONS[(n,i)]
        try:
            lp_opt,stt_opt,_,_ = compute_gaps_or_vectors_for_direction(d, sttutil, returnVectors=True, returnLPResultAsIs=False)
            lp_opt_str = str(scalar_product(d,lp_opt))
        except: # In case we run python instead of sage, skip the LP solver and print only some of the information.
            stt_opt = scalar_product_find_smallest(d,sttutil.get_all_search_trees())
            lp_opt_str = "??????"
        print ((n,i),"&",d,"&",lp_opt_str,"&",scalar_product(d,stt_opt))

def table3_info_approximation_ratio():
    """ Compute and print in latex-source format the approximation ratio information of chosen (fixed) directions. """
    for mapper in [ROUND_GAP_DIRECTIONS_BC,ROUND_GAP_DIRECTIONS_WC,{(8,4): (6.5,3,0,5,0,18,4,5)}]: # The last dictionary is one more extra explicit entry.
        for n,i in mapper:
            _approximation_output_helper((n,i),mapper[(n,i)], SearchTreeUtilities(ALL_SMALL_GRAPHS[n][i]))

def table5_generation(nMax=8,generateLogs=False):
    # The logs take minutes to generate (longer the larger n is), so it is better to one-time generate them.
    print ("# Note: Generating ALL the data is slow. Thus by default we only generate the first few path topologies. #")
    LOG_DIR = "/mnt/c/temp/"

    print ("#######################################################")
    print ("###   Generating Logs... If Applicable...           ###")
    print ("#######################################################")
    if generateLogs: analyze_path_graphs(n_values = range(6,nMax+1),log_dir=LOG_DIR)
    
    print ("#######################################################")
    print ("###   Parsing Logs to Generate Table Information    ###")
    print ("#######################################################")
    all_logs = glob.glob(LOG_DIR + os.path.sep + "graph_*line*.txt")
    for log in sorted(all_logs):
        z = parse_log(log,MODE_LINE)
        print ("\\hline")
    print ("\n\n"+"#"*30+"\n\n")

def table7_generation():
    for n in range(3,9):
        for i,G in enumerate(ALL_SMALL_GRAPHS[n]):
            graph_name = (n,i)
            edges = sorted(G.edges())
            diameter = networkx.diameter(networkx.Graph(edges)) # The package computes diameter in edges (weighted/unweighted), we need it in vertices.
            print ("%s & %d & %s \\\\"%(graph_name,diameter,edges))

def figure3_print_main_vertex():
    """ Computes and prints the 'main' vertex that we use in the paper. """
    direction = (3,2,0,2,3,3,10)
    stu = SearchTreeUtilities(ALL_SMALL_GRAPHS[7][3])

    inequalities,equalities,bounds = construct_constraints_primal(stu, modes_vanilla)
    inequalities_LP = inequalities + bounds # The bounds 'var >= 0' are also inequalities.

    objective_vector_of_LP = [0] * len(stu.dict_ids_to_var_number)
    for i in range(1,stu.n+1):
        objective_vector_of_LP[stu.dict_ids_to_var_number[i] - 1] = direction[i-1] # Put it in the coordinates that corresponds to the depth vector D.
    result_as_dict = solve_LP(objective_vector_of_LP,inequalities_LP)
    XZD_vector = clean_vector([result_as_dict[i] for i in result_as_dict])
    print_XZD_solution(XZD_vector, stu.n, stu.dict_ids_to_var_number, formatter_function = _formatter_compact, alsoPrintZ = True)

def figure5_print_3D_examples(subfigure='a',printFacets=True):
    assert subfigure in ['a','b']
    print ("# Note: visualization of the plot may not appear. #")
    print ("# If it does not, inline the lines of this function in 'https://sagecell.sagemath.org/'. #")
    B = [[0,0,1],[0,1,0],[1,0,0]]
    C = [[0,1,2],[0,2,1],[1,0,2],[2,0,1],[1,2,0],[2,1,0],[0,0,4],[0,4,0],[4,0,0]]
    if subfigure=='b': C += [[0.5,0.5,0.5]]
    p = Polyhedron(vertices = C, rays = B)
    if printFacets:
        for i,h in enumerate(p.Hrepresentation()): print (i,h)
    p.plot(polygon='rainbow', alpha=0.5, size=50) # size=50 of vertices

def print_primary_directions_U73_up_to_symmetries(): # Relevant to the paper just before Definition 2.5 (page ~11).
    def _swap_legs12(v): return v[:5][::-1] + v[5:]
    def _swap_legs13(v): return [v[6],v[5]] + v[2:5]+ [v[1],v[0]]
        
    directions = set(PRIMARY_DIRECTIONS[(7,3)])
    uniques = []
    while len(directions) > 0:
        # Remove all (up to) 6 permutations of d. Count symmetries.
        d1 = list(directions.pop())  # legs order 1,2,3
        d2 = _swap_legs12(d1) # legs order 2,1,3
        d3 = _swap_legs13(d1) # legs order 3,2,1
        d4 = _swap_legs13(d2) # legs order 3,1,2
        d5 = _swap_legs12(d3) # legs order 2,3,1
        d6 = _swap_legs12(d4) # legs order 1,3,2
        count = 1
        for d in [d2,d3,d4,d5,d6]:
            if tuple(d) in directions:
                directions.remove(tuple(d))
                count += 1
        uniques += [(d1,count)]
    for d,c in sorted(uniques):
        print ("Direction: %25s | Symmetry-count: %d"%(str(d),c))

def remark_3_3_min_depth_is_1():
    print ("Vertices with minimum D variable >= 1, per topology:")
    for key in NON_INT_VERTICES_REDUCED:
        vertices = [v for v in NON_INT_VERTICES_REDUCED[key] if min(v)>= 1]
        if len(vertices) >= 1:
            print ("~~~ Topology %s ~~~"%(str(key)))
            for v in vertices: print ("... %s"%str(v))

def example_2_7_partially_integer_vertex():
    searchTreeUtilities = SearchTreeUtilities(ALL_SMALL_GRAPHS[6][0])
    inequalities,equalities,bounds = construct_constraints_primal(searchTreeUtilities,[]) # vanilla LP, no special mods.
    assert len(equalities) == 0

    inequalities_LP = inequalities + bounds # The bounds 'var >= 0' are also inequalities.		
    objective_vector_of_LP = [0, 5, 5, 1, 2, 3, 1, 4, 1, 1, 3, 3, 1, 4, 2, 2, 3, 5, 3, 1, 1, 3, 5, 4, 2, 2, 6, 0, 2, 1, 5, 3, 3, 1, 5, 4, 4, 5, 3, 2, 1, 6, 3, 5, 2, 3, 4, 5, 3, 2, 2, 1, 0, 3, 5, 2] # No need to normalize the vector.
    result_as_dict = solve_LP(objective_vector_of_LP,inequalities_LP)
    
    vec = clean_vector([result_as_dict[i] for i in result_as_dict])
    vecD = get_D_vector_from_LP_solution(vec,searchTreeUtilities.dict_ids_to_var_number,searchTreeUtilities.n)
    assert is_integer_vector(vecD) and not is_integer_vector(vec)

    print ("Objective function direction:",objective_vector_of_LP)
    print_XZD_solution(vec, searchTreeUtilities.n, searchTreeUtilities.dict_ids_to_var_number, formatter_function = _formatter_compact, alsoPrintZ = True)

def section5_vertex_statistics_fractional_vertices_line_and_T_topologies():
    """ Relevant to the paper in the discussion that follows Remark 5.2 (page ~30), and to Section 5.3 when discussing the topology U(5,1). """
    for key in [(5,0),(5,1)]: # Path and 'T' topologies, respectively
        print ("Topology:",key)
        print ("... Vanilla (with Z, no monotonicity-constraints):")
        enumerate_all_vertices(key,withMonotonicity=False,withZ=True)
        for addMonotonicityConstraints in [False,True]:
            print ("... No Z variables. Added monotonicity constraints?",addMonotonicityConstraints)
            enumerate_all_vertices(key,addMonotonicityConstraints,withZ=False)

def section5_3_vertices_versus_monotonicity_constraints():
    print ("""Note: we analyze for each depths-vector a single full XZD-vector. However, it turns out that sometimes multiple XZD-vectors have the same D-vector (projection).
In such cases, validation/invalidation result for one extension does not guarantee the same result for the others. """)
           
    for key in NON_INT_TOPOLOGY_NAMES:
            print ("Topology %s, revised extra-vertices:"%(str(key)),end=" ")
            stu = SearchTreeUtilities(ALL_SMALL_GRAPHS[key[0]][key[1]])
            vertices = [i[1] for i in NON_INT_VERTICES_REDUCED_WHOLE_REPRESENTATION[key]]
            c = [0,0]
            for v in vertices:
                    isGood = True
                    Xpairs = extract_X_coordinates_as_dict_of_pairs(v, stu.n, stu.dict_ids_to_var_number)
                    for i in range(1,stu.n+1):
                            for j in range(1,stu.n+1):
                                    for k in range(1,stu.n+1):
                                            if i==j or k == i or k == j: continue
                                            if k in stu.betweenNodes(i,j):
                                                    isGood = isGood and (Xpairs[(i,k)] >= Xpairs[(i,j)]) and (Xpairs[(j,k)] >= Xpairs[(j,i)])
                    if isGood: c[0] += 1
                    else:      c[1] += 1
            print ("survived/invalidated = ",c) # Most survive. Total of 22 invalidations: 12 for (8,4), 9 for (8,12), 1 for (8,13).

def _approximation_output_helper(ni_key,d,sttutil):
    """ Given a direction 'd' and a SearchTreeUtitilies 'sttutil', compute the best and worst STT-approximation in direction 'd'. Print the computed ratios. """
    def _printable_to_ratio(x,y): return "/".join(["%d"%(round(a)) if abs(a-round(a))<NUMERIC_ERROR else "%2.5f"%(a) for a in [x,y]])
    
    lp_opt,stt_opt,stt_bc,stt_wc = compute_gaps_or_vectors_for_direction(d, sttutil, returnVectors=True, returnLPResultAsIs=False)
    cost_opt = convert_value_to_cost(scalar_product(d,stt_opt),d)
    cost_bc  = convert_value_to_cost(scalar_product(d,stt_bc ),d)
    cost_wc  = convert_value_to_cost(scalar_product(d,stt_wc ),d)
    sumd = sum(d)
    print (
        ni_key,"&",
        d,"&",
        _printable_to_ratio(cost_opt*sumd,sumd),"&",
        _printable_to_ratio(cost_bc*sumd,sumd),"&",
        _printable_to_ratio(cost_wc*sumd,sumd),"&",
        round(1.0*cost_bc/cost_opt,4),"&",
        round(1.0*cost_wc/cost_opt,4),"\\\\",
    )
    print ("\\hline")

def section5_4_XD_to_D_collisions(subset_topologies = None): # Takes ~90 seconds.
    """ For each primary direction, solve the Z-less LP to find an (X,D)-vertex. Then check for collisions when projected to D-space. """
    if subset_topologies is None: subset_topologies = NON_INT_TOPOLOGY_NAMES
    
    map_Dvec_to_Xvec = {}
    for key in subset_topologies:
        n,idx = key
        stu = SearchTreeUtilities(ALL_SMALL_GRAPHS[n][idx])
        map_Dvec_to_Xvec[key] = {}

        # Same constraints every time, so compute them once.
        inequalities,equalities,bounds = construct_constraints_primal(stu, modes_noZ)
        inequalities_LP = inequalities + bounds # The bounds 'var >= 0' are also inequalities.

        # Solve for every primary direction and find (X,D).
        for direction in PRIMARY_DIRECTIONS[key]:
            objective_vector_of_LP = [0] * len(stu.dict_ids_to_var_number)
            for i in range(1,stu.n+1):
                objective_vector_of_LP[stu.dict_ids_to_var_number[i] - 1] = direction[i-1] # Put it in the coordinates that corresponds to the depth vector D.

            result_as_dict = solve_LP(objective_vector_of_LP,inequalities_LP)
            XZD_vector = clean_vector([result_as_dict[i] for i in result_as_dict])

            Dvec = tuple(get_D_vector_from_LP_solution(XZD_vector,stu.dict_ids_to_var_number,stu.n))
            Xmat = get_X_matrix_from_LP_solution(XZD_vector,stu.dict_ids_to_var_number,stu.n)
            
            if Dvec not in map_Dvec_to_Xvec[key]: map_Dvec_to_Xvec[key][Dvec] = []
            map_Dvec_to_Xvec[key][Dvec] += [(Xmat,direction)]

        # Now check for collisions of (X,D) when projected to D.
        print ("=== Topology: %s ==="%(str(key)))
        for Dvec in map_Dvec_to_Xvec[key]:
            justXall = [i[0] for i in map_Dvec_to_Xvec[key][Dvec]]
            justXuniques = sorted(set(justXall))
            if len(justXuniques) > 1:
                Diff12 = [[justXuniques[0][i][j]-justXuniques[1][i][j] for j in range(n)] for i in range(n)] # Also print the diff of the first two Xs.
                
                print ("%d-way collision:"%(len(justXuniques)))
                for i in range(n):
                    print(" | ".join([str(X[i]) for X in (justXuniques + [Diff12])]).replace("0.5","h").replace("-h","m").replace("0.0","0")) # Print all matrices side-to-side. "h" for half.
                counts = []
                example_direction = []
                for X in justXuniques:
                    example_direction += [ map_Dvec_to_Xvec[key][Dvec][justXall.index(X)][1] ]
                    counts += [justXall.count(X)]
                print ("normal counts per X:",counts)
                print ("representative normal per X:",example_direction)

##############################################
### Functions to Generate Paper Data (end) ###
##############################################


###########################################
### Additional Analysis - Misc. (start) ###
###########################################

def optimize_direction_to_maximize_gap(n,i,direction,isWorstCaseGap=True,debugPrint=False):
    """ Given a direction, naively check small variations in each coordinate, repeatedly, to increase the approximation ratio.
    # Example: >>> optimize_direction_to_maximize_gap(8,4,(6,3,0,5,0,18,4,5),isWorstCaseGap=True)
    # [result, cleaned:] (8, 4) & [6.5, 3, 0, 5, 0, 18, 4, 5] & 190/83 & 191/83 & 263/83 & 1.0053 & 1.3842 \\ """
    sttutil = SearchTreeUtilities(ALL_SMALL_GRAPHS[n][i])
    best_ratio = 1
    current_d = direction[:]
    step_size = 0.1

    for step in range(100):
        isBetter=False
        for k in range(n): # Why in order, only increase, and step-size=0.1? Because it works.
            d = [current_d[i]+(step_size if i == k else 0) for i in range(n)]
            lp_opt,stt_opt,stt_bc,stt_wc = compute_gaps_or_vectors_for_direction(d, sttutil, returnVectors=True, returnLPResultAsIs=False)
            cost_opt = convert_value_to_cost(scalar_product(d,stt_opt),d)
            stt = (stt_wc if isWorstCaseGap else stt_bc)
            cost_stt = convert_value_to_cost(scalar_product(d,stt),d)
            new_ratio = 1.0*cost_stt/cost_opt
            if new_ratio > best_ratio:
                if debugPrint: print ("old: %2.5f / new: %2.5f / direction=%s"%(best_ratio,new_ratio,d))
                current_d = d
                best_ratio = new_ratio
                isBetter=True
                break
        if not isBetter: #no coordinate improvement
            if step_size > 10**-6: step_size /= 10. # refine
            else: break
    d = current_d
    print ("optimization done. Resulting direction=",d)
    _approximation_output_helper((n,i),d,sttutil)

def test_print_L_infinifty_ditance_from_STTaverages(graph_ids = None):
    """ Check how close we can get to each non-integer vertex as an average of (at most) 2 STTs. The distance is in L-infinity norm.

    Note: most vertices are at distance 0.5, with three exceptions for graph (8,4) whose print-output is (up to permutation by automorphism):
    distance: 1.0 vertex: (1.5, 2, 4.5, 1.5, 0.5, 3, 2.5, 2.5)  | combination: ([(0, 1, 2, 4, 3, 4, 4, 3), (2, 4, 5, 1, 0, 1, 3, 4)], [0.5, 0.5])
    distance: 1.0 vertex: (2.5, 2.5, 4.5, 2, 1.5, 4, 1.5, 0.5)  | combination: ([(0, 1, 5, 2, 3, 4, 4, 3), (3, 5, 6, 4, 2, 3, 1, 0)], [0.5, 0.5])
    distance: 1.0 vertex: (2, 2, 4.5, 1.5, 0.5, 3, 2, 2)        | combination: ([(0, 1, 2, 4, 3, 4, 4, 3), (3, 4, 5, 1, 0, 1, 2, 3)], [0.5, 0.5]) """
    
    def _distance(v,trees,weights):
        d = list(v)
        for t in range(len(trees)):
            for idx in range(len(d)):
                d[idx] -= trees[t][idx]*weights[t]
        return max(map(abs,d))

    if graph_ids is None: graph_ids = NON_INT_VERTICES_REDUCED.keys()
    for key in graph_ids:
        print ("=== === === BEGIN NEW GRAPH: %s === === ==="%str(key))
        n,i = key
        all_stts = SearchTreeUtilities(ALL_SMALL_GRAPHS[n][i]).get_all_search_trees()
        for vertex in NON_INT_VERTICES_REDUCED[key]:
            best = (10**6,None,None) # distance, trees, weights
            for t1 in all_stts:
                for t2 in all_stts:
                    tlist,wlist = [t1,t2],[0.5,0.5] # If t1=t2 then we test a STT instead of an average of two.
                    dd = _distance(vertex,tlist,wlist)
                    if dd < best[0]: best = (dd,tlist,wlist)
            print ("distance:",best[0],"vertex:",vertex," | combination:",best[1:])

def test_rounding_caused_by_lifting():
    """ For each non-integer vertex, check the effect incurred by rooting each of the possible nodes,
    and see which is closest in L-infinity distance to the original when we compare the depth vectors. We tie-break in favor of having fewest coordinates that equal the distance.

    It may be 0 (ideal), at worst it is 1/2 (proven). Therefore it is interesting to check how fewest (1/2)-increase we can get by picking the best node to lift to the root.
    In most cases, there was only one +(1/2) node. However even with out small graphs, there are examples for more than that: 4 cases with a pair of +1/2 in vertices of (8,4), and one case of a triplet for (8,13):
    (Graph = (8,13)): Distance=0.500 | Count= 3 (lifted root=2) [delta=[-0.5, -2.0, -0.5, 0.5, 0.5, 0.0, -0.5, 0.5],before=[1.5, 2.0, 3.5, 2.0, 1.0, 1.0, 3.5, 1.5],lifted=[1, 0, 3.0, 2.5, 1.5, 1, 3.0, 2.0]] """
    
    for key in NON_INT_VERTICES_REDUCED_WHOLE_REPRESENTATION:
        print ("=== === === BEGIN NEW GRAPH: %s === === ==="%str(key))
        n,iii = key
        for Ds,XZDs in NON_INT_VERTICES_REDUCED_WHOLE_REPRESENTATION[key]:
            sttutil = SearchTreeUtilities(ALL_SMALL_GRAPHS[n][iii])
            X = extract_X_coordinates_as_dict_of_pairs(XZDs,n,sttutil.dict_ids_to_var_number)

            best = (n,n,None,None) # distance, max-count, depth-vector pre-lifting, depth-vector post-lifting
            for newRoot in range(1,n+1):
                newX = sttutil.lifting(X,newRoot)
                D_X,D_newX,D_delta = [0]*(n+1),[0]*(n+1),[0]*(n+1) # with sentinel for index 0
                for i in range(1,n+1):
                    for j in range(1,n+1):
                        if i != j:
                            D_X[i] += X[(j,i)]
                            D_newX[i] += newX[(j,i)]
                    D_delta[i] = D_newX[i] - D_X[i]
                deltaMax = max(D_delta)
                deltaCount = D_delta[1:].count(deltaMax)
                if deltaMax < best[0] or (deltaMax == best[0] and deltaCount < best[1]):
                    best = (deltaMax,deltaCount,newRoot,(D_delta[1:],D_X[1:],D_newX[1:])) # keep D_xx without sentinels
            assert best[0] <= 0.5 # Guaranteed by analysis.
            if best[0]>0 and best[1]>1: # Sieves only the "interesting" cases.
                print ((".........."+"   "*best[1] if best[0]>0 else "") + "Distance=%2.3f | Count=%2d (lifted root=%d) [delta=%s,before=%s,lifted=%s]"%(best[0],best[1],best[2],best[3][0],best[3][1],best[3][2]))

def test_integrality_gap_and_approximation_ratios_exhaustive_info(graph_ids = None,log_dir=LOG_DIR):
    """ This function combines two exhaustive tests for maximizing the integrality gap and approximation ratios. """
    compute_integrality_and_approximation_gap_for_graphs(log_dir,graph_ids)
    gaps_maximize_with_LP(log_dir,graph_ids)

#########################################
### Additional Analysis - Misc. (end) ###
#########################################


###########################
### "main" part (start) ###
###########################
# Calling each of the data-generations / tests.
# In general, we omit parameters that result in a long running time, one can tailor specific calls to compute heavier results.

def example_of_all_data_calls(generateLogs=False):
    """ This function gathers all the calls that serve as examples on how to generate the data throughout the paper.
    Since some computations are *very* heavy, in some cases we only give a toy-example.
    As a concrete example, we do not generate the full data of Table6 here, only information up to Topologies of size n<=5, and the special topology of size 7. """
    # Figures
    figure3_print_main_vertex()
    figure5_print_3D_examples('a')
    figure5_print_3D_examples('b')

    # Tables
    table1_table6_generation(nMaxGeneration=5,genLogU73=generateLogs) # nMaxGeneration=5 takes ~10 seconds, genLogU73=True takes ~15 minutes.
    table1_table6_extra_columns() # Based mostly on the hard-coded pre-computed values.
    table2_info_integrality_gap() # Computes the gap for the (hardcoded) directions.
    table3_info_approximation_ratio() # Computes the gap for the (hardcoded) directions.
    table5_generation(nMax=9,generateLogs=generateLogs)
    table7_generation()

    # Additional data throughout the paper
    print_primary_directions_U73_up_to_symmetries()
    remark_3_3_min_depth_is_1()
    example_2_7_partially_integer_vertex()
    section5_vertex_statistics_fractional_vertices_line_and_T_topologies()
    section5_3_vertices_versus_monotonicity_constraints()
    section5_4_XD_to_D_collisions()
    
def example_of_extra_tests(runSlowTestToo=False):
    """ These are additional tests and analysis that may be of interest. The calls are only top-examples, as to not be too heavy. Adapt the calls individually as you please. """
    optimize_direction_to_maximize_gap(8,4,(6,3,0,5,0,18,4,5),isWorstCaseGap=True)
    test_print_L_infinifty_ditance_from_STTaverages(graph_ids = [(7,3)])
    test_rounding_caused_by_lifting()
    analyze_enrichment_only_for_graphs([(6,0)]) # (6,0) should yield no enrichment (in ~10-15 seconds). The following yield enrichment, but are much-much slower: (7,3) yields 2 iterations, (8,13) is capped at 1 iteration.
    if runSlowTestToo: # Very slow (~15 minutes), so not part of the "basic package".
        test_integrality_gap_and_approximation_ratios_exhaustive_info([(7,3)]) # Single graph with non-integer vertices; the others are too slow when solving for the WC-approximation.
    
#########################
### "main" part (end) ###
#########################




# --------------------------------------------------
# --------------------------------------------------

# If 'includeSlowParts = True' : takes 55-60 minutes of total running time.
# If 'includeSlowParts = False': takes ~2 minutes.
includeSlowParts = False

start = time.time()
print ("start...")
example_of_all_data_calls(generateLogs=includeSlowParts) # This call should take ~15-30 seconds, depending on the number of logs we parse.
print ("mid ",int(time.time()-start))
example_of_extra_tests(runSlowTestToo=includeSlowParts) # This call should take ~15-30 seconds.
print ("done",int(time.time()-start))

# --------------------------------------------------
# --------------------------------------------------


