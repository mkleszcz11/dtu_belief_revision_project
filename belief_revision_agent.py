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
        for clause in self.knowledge_base:
            solver.add_clause(clause)
        solver.add_clause(new_clause)
        
        # Check if the new knowledge is consistent
        if solver.solve():
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


    def check_belief(self, clause):
        """Method for checking logical entailment (e.g., resolution-based)"""
        solver = Solver()
        for clause in self.knowledge_base:
            solver.add_clause(clause)
        
        if solver.check_clauses():
            print(f"Belief is entailed: {clause}")
            return True
        else:
            print(f"Belief is not entailed: {clause}")
            return False
