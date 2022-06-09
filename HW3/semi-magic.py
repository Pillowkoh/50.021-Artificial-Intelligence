import pdb
from csp import *
from random import shuffle

def solve_semi_magic(algorithm=backtracking_search, **args):
    """ From CSP class in csp.py
        vars        A list of variables; each is atomic (e.g. int or string).
        domains     A dict of {var:[possible_value, ...]} entries.
        neighbors   A dict of {var:[var,...]} that for each variable lists
                    the other variables that participate in constraints.
        constraints A function f(A, a, B, b) that returns true if neighbors
                    A, B satisfy the constraint when they have values A=a, B=b
                    """
    # Use the variable names in the figure
    csp_vars = ['V%d'%d for d in range(1,10)]

    #########################################
    # Fill in these definitions

    csp_domains = {v:[1,2,3] for v in csp_vars}
    csp_neighbors = {
        "V1":["V2","V3","V4","V5","V7","V9"],
        "V2":["V1","V3","V5","V8"],
        "V3":["V1","V2","V6","V9"],
        "V4":["V1","V5","V6","V7"],
        "V5":["V1","V2","V4","V6","V8","V9"],
        "V6":["V3","V4","V5","V9"],
        "V7":["V1","V4","V8","V9"],
        "V8":["V2","V5","V7","V9"],
        "V9":["V1","V3","V5","V6","V7","V8"]
    }


    def csp_constraints(A, a, B, b):
        return a != b

    #########################################
    
    # define the CSP instance
    csp = CSP(csp_vars, csp_domains, csp_neighbors,
              csp_constraints)

    # run the specified algorithm to get an answer (or None)
    ans = algorithm(csp, **args)
    
    print('number of assignments', csp.nassigns)
    assign = csp.infer_assignment()
    if assign:
        for x in sorted(assign.items()):
            print(x)
    return csp


if __name__ == '__main__':
    # select_unassigned_variable
    variable_ordering = [first_unassigned_variable, mrv]

    # order_domain_values
    value_ordering = [unordered_domain_values, lcv]

    # inference
    inference = [no_inference, forward_checking, mac]

    for i in variable_ordering:
        for j in value_ordering:
            for k in inference:
                print(f'Variable ordering: {i.__name__},\nValue_ordering: {j.__name__},\nInference: {k.__name__}')
                solve_semi_magic(backtracking_search,
                                select_unassigned_variable = i,
                                order_domain_values = j,
                                inference=k)
                print("\n")


# Observations: After running the python programme multiple times, the number of assignments for the different solution 
#               algorithms are generally consistent with 9 assignments each. However, there are two different combination
#               of assignments which can give rise to an increased number of assignments, namely: 1) Backtracking-search
#               with minimum-remaining-values (mrv) heuristic, unordered domain values and no inference; 2) Backtracking
#               search with mrv heuristic, least-constraining-values (lcv) heuristic and no inference. The common features
#               of these two solution algorithms are that they both use the mrv heuristic and do not perform inferencence.
#               As the mrv heuristic causes the solution algorithms to assign variables with the minimum remaining values 
#               first, the assigned value maybe incorrect since there is no inference performed to ensure consistency with 
#               the future states. Therefore, the lack of inference, coupled with the mrv heuristic may cause the solution 
#               algorithms to assign variables incorrectly, thus resulting in backtracking and increase the total number
#               of assignments to arrive at the final goal state.
