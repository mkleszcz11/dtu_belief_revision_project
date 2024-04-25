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

        # A set to keep track of all unique resolvents to avoid infinite loops.
        unique_resolvents = set()
        
        while True:
            new = []
            # Use combinations to ensure each pair is only considered once.
            for clause1, clause2 in combinations(self.clauses, 2):
                resolvent = self.resolve(clause1, clause2)
                for clause in resolvent:
                    # Normalize each clause by sorting (to avoid different orders creating 'new' clauses)
                    normalized_clause = tuple(sorted(clause))
                    if normalized_clause == tuple():
                        return True  # Empty clause found: contradiction!
                    if normalized_clause not in unique_resolvents:
                        unique_resolvents.add(normalized_clause)
                        new.append(clause)

            if not new:
                return False  # No new clauses were generated, stop the loop

            # Update the knowledge base with new findings
            self.clauses.extend(new)


    def resolve(self, clause1, clause2):
        '''
        Resolve two clauses.
        '''
        resolvents = []

        clause1 = clause1[0]
        clause2 = clause2[0]

        if isinstance(clause1, tuple):
            clause1 = [clause1]
        if isinstance(clause2, tuple):
            clause2 = [clause2]

        for literal1 in clause1:
            for literal2 in clause2:
                if literal1[0] != literal2[0] and literal1[1] == literal2[1]:
                    # Create a new clause excluding the conflicting literals
                    new_clause = [lit for lit in clause1 if lit != literal1] + [lit for lit in clause2 if lit != literal2]
                    # Remove duplicates and ensure order to prevent reprocessing
                    new_clause_sorted = tuple(sorted(set(new_clause), key=lambda x: (x[1], not x[0])))
                    if new_clause_sorted not in [tuple(r) for r in resolvents]:
                        resolvents.append(new_clause_sorted)
        return resolvents
