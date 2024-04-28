import unittest
import unittest.mock
from belief_base import BeliefBase, Belief
from belief_revision_agent import BeliefRevisionAgent
from sympy import symbols, Not, Or, And, Equivalent, Implies

A, B, D, p, q, r, s, w, a, b, c = symbols('A B D p q r s w a b c')

class TestBeliefBase(unittest.TestCase):
    def setUp(self):
        self.agent = BeliefRevisionAgent()


    def test_belief_base_raw_output(self):
        #Arrange
        input = [
            A,
            A & B,
            A | B,
            (D | ~A) & (D | ~B),
            p & q >> r,
            Equivalent(a | b, c),
            p | p
        ]

        expected_output = [
            [[(True, 'A')]],
            [[(True, 'A')], [(True, 'B')]],
            [[(True, 'A'), (True, 'B')]],
            [[(True, 'D'), (False, 'A')], [(True, 'D'), (False, 'B')]],
            [[(True, 'p')], [(True, 'r'), (False, 'q')]],
            [[(True, 'c'), (False, 'a')], [(True, 'c'), (False, 'b')], [(True, 'a'), (True, 'b'), (False, 'c')]],
            [[(True, 'p')]]
        ]

        # Act
        for i in range(len(input)):
            self.agent.add_belief(input[i], 0.5)

        # Assert
        stored_clauses = []
        for belief in self.agent.belief_base.beliefs:
            stored_clauses.append(belief.clause)

        self.assertEqual(stored_clauses, expected_output)


    def test_belief_base_pretty_print(self):
        # Arrange
        input = [
            A,
            A & B,
            A | B,
            (D | ~A) & (D | ~B),
            p & q >> r,
            Equivalent(a | b, c)
        ]

        expected_output = (
            "Belief 1 -> priority: 0, clause: (A)\n" +
            "Belief 2 -> priority: 0, clause: (A) AND (B)\n" +
            "Belief 3 -> priority: 0, clause: (A OR B)\n" +
            "Belief 4 -> priority: 0, clause: (D OR not A) AND (D OR not B)\n"
            "Belief 5 -> priority: 0, clause: (p) AND (r OR not q)\n"
            "Belief 6 -> priority: 0, clause: (c OR not a) AND (c OR not b) AND (a OR b OR not c)"
        )

        # Act
        for i in range(len(input)):
            self.agent.add_belief(input[i])

        # Assert
        self.assertEqual(self.agent.belief_base.pretty_print(), expected_output)


if __name__ == '__main__':
    unittest.main()
