from belief_base import BeliefBase
from solver import Solver
from belief_revision_agent import BeliefRevisionAgent
from sympy import symbols, Not, Or, And, Equivalent, Implies
from sympy.logic.boolalg import to_cnf
from belief_base import Belief

from sympy import symbols

A, B, D, p, q, r, s, w, a, b, c = symbols('A B D p q r s w a b c')

def check_consistent(agent,phi):
    solver =  Solver()
    solver1 = Solver()
    # phi = BeliefRevisionAgent()
    # Add all beliefs to the solver
    for belief in phi.belief_base.beliefs:
        solver.add_belief(belief)
        print(solver.resolution())
        
    #check phi is consistent or not    
    phi_consistent = solver.check_clauses()  
    # print(phi_consistent)    
    
    if  phi_consistent:
        print("q")
        return False
    
    B1 = agent.copy()
    B1.show_beliefs(pretty=False)
    for belief in phi.belief_base.beliefs:
        B1.revise_belief(belief)
        B1.show_beliefs(pretty=False)
        for belief in phi.belief_base.beliefs:
            solver1.add_belief(belief)
            new = solver1.resolution()
            if not new :
                return True
        
    
    
def check_extensional(agent,x,y):

    B2 = agent.copy()
    B3 = agent.copy()
    for belief in x.belief_base.beliefs:
        B2.revise_belief(belief)
    for belief in y.belief_base.beliefs:
        B3.revise_belief(belief)
   
    #compare B2 == B3

    return True
    

def main():

    phi = BeliefRevisionAgent()
    phi.add_belief(s, 0.2)

    agent = BeliefRevisionAgent()
    agent.add_belief(s,0.2)
    agent.add_belief(a,0.2)
    agent.show_beliefs(pretty=False)
    
    x = BeliefRevisionAgent()
    y = BeliefRevisionAgent()
    x.add_belief(s,0.2)
    y.add_belief(s,0.2)


    if check_consistent(agent, phi) == True:
        print("consistency success")
    if check_extensional(agent,x,y) == True:
        print("extensionality success")

if __name__ == "__main__":
    main()

