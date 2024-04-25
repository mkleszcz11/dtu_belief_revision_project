class Solver:
    def __init__(self):
        self.clauses = [] # clauses must be in CNF, stored as a list of lists of tuples, were each tuple is a literal (is_positive, symbol)
    
    def add_clause(self, clause):
        self.clauses.append(clause)
        
    def check_clauses(self) -> bool:
        '''
        Method for checking if the clauses are entailed.
        
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
        for clause in self.clauses:
            for c in clause:
                clauses.append(c)

        new_clauses = []

        while True:
            for clause1, clause2 in combinations(clauses, 2):
                resolvents = self.resolve(clause1, clause2)
                if [] in resolvents:
                    return True
                new_clauses.extend(resolvents)
        
            if self.check_if_subset(new_clauses, clauses):
                return False

            clauses.extend(new_clauses) # TODO Optimaze to add only unique clauses


    def resolve(self, clause1, clause2):
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
