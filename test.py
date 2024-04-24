#########################
###### TESTING FILE #####
#########################

#TODO add some normal tests

from belief_base import BeliefBase
from belief_revision_agent import BeliefRevisionAgent
from sympy import symbols, Not, Or, And, Equivalent, Implies

A, B, D, p, q, r, a, b, c = symbols('A B D p q r a b c')

def test_belief_base_raw_output():
    A, B, D = symbols('A B D')
    input = [
        A,
        A & B,
        A | B,
        (D | ~A) & (D | ~B),
        p & q >> r,
        Equivalent(a | b, c)
    ]

    expected_output = [
        [[(True, 'A')]],
        [[(True, 'A')], [(True, 'B')]],
        [[(True, 'A'), (True, 'B')]],
        [[(True, 'D'), (False, 'A')], [(True, 'D'), (False, 'B')]],
        [[(True, 'p')], [(True, 'r'), (False, 'q')]],
        [[(True, 'c'), (False, 'a')], [(True, 'c'), (False, 'b')], [(True, 'a'), (True, 'b'), (False, 'c')]]
    ]
    
    agent = BeliefRevisionAgent()
    for i in range(len(input)):
        agent.belief_base.add_belief(input[i])
        # print("-----------")
        # print(agent.belief_base.beliefs[i])
        # print(expected_output[i])
        assert agent.belief_base.beliefs[i] == expected_output[i]
    
    print("-------------")
    print("test_belief_base_raw_output passed")


def test_belief_base_pretty_print():
    input = [
        A,
        A & B,
        A | B,
        (D | ~A) & (D | ~B),
        p & q >> r,
        Equivalent(a | b, c)
    ]

    expected_output = (
        "Belief 1: (A)\n" +
        "Belief 2: (A) AND (B)\n" +
        "Belief 3: (A OR B)\n" +
        "Belief 4: (D OR not A) AND (D OR not B)\n"
        "Belief 5: (p) AND (r OR not q)\n"
        "Belief 6: (c OR not a) AND (c OR not b) AND (a OR b OR not c)"
    )
    
    agent = BeliefRevisionAgent()

    for i in range(len(input)):
        agent.belief_base.add_belief(input[i])

    # print("-----------")
    # print(agent.belief_base.pretty_print())
    # print(expected_output)

    assert agent.belief_base.pretty_print() == expected_output
    print("-------------")
    print("test_belief_base_pretty_print passed")


def test_agent_check_belief():
    '''
    1. Add some beliefs to the agent's belief base (logically entailed beliefs)
    2. Check the entiled beliefs
    3. Check the non-entailed beliefs
    '''
    agent = BeliefRevisionAgent()
    agent.add_belief("A")
    agent.add_belief("A & B")
    agent.add_belief("A | B")


def main():
    test_belief_base_raw_output()
    test_belief_base_pretty_print()
    print("All tests passed.")


if __name__ == "__main__":
    main()
