from sympy import symbols, Not, Or, And, Equivalent
from sympy.logic.boolalg import to_cnf

class BeliefBase:
    def __init__(self):
        self.beliefs = []
        self.belief_sets = []


    def add_belief(self, clause):
        '''
        Add a belief to the belief base.
        
        clause should be in the form of a disjunction of literals (e.g. ~(A | B) | D)).
        '''
        # if not isinstance(clause, Or):
        #     raise ValueError("The belief should be a disjunction of literals")

        cnf_clause = to_cnf(clause)
        our_belief = self.from_symbols_to_list(cnf_clause)

        self.beliefs.append(our_belief)
            
    def from_symbols_to_list(self, clause):
        ''''
        (D | ~A) & (D | ~B)
        should be:
        [(True, "D"), (False, "A")], [(True, "D") , (False, "B")]
        '''
        if isinstance(clause, And):
            # Handle conjunctions
            return [self.from_symbols_to_list(arg) for arg in clause.args]
        elif isinstance(clause, Or):
            # Handle disjunctions
            return [self.from_symbols_to_list(arg) for arg in clause.args]
        elif isinstance(clause, Not):
            # Handle negation
            return (False, str(clause.args[0]))
        else:
            # Handle plain symbol
            return (True, str(clause))
        
        
    def display_beliefs(self):
        for idx, belief in enumerate(self.beliefs):
            print(f"Belief {idx + 1}:")
            if len(belief) > 1:
                print("KEK")
                print(belief)
                print(len(belief))
                # if isinstance(belief, list):  # Handling conjunctions of disjunctions
                #     formatted = ' AND '.join(['(' + ' OR '.join(
                #         f"{'not ' + element[1] if not element[0] else element[1]}" for element in disjunction
                #     ) + ')' for disjunction in belief])
                #     print(formatted)
                # else:  # If there's a single belief, handle it directly
                #     formatted = ' OR '.join(f"{'not ' + element[1] if not element[0] else element[1]}" for element in belief)
                #     print(formatted)
            






















# class BeliefBase:
#     def __init__(self):
#         self.beliefs = []
#         self.belief_sets = []


#     def add_belief(self, cnf_clause):
#         # Check if the input is structured properly as a list of lists of tuples
#         if not all(isinstance(conjunction, list) and all(isinstance(literal, tuple) for literal in conjunction) for conjunction in cnf_clause):
#             raise ValueError("Each clause must be a list of conjunctions, where each conjunction is a list of tuples (variable, is_negated)")

#         self.beliefs.append(cnf_clause)
#         # converted_clauses = []

#         # for conjunction in cnf_clause:
#         #     conj_set = set()
#         #     for var, is_pos in conjunction:
#         #         if is_pos:
#         #             formatted_var = var
#         #         else:
#         #             formatted_var = 'not ' + var                
#         #         conj_set.add(formatted_var)
            
#         #     # Convert the set to a frozenset (immutable) to add to the list of converted clauses
#         #     converted_clauses.append(frozenset(conj_set))

#         # # Append the transformed CNF clause (list of frozensets) to belief_sets
#         # self.belief_sets.append(set(converted_clauses))
        
#         converted_clause = [frozenset(f"{var if is_pos else 'not ' + var}" for var, is_pos in conjunction) for conjunction in cnf_clause]
#         self.belief_sets.append(set(converted_clause))


#     def add_implication(self, antecedent, consequent):
#         # Transform implication A -> B into ~A OR B
#         transformed_clause = [
#             [("not " + antecedent, True)],  # ~A
#             [(consequent, True)]  # B
#         ]
#         self.add_belief(transformed_clause)


#     def display_beliefs(self):
#         for idx, belief in enumerate(self.beliefs):
#             print(f"Belief {idx + 1}:")
#             # Create a string for each clause and join them with ' OR '
#             formatted_clauses = [
#                 " AND ".join(f"{'not ' if not is_pos else ''}{var}" for var, is_pos in clause)
#                 for clause in belief
#             ]
#             print(f"({') OR ('.join(formatted_clauses)})\n")  # Encapsulate clauses in parentheses and separate by 'OR'
