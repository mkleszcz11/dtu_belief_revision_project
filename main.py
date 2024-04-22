from belief_revision_agent import BeliefRevisionAgent

agent = BeliefRevisionAgent()
agent.add_belief([1, -2])  # Adding a belief: p or not q
agent.add_belief([-1, 3])  # Adding another belief: not p or r

# Attempt to add a conflicting belief
agent.revise_belief([-3])  # Adding a belief: not r

# Check beliefs
print("Is 'p or not q' a belief? ", agent.check_belief([1, -2]))
print("Is 'not r' a belief? ", agent.check_belief([-3]))

# Output current knowledge base
print("Current Knowledge Base:")
for clause in agent.knowledge_base:
    print(clause)
   
print("###################")
    
print(agent.knowledge_base)
