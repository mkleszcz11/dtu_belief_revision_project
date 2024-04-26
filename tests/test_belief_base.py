import unittest
import unittest.mock
from belief_base import BeliefBase
from belief_revision_agent import BeliefRevisionAgent
from sympy import symbols, Not, Or, And, Equivalent, Implies

A, B, D, p, q, r, a, b, c = symbols('A B D p q r a b c')

class TestBeliefBase(unittest.TestCase):
    def setUp(self):
        self.agent = BeliefRevisionAgent()


    def test_belief_base_raw_output(self):
        # Arrange
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

        # Act
        for i in range(len(input)):
            self.agent.belief_base.add_belief(input[i])

        # Assert
        self.assertEqual(self.agent.belief_base.beliefs, expected_output)


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
            "Belief 1: (A)\n" +
            "Belief 2: (A) AND (B)\n" +
            "Belief 3: (A OR B)\n" +
            "Belief 4: (D OR not A) AND (D OR not B)\n"
            "Belief 5: (p) AND (r OR not q)\n"
            "Belief 6: (c OR not a) AND (c OR not b) AND (a OR b OR not c)"
        )

        # Act
        for i in range(len(input)):
            self.agent.belief_base.add_belief(input[i])

        # Assert
        self.assertEqual(self.agent.belief_base.pretty_print(), expected_output)


    @unittest.mock.patch('builtins.print')
    def test_agent_check_belief(self, mock_print):
        # Arrange
        self.agent.add_belief(p)
        self.agent.add_belief(p >> q)

        # Act
        result_q = self.agent.check_belief(q)
        result_a = self.agent.check_belief(a)

        # Assert
        self.assertTrue(result_q)
        self.assertFalse(result_a)
        mock_print.assert_called_with("Belief is not entailed: [[(True, 'a')]]")

if __name__ == '__main__':
    unittest.main()
