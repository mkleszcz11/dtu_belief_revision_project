from belief_base import BeliefBase
from sympy import symbols, Not, Or, And, Equivalent, Implies
from solver import Solver

class AGM_Rev:
    
    def agm_success(self, belief_base, phi):

        result = self.find_phi_in_base(belief_base, phi)

        return result

    def agm_inclusion(self, base_revised, base_expanded):

        result = self.compare_bases(base_revised, base_expanded)

        return result

    def agm_vacuity(self, belief_orig, belief_rev, belief_exp, phi):

        phi_found = self.find_phi_in_base(belief_orig, phi.clause)

        if not phi_found:
            result = self.compare_bases(belief_rev, belief_exp)
        else:
            result = "Not applicable"      # AGM not applicable
        return result
        
    def agm_consistency(self, bb_agent, phi_agent, clause) -> bool:

        result_phi = phi_agent.check_clause_for_no_contradiction(clause)
        result_bb = bb_agent.check_clause_for_no_contradiction([])

        result = bool(result_bb*result_phi)
       
        return result
    
    def agm_extensionality(self, bb1, bb2):

        result = self.compare_bases(bb1, bb2)

        return result

    def compare_bases(self, base1, base2):

        state = False

        for belief1 in base1:
            for belief2 in base2:
                if belief1 == belief2:
                    state = True
                    break
            else:
                state = False
                break

        return state
    
    def find_phi_in_base(self, belief_base, phi):

        for belief in belief_base:
            if belief == phi:
                return True
        else:
            return False
        
    def check_consistency(self, belief_base):
        return True