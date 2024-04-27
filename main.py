from belief_revision_agent import BeliefRevisionAgent
from sympy import symbols

from sympy import symbols, Not, Or, And, Equivalent, Implies

agent = BeliefRevisionAgent()

A, B, D, p, q, r, s, w, a, b, c = symbols('A B D p q r s w a b c')


agent.add_belief_with_revision(w, 0.7, verbose_print=True)
agent.add_belief_with_revision(~w, 0.3, verbose_print=True)
agent.add_belief_with_revision(~w, 0.9, verbose_print=True)

# agent.add_belief_with_revision(p >> r, verbose_print=True)
# # agent.add_belief_with_revision(p >> q)
# agent.add_belief_with_revision(p, verbose_print=True)
# agent.add_belief_with_revision(~r, 0.7, verbose_print=True)

print("Current Belief Base:")
agent.show_beliefs()


# #Adding first belief
# agent.add_belief_with_revision(Equivalent(a | b, c), 0.7)

# #Adding second belief
# agent.add_belief_with_revision(q, 0.8)

# #Adding third belief
# agent.add_belief_with_revision(a | c, 0.9)


# agent.add_belief_with_revision(w, 0.7)
# # agent.show_beliefs()
# agent.add_belief_with_revision(~w, 0.3)
# # agent.show_beliefs()
# agent.add_belief_with_revision(~w, 0.9)
# # agent.show_beliefs()

# agent.show_beliefs(pretty=False)

        
# MAIN IS NOT WORKING, WRITE A NEW ONE
# w = symbols('w')
# print("Adding belief w with 0.7")
# agent.add_belief_with_revision(w, 0.7)
# print("Adding belief ~w with 0.3")
# agent.add_belief_with_revision(~w, 0.3)
# print("Adding belief ~w with 0.8")
# agent.add_belief_with_revision(~w, 0.8)
# #agent.add_belief_with_revision(~w, 0.3)

# while True:
#     print("Enter a belief to add to the agent's belief base (e.g., ~(A | B) | D):")
#     belief = input()
#     if belief == "exit":
#         break
#     agent.add_belief(belief)
    
#     print("Current Belief Base:")
#     print(agent.belief_base.pretty_print())
#     print("----------")



# #add "r"
# agent.add_belief([
#     [("r", True)]
#     ])

# # add p or s
# agent.add_belief([
#     [("p", True), ("s", True)], 
#     [("z", False), ("w", False)]
#     ])


# # add a and b and c
# agent.add_belief([
#     [("a", True), ("b", True), ("c", True)]
#     ])

# agent.add_implication("a", "b")

# agent.belief_base.display_beliefs()

# print("####################")
# print(agent.belief_base.belief_sets)


#agent.add_belief([-1, 3])  # Adding another belief: not p or r



# # Attempt to add a conflicting belief
# agent.revise_belief([-3])  # Adding a belief: not r

# # Check beliefs
# print("Is 'p or not q' a belief? ", agent.check_belief([1, -2]))
# print("Is 'not r' a belief? ", agent.check_belief([-3]))

# # Output current knowledge base
# print("Current Knowledge Base:")
# for clause in agent.knowledge_base:
#     print(clause)
   
# print("###################")
    
# print(agent.knowledge_base)
