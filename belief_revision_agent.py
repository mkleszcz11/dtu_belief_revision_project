from belief_base import BeliefBase, Belief
from solver import Solver
import warnings
import copy
from agms_revision import AGM_Rev

class BeliefRevisionAgent:
    def __init__(self):
        self.belief_base = BeliefBase()


    def add_belief_with_revision(self, clause, priority=0, verbose_print=False):
        '''
        Method for adding beliefs with revision, this is the default method for adding beliefs.
        
        The method checks if the new belief is consistent with the current beliefs.
        If it is not, the method performs contraction.

        '''
        new_belief = Belief()
        new_belief.clause = self.belief_base.format_sympy_clause_to_our_format(clause)
        new_belief.priority = priority                                      # New belief added to queue

        clause_copy = copy.deepcopy(clause)
        # print(clause_copy)

        clause_test_vac = f"~{clause_copy}"
        # print(clause_test_vac)

        new_belief_test_vac = Belief()
        new_belief_test_vac.clause = self.belief_base.format_sympy_clause_to_our_format(clause_test_vac)
        new_belief_test_vac.priority = priority     

        # print(new_belief_test_vac.clause)

        clause_test_ext = f"{clause_copy} | {clause_copy}"
        # print(clause_test)

        

        new_belief_test = Belief()
        new_belief_test.clause = self.belief_base.format_sympy_clause_to_our_format(clause_test_ext)
        new_belief_test.priority = priority     

        # print(f"comparison: {new_belief.clause} and {new_belief_test.clause}")

        bb_copy: BeliefBase = copy.deepcopy(self.belief_base)
        phi_copy: Belief = copy.deepcopy(new_belief)
        beliefs_separated = [belief.clause for belief in bb_copy.beliefs]
        phi_separated = phi_copy.clause

        # print("phi: ", phi_copy)
        # print("phi sep: ", phi_separated)
        # print(f"before: {beliefs_separated}")

        result = self.revise_belief(new_belief, verbose_print)                       # Belief revised with the queue

        bb_after_exp: BeliefBase = copy.deepcopy(bb_copy)
        bb_after_exp.add_belief(new_belief.clause, new_belief.priority)
        bb_exp_sep = [belief.clause for belief in bb_after_exp.beliefs]

        bb_after_rev: BeliefBase = copy.deepcopy(self.belief_base)
        bb_rev_sep = [belief.clause for belief in bb_after_rev.beliefs]

        # print(f"after: {bb_separated}")
        
        print("resu: ", self.check_agms("Vacuity", belief_orig=beliefs_separated, belief_rev=bb_rev_sep, belief_exp=bb_exp_sep, phi=new_belief_test_vac))

        # if result:
        #     print(self.check_agms("Success", belief_rev=bb_rev_sep, phi=phi_copy))
        #     # print(self.check_agms("Inclusion", belief_rev=bb_rev_sep, belief_exp=bb_exp_sep))
        #     # print(self.check_agms("Vacuity", belief_rev=bb_rev_sep, phi=phi_copy))
        #     # print(self.check_agms("Consistency", belief_rev=bb_rev_sep, phi=phi_copy))
        #       print("resu: ", self.check_agms("Consistency", belief_rev=bb_after_rev, phi=phi_copy))
              # print("resu: ", self.check_agms("Extensionality", belief_rev=bb_copy, belief_exp=bb_exp_sep, phi=new_belief_test))
        # else:
        #     print("AGMs not needed")


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
        print("Current Belief Base:")
        if pretty:
            print(self.belief_base.pretty_print())
        else:
            for belief in self.belief_base.beliefs:
                print(f"{belief.clause} / Priority: {belief.priority}")


    def revise_belief(self, new_belief: Belief, verbose_print=False):
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
            return True
        else:
            if self.check_clause_for_no_contradiction(new_belief.clause):
                # Contradiction not found for negated clause
                self.add_belief(new_belief.clause, new_belief.priority)
                print("No contradiction found. Belief added to the database.")
                return True
            else:
                #print("Contradiction found. Performing contraction.")
                # If contradiction found, perform contraction
                # print("Contradicting clause of higher or equal priority found. The belief was not added to the database.")
                res = self.contract_knowledge(new_belief, verbose_print)
                return res


    def contract_knowledge(self, conflicting_belief: Belief, verbose_print=False) -> BeliefBase:
        '''
        Method for contracting knowledge base.
        
        Method is based on the priority of the conflicting beliefs.
        If there are no contracting clauses with higher or same priority, the new belief is added and the conflicting beliefs are removed.
        
        It returns the new belief base, after contraction
        '''
        # belief_base_copy = self.belief_base.copy.deepcopy()
        beliefs_to_remove = []
        local_base = BeliefBase()

        conflicting_belief.clause = self.belief_base.format_sympy_clause_to_our_format(conflicting_belief.clause)

        for new_global_belief in self.belief_base.beliefs:
            # 1. Add new_global_belief to the local_base
            # 2. Check for contradiction of the conflicting_belief with the local_base
            # 3. If there is a contradiction, check the priority of the new_global_belief
            # 3.1. If the priority of the new_global_belief is higher or equal, return the original belief_base
            # 3.2. If the priority of the new_global_belief is lower, remove the newly added belief from the local_base and add it to the list of removed beliefs
            local_base.add_belief(new_global_belief.clause)
            if not self.check_clause_for_no_contradiction(conflicting_belief.clause, local_base):
                if new_global_belief.priority >= conflicting_belief.priority:
                    print("Contradicting clause of higher or equal priority found. The belief was not added to the database.")
                    # return self.belief_base    # Marcel change
                    return False
                else:
                    local_base.remove_belief(new_global_belief.clause)
                    beliefs_to_remove.append(new_global_belief)

        self.belief_base = local_base
        self.add_belief(conflicting_belief.clause, conflicting_belief.priority)
        print("Contradicting clause(s) of lower priority found. The belief was added to the database.")

        if verbose_print:
            print("Following beliefs were removed:")
            for belief in beliefs_to_remove:
                print(f"Priority: {belief.priority}, Belief: {belief.clause}")

        # return local_base  # Marcel change
        return True


    def check_clause_for_no_contradiction(self, clause, local_base=None) -> tuple[bool, Belief]:
        '''
        Method for checking contradiction for the specified clause, regarding the belief base.
        
        return: Tuple (True, None) if no contradiction is found,
                Tuple (False, conflicting_belief) if contradiction is found
        '''
        solver = Solver()
        for belief in self.belief_base.beliefs:
            solver.add_belief(belief)
            
        new_belief = Belief()
        new_belief.clause = clause
        solver.add_belief(new_belief)
        
        if solver.resolution():
            return False
        else:
            return True


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

    def check_agms(self, choice, belief_orig, belief_rev, belief_exp=[], phi=[]):

        # print(f"bb {belief_base}")
        # print(f"phi: {phi}")

        testing = AGM_Rev()
        

        if choice == "Success":
            result = testing.agm_success(belief_rev, phi.clause)
        elif choice == "Inclusion":
            result = testing.agm_inclusion(belief_rev, belief_exp)
        elif choice == "Vacuity":

            result = testing.agm_vacuity(belief_orig, belief_rev, belief_exp, phi)

            if result == "Not applicable":
                print(result)
                result = True
        
        elif choice == "Consistency":
            # print(phi.clause)
            phi_test = BeliefRevisionAgent()
            bb_test = BeliefRevisionAgent()

            bb_test.belief_base = belief_rev

            result = testing.agm_consistency(bb_test, phi_test, phi.clause)
         
            phi_test.clear_beliefs
        elif choice == "Extensionality":

            print(phi.clause)
            # phi.clause = [phi.clause, phi.clause]

            bb_test = BeliefRevisionAgent()

            bb_test.belief_base = belief_rev  # copy of bb before revision
            bb_test.revise_belief(phi)
            bb_sep = [belief.clause for belief in bb_test.belief_base.beliefs]  

            bb_rev = belief_exp  #actually revised by main

            print(f"test: {bb_sep}, rev: {bb_rev}")

            result = testing.agm_extensionality(bb_sep, bb_rev)

            
        return result