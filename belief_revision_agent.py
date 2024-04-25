from belief_base import BeliefBase
from solver import Solver


class BeliefRevisionAgent:
    def __init__(self):
        self.belief_base = BeliefBase()


    def add_belief(self, clause):
        self.belief_base.add_belief(clause)


    def revise_belief(self, new_clause):
        """Method for revising beliefs based on new information"""
        # Solver to check consistency with new belief
        solver =  Solver()
        
        # Add all beliefs to the solver
        for clause in self.belief_base.beliefs:
            solver.add_clause(clause)
        solver.add_clause(new_clause)
        
        # Check if the new knowledge is consistent
        if solver.check_clauses():
            # If consistent, add the new belief
            self.knowledge_base.append(new_clause)
        else:
            # If not consistent, perform contraction
            print("Conflict detected. Contracting knowledge base.")
            self.contract_knowledge(new_clause)
        
        solver.delete()


    def contract_knowledge(self, conflicting_clause):
        """Method for contracting knowledge base"""
        # TODO - what method should be used for contraction?
        # PLACEHOLDER
        pass


    def check_belief(self, pos_clause):
        '''
        Method for checking logical entailment (e.g., resolution-based)
        
        pos_clause - clause to check for entailment, not negated (will be negated in the method),
                     it should be in the form compliant with sympy library, since it will be
                     converted to our custom CNF.
        '''
        solver = Solver()
        for clause in self.belief_base.beliefs:
            solver.add_clause(clause)
        
        pos_clause = self.belief_base.format_symopy_to_our_format(pos_clause)
        neg_clause = []
        for literal in pos_clause:
            neg_clause.append([(not literal[0][0], literal[0][1])])

        solver.add_clause(neg_clause)
        
        if solver.check_clauses(): # contradiction found for neg_clause, so the belief is entailed for pos_clause
            print(f"Belief is entailed: {pos_clause}")
            return True
        else:
            print(f"Belief is not entailed: {pos_clause}")
            return False
