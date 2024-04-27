# from belief_base import BeliefBase
from solver import Solver
from belief_revision_agent import BeliefRevisionAgent
def check_consistent(agent,phi):
    solver =  Solver()

    # Add all beliefs to the solver
    for clause in phi.belief_base.beliefs:
        solver.add_belief([clause,0.2])
        
    #check phi is consistent or not    
    phi_consistent = solver.check_clauses()      
    
    if not phi_consistent:
        return False
    
    B1 = agent.copy()
    for belief in phi.belief_base.beliefs:
        B1.revise_belief(belief)
    
        return belief in B1.belief_base.beliefs
    
    
def check_extensional(agent,x,y):

    B2 = agent.copy()
    B3 = agent.copy()
    B2.revise_belief(x)
    B3.revise_belief(y)
    return B2.belief_base.beliefs == B3.belief_base.beliefs

    
    

def main():

    phi = BeliefRevisionAgent()
    phi.add_belief('s',0.2)

    agent = BeliefRevisionAgent()
    agent.add_belief('s',0.2)
    agent.add_belief('a',0.2)
    print(agent.belief_base.beliefs)
    x = [[(True, 's'),0.2]]
    y = [[(True, 's'), (True, 's')]]

    if check_consistent(agent, phi) == True:
        print("consistency success")
    if check_extensional(agent,x,y) == True:
        print("extensionality success")

if __name__ == "__main__":
    main()

