from belief_base import BeliefBase, Belief
from solver import Solver


class BeliefRevisionAgent:
    def __init__(self):
        self.belief_base = BeliefBase()


    def add_belief(self, clause, priority=0):
        self.belief_base.add_belief(clause, priority)


    def clear_beliefs(self):
        self.belief_base.clear_beliefs()


    def revise_belief(self, new_clause, priority=0):
        """Method for revising beliefs based on new information"""
        # Solver to check consistency with new belief
        solver =  Solver()
        
        # Add all beliefs to the solver
        for belief in self.belief_base.beliefs:
            solver.add_belief(belief)

        solver.add_belief(new_clause, priority)
 
        # Check if the new knowledge is consistent
        if solver.check_clauses():
            # If consistent, add the new belief
            self.add_belief(new_clause, priority)
        else:
            # If not consistent, perform contraction
            print("Conflict detected. Contracting knowledge base.")
            self.contract_knowledge(new_clause, priority)


    def contract_knowledge(self, conflicting_clause):
        """Method for contracting knowledge base"""
        # TODO - what method should be used for contraction?
        # PLACEHOLDER
        pass


    def check_clause(self, pos_clause):
        '''
        Method for checking logical entailment (e.g., resolution-based)
        
        pos_clause - clause to check for entailment, not negated (will be negated in the method),
                     it should be in the form compliant with sympy library, since it will be
                     converted to our custom CNF.
        '''
        solver = Solver()
        for belief in self.belief_base.beliefs:
            solver.add_belief(belief)
        
        pos_clause = self.belief_base.format_sympy_clause_to_our_format(pos_clause)
        neg_clause = []
        for literal in pos_clause:
            neg_clause.append([(not literal[0][0], literal[0][1])])

        belief_to_check = Belief()
        belief_to_check.clause = neg_clause
        solver.add_belief(belief_to_check)
        
        if solver.check_clauses(): # contradiction found for neg_clause, so the belief is entailed for pos_clause
            print(f"Belief is entailed: {pos_clause}")
            return True
        else:
            print(f"Belief is not entailed: {pos_clause}")
            return False
