from belief_base import BeliefBase
from sympy import symbols, Not, Or, And, Equivalent, Implies
from solver import Solver

class AGM_Rev:

    # def __init__(self, agent):
    #     self.belief_base = agent.belief_base.deepcopy()
    #     print(f"Hello: {self.belief_base.beliefs}")
    
    def agm_success(self, belief_base, phi):

        result = self.find_phi_in_base(belief_base, phi)

        return result

    def agm_inclusion(self, base_revised, base_expanded):

        result = self.compare_bases(base_revised, base_expanded)

        return result

    # def agm_vacuity(self, belief_base, phi):

    #     phi_found = self.find_phi_in_base(belief_base, not_phi)

    #     if phi_found:
            
    #         # print("Vacuity not applicable")
    #         return None
        
    #     else:
    #         base_expanded = belief_base_copy.copy()
    #         base_revised = belief_base_copy.copy()

    #         base_revised.remove(2)
    #         base_revised.append(phi_copy)

    #         base_expanded.append(phi_copy)

    #         result = self.compare_bases(base_revised, base_expanded)

    #         return result
        
    def agm_consistency(self, bb_agent, phi_agent, clause) -> bool:

        result_phi = phi_agent.check_clause_for_no_contradiction(clause)
        result_bb = bb_agent.check_clause_for_no_contradiction([])
       
        return result_bb*result_phi
    
    # def check_consistent(belief_rev,phi):
    #     solver =  Solver()
    #     solver1 = Solver()
    #     # phi = BeliefRevisionAgent()
    #     # Add all beliefs to the solver
    #     for belief in phi.belief_base.beliefs:
    #         solver.add_belief(belief)
    #         print(solver.resolution())
            
    #     #check phi is consistent or not    
    #     phi_consistent = solver.check_clauses()  
    #     # print(phi_consistent)    
        
    #     if  phi_consistent:
    #         # print("q")
    #         return False
        
    #     # B1 = agent.copy()
    #     # B1.show_beliefs(pretty=False)
    #     for belief in phi.belief_rev.beliefs:
    #         # B1.revise_belief(belief)
    #         B1.show_beliefs(pretty=False)
    #         for belief in phi.belief_base.beliefs:
    #             solver1.add_belief(belief)
    #             new = solver1.resolution()
    #             if not new :
    #                 return True
    
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

        print(f"bb1: {belief_base}")
        print(f"phi: {phi}")

        for belief in belief_base:
            if belief == phi:
                print("compared1: ", belief)
                print("compared2: ", phi)
                return True
        else:
            return False
        
    def check_consistency(self, belief_base):
        return True


def main():
    belief_base_test = [1, 2, 3]
    phi_test = 4

    # test = AGM_Rev()

    # print(f"succes: {test.agm_success(belief_base_test, phi_test)}")
    # print(f"inclusion: {test.agm_inclusion(belief_base_test, phi_test)}")
    # print(f"vacuity: {test.agm_vacuity(belief_base_test, phi_test)}")
    # print(f"consistency: {test.agm_consistency(belief_base_test, phi_test)}")
    # print(f"extensionality: {test.agm_extensionality(belief_base_test, phi_test)}")

if __name__ == "__main__":
    main()
