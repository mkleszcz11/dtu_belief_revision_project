from belief_base import BeliefBase
from belief_revision_agent import BeliefRevisionAgent
from sympy import symbols, Not, Or, And, Equivalent, Implies


class AGM_Cont:

    # def __init__(self):
    #     self.belief_base = []
    
    def agm_success(self, belief_base, phi):


        if not phi == []:

            belief_base_contracted = belief_base.copy()
            belief_base_contracted.remove(phi)

            result = self.find_phi_in_base(belief_base_contracted, phi)

            return not result
        else:
            return None


        return result

    def agm_inclusion(self, belief_base, phi):

        base_contracted = belief_base.copy()
        base_original = belief_base.copy()

        base_contracted.remove(phi)

        result = self.compare_bases(base_contracted, base_original)

        return result

    def agm_vacuity(self, belief_base, phi):

        belief_base_contracted = belief_base.copy()
        belief_base_original = belief_base.copy()
        
        check_cn = self.check_phi_is_in_Cn(belief_base_original, phi)

        if not check_cn:

            # belief_base_contracted.remove(4)

            result = self.compare_bases(belief_base_original, belief_base_contracted)

            return result
        
        return None

    
    
    def agm_extensionality(self, belief_base, phi):

        phi_copy = phi
        phi_check = phi

        base1_contracted = belief_base.copy()
        base2_contracted = belief_base.copy()

        base1_contracted.remove(2)

        base2_contracted.remove(2)

        result = self.compare_bases(base1_contracted, base2_contracted)

        return result


    def compare_bases(self, base1, base2):

        # base 1 = revised base
        # base 2 = expanded base

        base1_copy = base1.copy()
        base2_copy = base2.copy()

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
        
    def check_phi_is_in_Cn(self, belief_base, phi):

        # Check if phi is a part of the logical consequence considering resolution

        result = False

        return result



def main():
    belief_base_test = [1, 2, 3]
    phi_test = belief_base_test[1]

    test = AGM_Cont()

    print(f"succes: {test.agm_success(belief_base_test, phi_test)}")
    print(f"inclusion: {test.agm_inclusion(belief_base_test, phi_test)}")
    print(f"vacuity: {test.agm_vacuity(belief_base_test, phi_test)}")
    print(f"extensionality: {test.agm_extensionality(belief_base_test, phi_test)}")

if __name__ == "__main__":
    main()