from belief_base import BeliefBase
from belief_revision_agent import BeliefRevisionAgent
from sympy import symbols, Not, Or, And, Equivalent, Implies


class AGM:

    # def __init__(self):
    #     self.belief_base = []
    
    def agm_success(self, belief_base, phi):

        belief_base_copy = belief_base.copy()
        belief_base_copy.append(phi)
        result = self.find_phi_in_base(belief_base_copy, phi)
        return result

    def agm_inclusion(self, belief_base, phi):

        base_expanded = belief_base.copy()
        base_revised = belief_base.copy()

        base_revised.remove(2)
        base_revised.append(phi)
        base_expanded.append(phi)

        result = self.compare_bases(base_revised, base_expanded)

        return result

    def agm_vacuity(self, belief_base, phi):

        belief_base_copy = belief_base.copy()
        phi_copy = phi
        not_phi = 6

        phi_found = self.find_phi_in_base(belief_base_copy, not_phi)

        if phi_found:
            
            # print("Vacuity not applicable")
            return None
        
        else:
            base_expanded = belief_base_copy.copy()
            base_revised = belief_base_copy.copy()

            base_revised.remove(2)
            base_revised.append(phi_copy)

            base_expanded.append(phi_copy)

            result = self.compare_bases(base_revised, base_expanded)

            return result
        
    def agm_consistency(self, belief_base, phi):
        return 
    
    def agm_extensionality(self, belief_base, phi):

        phi_copy = phi
        phi_check = phi

        base1_revised = belief_base.copy()
        base2_revised = belief_base.copy()

        base1_revised.remove(2)
        base1_revised.append(phi_copy)

        base2_revised.remove(2)
        base2_revised.append(phi_check)

        result = self.compare_bases(base1_revised, base2_revised)

        return result

        
    '''''

    pseudo code for the rest

  

    def agm_consistency(self, belief_base, phi):
        
        phi_cons = check_consistency(phi)
        belief_base_cons = check_consistency(revision(belief_base, phi))

        if phi_cons == success && belief_base_cons == success: success else: failure

    def agm_extensionality(self, belief_base, phi):
        
        check_phi = [phi | phi]
        belief_base_new1 = revision(belief_base, phi)
        belief_base_new2 = revision(belief_base, check_phi)

        if belief_base_new1 == belief_base_new2: success else: failure

    '''

    def compare_bases(self, base1, base2):

        # base 1 = revised base
        # base 2 = expanded base

        base1_copy = base1.copy()
        base2_copy = base2.copy()

        state = "failure"

        for belief1 in base1:
            for belief2 in base2:
                if belief1 == belief2:
                    state = "success"
                    break
            else:
                state = "failure"
                break
        if state == "success":
            return True
        else:
            return False
    
    def find_phi_in_base(self, belief_base, phi):

        for belief in belief_base:
            if belief == phi:
                return True
        else:
            return False


def main():
    belief_base_test = [1, 2, 3]
    phi_test = 4

    test = AGM()

    print(f"succes: {test.agm_success(belief_base_test, phi_test)}")
    print(f"inclusion: {test.agm_inclusion(belief_base_test, phi_test)}")
    print(f"vacuity: {test.agm_vacuity(belief_base_test, phi_test)}")
    print(f"extensionality: {test.agm_extensionality(belief_base_test, phi_test)}")

    # print(test.find_phi_in_base(belief_base_test, phi_test))
    # test.agm_vacuity(belief_base_test, phi_test)
    # print(test.agm_vacuity(belief_base_test, phi_test)) 

    # belief_base_test_exp = belief_base_test.copy()
    # belief_base_test_exp.append(phi_test)

    # assert test.compare_bases(belief_base_test, belief_base_test_exp) == True


if __name__ == "__main__":
    main()