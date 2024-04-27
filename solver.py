from belief_base import Belief

class Solver:
    def __init__(self):
        self.beliefs = [] # clauses must be in CNF, stored as a list of lists of tuples, were each tuple is a literal (is_positive, symbol)
    

    def add_belief(self, belief: Belief):
        '''
        Add belief (our format) to the solver database.
        '''
        self.beliefs.append(belief)


    def remove_belief(self, belief: Belief):
        self.beliefs.remove(belief)


    def check_clauses(self) -> bool:
        '''
        Method for checking if the clauses stored in solver beliefs database are entailed.
        
        Implemented methods:
        - Resolution

        return: True if the clauses are entailed, False otherwise
        '''
        return self.resolution()
        
        
    def resolution(self) -> bool:
        '''
        Check entailment using resolution.
        
        Sources used during implementation:
        https://www.geeksforgeeks.org/resolution-algorithm-in-artificial-intelligence/
        https://www.youtube.com/watch?v=PMm5Mat0MRA
        https://www.youtube.com/watch?v=SjEQNOV5FMk&t=189s
        '''
        from itertools import combinations
        
        clauses = []

        for belief in self.beliefs:
            for c in belief.clause:
                clauses.append(c)

        new_clauses = []

        while True:
            for clause1, clause2 in combinations(clauses, 2):
                resolvents = self.resolve_clauses(clause1, clause2)
                if [] in resolvents:
                    return True # Contradiction found
                new_clauses.extend(resolvents)
        
            if self.check_if_subset(new_clauses, clauses):
                return False

            # For every new clause that is not in the list of clauses, add it to this list
            for cl in new_clauses:
                if cl not in clauses:
                    clauses.append(cl)


    def resolve_clauses(self, clause1, clause2):
        '''
        Resolve two clauses.
        '''
        resolvents = []
        for el_1 in clause1:
            for el_2 in clause2:
                if el_1[1] == el_2[1] and el_1[0] != el_2[0]:
                    resolvents.append([x for x in clause1 if x != el_1] + [x for x in clause2 if x != el_2])
        return resolvents
        

    def check_if_subset(self, list1, list2):
        '''
        Check if list1 is a subset of list2.
        
        Note: lit1 and list2 contain lists of tuples.
        '''
        
        for item in list1:
            if item not in list2:
                return False
        return True
