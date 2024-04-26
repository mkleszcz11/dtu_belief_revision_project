from belief_base import BeliefBase
from belief_revision_agent import BeliefRevisionAgent
from sympy import symbols, Not, Or, And, Equivalent, Implies


class AGM:

    # def __init__(self):
    #     self.belief_base = []
    
    def agm_success(self, belief_base, phi):

        for belief in belief_base:
            if belief == phi:
                print("Success")
                break
        else:
            print("Success postulate not met")

    def agm_inclusion(self, belief_base, phi):

        # belief_base_copy = belief_base
        # base_expanded = belief_base.add_belief(belief_base_copy, phi)
        # base_revised = belief_base.revision(belief_base_copy, phi)

         # if base_expanded == base_revised:
        #     print("Inclusion success")
        # else:
        #     print("Inclusion failure")

        base_expanded = belief_base.copy()
        base_revised = belief_base.copy()
        # base_expanded.append(phi)
        base_revised.remove(2)
        base_revised.append(phi)
        # base_revised.append(phi)

       

        print(base_expanded)
        print(base_revised)

        for belief_rev in base_revised:
            for belief_exp in base_expanded:
                if belief_rev == belief_exp:
                    break
            else:
                print("Inclusion failed")
                break

    '''''

    pseudo code for the rest

    def agm_vacuity(self, belief_base, phi):

        if Not(phi) is not in belief_base:
            result = agm_inclusion
            success
        else:
            failure

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


def main():
    belief_base_test = [1, 2, 3]
    phi_test = 4

    test = AGM()

    test.agm_inclusion(belief_base_test, phi_test)


if __name__ == "__main__":
    main()