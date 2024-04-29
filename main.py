from belief_revision_agent import BeliefRevisionAgent
from sympy import symbols

from sympy import symbols, Not, Or, And, Equivalent, Implies
from agms_revision import AGM_Rev

p, q, r, s = symbols('p q r s')

if __name__ == "__main__":

    print("========================= Example 1 ============================")
    agent = BeliefRevisionAgent()
    agent.add_belief_with_revision(p, 0.7, verbose_print=True)
    agent.add_belief_with_revision(r, 0.7, verbose_print=True)
    agent.add_belief_with_revision(And(p, r), 0.7, verbose_print=True)
    agent.show_beliefs(pretty=True)
    agent.clear_beliefs()

    print("========================= Example 2 ============================")
    agent.add_belief_with_revision(p, 0.7, verbose_print=True)
    agent.add_belief_with_revision(Implies(p, r), 0.7, verbose_print=True)
    agent.add_belief_with_revision(r, 0.7, verbose_print=True)
    agent.show_beliefs(pretty=True)
    agent.clear_beliefs()

    print("========================= Example 3 ============================")
    agent.add_belief_with_revision(p, 0.7, verbose_print=True)
    agent.add_belief_with_revision(Implies(p, r), 0.7, verbose_print=True)
    agent.add_belief_with_revision(~r, 0.3, verbose_print=True)
    agent.show_beliefs(pretty=True)
    agent.clear_beliefs()

    print("========================= Example 4 ============================")
    agent.add_belief_with_revision(p, 0.7, verbose_print=True)
    agent.add_belief_with_revision(Implies(p, r), 0.3, verbose_print=True)
    agent.add_belief_with_revision(~r, 0.5, verbose_print=True)
    agent.show_beliefs(pretty=True)
    agent.clear_beliefs()

    print("========================= Example 5 ============================")
    agent.add_belief_with_revision(p, 0.9, verbose_print=True)
    agent.add_belief_with_revision(Implies(p, r), 0.8, verbose_print=True)
    agent.add_belief_with_revision(Implies(r, q), 0.7, verbose_print=True)
    agent.add_belief_with_revision(Implies(q, s), 0.6, verbose_print=True)
    agent.add_belief_with_revision(And(r,And(q, s)), 0.5, verbose_print=True)
    agent.add_belief_with_revision(~p, 1, verbose_print=True)
    agent.show_beliefs(pretty=True)
    agent.clear_beliefs()

