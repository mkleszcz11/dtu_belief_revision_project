from sympy import symbols, Not, Or, And, Equivalent, Implies
from sympy.logic.boolalg import to_cnf


class Belief:
    def __init__(self, clause=[], priority=0):
        self.clause = clause
        self.priority = priority


class BeliefBase:
    def __init__(self):
        self.beliefs = [] # List of Beliefs


    def add_belief(self, clause, priority=0):
        '''
        Add a belief to the belief base.

        clause should be in the form of a disjunction of literals (e.g. ~(A | B) | D)).
        Implies(p & q, r")  should be: p & q >> r
        Equivalent(a | b, c) should be: a | b = c
        '''
        new_belief = Belief()
        new_belief.clause = self.format_sympy_clause_to_our_format(clause)
        new_belief.priority = priority

        self.beliefs.append(new_belief)


    def remove_belief(self, clause) -> bool:
        '''
        Remove a belief from the belief base.

        Returns True if the remove operation was succesful, False otherwise.
        '''
        new_belief = self.format_sympy_clause_to_our_format(clause)

        #find the belief to remove
        for belief in self.beliefs:
            if belief.clause == new_belief:
                self.beliefs.remove(belief)
                return True
        return False


    def clear_beliefs(self):
        '''
        Clear all beliefs from the belief base.
        '''
        self.beliefs = []


    def format_sympy_clause_to_our_format(self, clause):
        '''
        Convert a sympy clause to our format.
        '''
        # Check if clause is already in our format
        if isinstance(clause, list):
            return clause

        cnf_clause = to_cnf(clause, simplify=True)
        our_clause = self.from_symbols_to_list(cnf_clause)
        return our_clause


    def from_symbols_to_list(self, clause):
        '''
        Converts a CNF clause to a standardized nested list format.
        Examples:
            A should be: [[(True, "A")]]
            A & B should be: [[(True, "A")], [(True, "B")]]
            A | B should be: [[(True, "A"), (True, "B")]]
            (D | ~A) & (D | ~B) should be: [[(True, "D"), (False, "A")], [(True, "D"), (False, "B")]]
        '''
        if isinstance(clause, And):
            return [self.process_or_literals(arg) for arg in clause.args]  # Process each 'Or' clause in the 'And'
        elif isinstance(clause, Or):
            return [self.process_or_literals(clause)]  # Single 'Or' clause directly
        else:
            return [[self.process_literal(clause)]]  # Single literal


    def process_or_literals(self, or_clause):
        '''
        Process an 'Or' clause into a list of literals.
        '''
        if isinstance(or_clause, Or):
            return [self.process_literal(lit) for lit in or_clause.args]
        else:
            return [self.process_literal(or_clause)]


    def process_literal(self, literal):
        '''
        Convert a literal to a tuple (is_positive, symbol).
        '''
        if isinstance(literal, Not):
            return (False, str(literal.args[0]))
        else:
            return (True, str(literal))


    def pretty_print(self):
        output = []
        for idx, belief in enumerate(self.beliefs):
            clause = belief.clause
            formatted = ' AND '.join(['(' + ' OR '.join(
                f"{'not ' + element[1] if not element[0] else element[1]}" for element in disjunction
            ) + ')' for disjunction in clause])
            priority = belief.priority
            output.append(f"Belief {idx + 1} -> priority: {priority}, clause: {formatted}")
        return "\n".join(output)


#####################################
########### USAGE EXAMPLE ###########
#####################################

# bb = BeliefBase()
# A, B, D, p, q, r, a, b, c = symbols('A B D p q r a b c')
# bb.add_belief(A)
# bb.add_belief(A & B)
# bb.add_belief(A | B)
# bb.add_belief((D | ~A) & (D | ~B))
# bb.add_belief(p & q >> r)
# bb.add_belief(Equivalent(a | b, c))

# #print raw database
# for idx, belief in enumerate(bb.beliefs):
#     print(f"Belief {idx + 1}: {belief}")

# # Display beliefs in a more readable format
# pretty_db = bb.pretty_print()
# print(pretty_db)

#####################################
########## EXPECTED OUTPUT ##########
#####################################
# Belief 1: [[(True, 'A')]]
# Belief 2: [[(True, 'A')], [(True, 'B')]]
# Belief 3: [[(True, 'A'), (True, 'B')]]
# Belief 4: [[(True, 'D'), (False, 'A')], [(True, 'D'), (False, 'B')]]
