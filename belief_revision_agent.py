from belief_base import BeliefBase, Belief
from solver import Solver
import warnings


class BeliefRevisionAgent:
    def __init__(self):
        self.belief_base = BeliefBase()


    def add_belief_with_revision(self, clause, priority=0):
        '''
        Method for adding beliefs with revision, this is the default method for adding beliefs.
        
        The method checks if the new belief is consistent with the current beliefs.
        If it is not, the method performs contraction.
        '''
        new_belief = Belief()
        new_belief.clause = self.belief_base.format_sympy_clause_to_our_format(clause)
        new_belief.priority = priority

        self.revise_belief(new_belief)


    def add_belief(self, clause, priority=0):
        '''
        Just add the belief to the belief base. Clause should be in sympy format.
        '''
        self.belief_base.add_belief(clause, priority)
        
    
    def remove_belief(self, clause):
        '''
        Remove specified belief from the belief base.
        '''
        if self.belief_base.remove_belief(clause):
            print("Belief was removed from belief base")
        else:
            warnings.warn(f"Belief was not removed, there is no such belief in the base: {clause}")            


    def clear_beliefs(self):
        '''
        Clear all beliefs from the belief base.
        '''
        self.belief_base.clear_beliefs()
        
    
    def show_beliefs(self, pretty = True):
        '''
        Print current belief base
        
        If arg "pretty" is set to false, then the database is printend in the raw format (list of lists of tuples)  
        '''
        if pretty:
            print(self.belief_base.pretty_print())
        else:
            for belief in self.belief_base.beliefs:
                print(f"{belief.clause} / Priority: {belief.priority}")


    def revise_belief(self, new_belief: Belief):
        '''
        Method for revising beliefs based on new information.
        
        The method checks if the new belief is consistent with the current beliefs.
        If it is, the method adds the new belief to the belief base.
        If it is not, the method performs contraction.
        '''
        #new_belief.clause = self.belief_base.format_sympy_clause_to_our_format(new_belief.clause)
        if self.belief_base.beliefs == []:
            self.add_belief(new_belief.clause, new_belief.priority)
            print("Belief added to the database.")
        else:
            if self.check_clause_for_no_contradiction(new_belief.clause):
                # Contradiction found for negated clause
                self.add_belief(new_belief.clause, new_belief.priority)
                print("No contradiction found. Belief added to the database.")
            else:
                # If contradiction found, perform contraction
                # print("Contradicting clause of higher or equal priority found. The belief was not added to the database.")
                self.contract_knowledge(new_belief)


    def contract_knowledge(self, conflicting_belief: Belief):
        '''
        Method for contracting knowledge base.
        
        Method is based on the priority of the conflicting beliefs.
        If there are no contracting clauses with higher or same priority, the new belief is added and the conflicting beliefs are removed.
        '''
        beliefs_to_remove = []
        
        solver = Solver()
        solver.add_belief(conflicting_belief)
        
        # Check every belief in the database for contraction
        for belief in self.belief_base.beliefs:
            belief.clause = self.belief_base.format_sympy_clause_to_our_format(belief.clause)
            solver.add_belief(belief)               # Add belief to the solver, there should be only two beliefs in the solver belief base.
            if solver.check_clauses():          # Check if there is a contradiction.
                if belief.priority >= conflicting_belief.priority:
                    print("Contradicting clause of higher or equal priority found. The belief was not added to the database.")
                    return
                else:
                    beliefs_to_remove.append(belief)
            solver.remove_belief(belief)            # Remove belief from the solver.
        
        self.add_belief(conflicting_belief.clause, conflicting_belief.priority)
        print("Contradicting clause(s) of lower priority found. The belief was added to the database.")
        
        if beliefs_to_remove is not None:
            # Remove conflicting beliefs from the database
            print("Following beliefs were removed:")
            for belief in beliefs_to_remove:
                print(f"Priority: {belief.priority}, Belief: {belief.clause}")
                self.belief_base.remove_belief(belief.clause)


    def check_clause_for_no_contradiction(self, clause) -> bool:
        '''
        Method for checking contradiction for the specified clause, regarding the belief base.
        
        return: True if the clause is consistent, False otherwise (contradiction found)
        '''
        solver = Solver()
        for belief in self.belief_base.beliefs:
            solver.add_belief(belief)
            
        new_belief = Belief()

        solver.add_belief(new_belief)
        
        if solver.resolution():
            return True
        else:
            return False


    def check_clause_for_entilement(self, pos_clause) -> bool:
        '''
        Method for checking logical entailment (e.g., resolution-based) for specified the clause.

        pos_clause - clause to check for entailment, not negated (will be negated in the method),
                     it should be in the form compliant with sympy library, since it will be
                     converted to our custom CNF.
                     
        return: True if the clause is entailed, False otherwise
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
