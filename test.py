#########################
###### TESTING FILE #####
#########################

#TODO add some normal tests

from belief_base import BeliefBase
from belief_revision_agent import BeliefRevisionAgent


def test_belief_base_raw_output():
    input = [
        "A",
        "A & B",
        "A | B",
        "(D | ~A) & (D | ~B)"
    ]

    expected_output = [
        [[(True, "A")]],
        [[(True, "A")], [(True, "B")]],
        [[(True, "A"), (True, "B")]],
        [[(True, "D"), (False, "A")], [(True, "D"), (False, "B")]]
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
        "A",
        "A & B",
        "A | B",
        "(D | ~A) & (D | ~B)",
    ]

    expected_output = (
        "Belief 1: (A)\n" +
        "Belief 2: (A) AND (B)\n" +
        "Belief 3: (A OR B)\n" +
        "Belief 4: (D OR not A) AND (D OR not B)"
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


def main():
    test_belief_base_raw_output()
    test_belief_base_pretty_print()
    print("All tests passed.")


if __name__ == "__main__":
    main()
