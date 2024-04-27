from belief_revision_agent import BeliefRevisionAgent
from agms_revision import AGM_Rev

agent = BeliefRevisionAgent()


print("Enter a belief to add to the agent's belief base (e.g., ~(A | B) | D):")
belief = input()
agent.add_belief(belief)
testing = AGM_Rev(agent)

print("Current Belief Base:")
print(agent.belief_base.pretty_print())
print("----------")

# print("Testing AGMs")
# print(testing.agm_success(agent.belief_base, []))

# MAIN IS NOT WORKING, WRITE A NEW ONE


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
