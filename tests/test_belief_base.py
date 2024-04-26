import unittest
import unittest.mock
from belief_base import BeliefBase, Belief
from belief_revision_agent import BeliefRevisionAgent
from sympy import symbols, Not, Or, And, Equivalent, Implies

A, B, D, p, q, r, s, a, b, c = symbols('A B D p q r s a b c')

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
            "Belief 1: priority: 0, clause: (A)\n" +
            "Belief 2: priority: 0, clause: (A) AND (B)\n" +
            "Belief 3: priority: 0, clause: (A OR B)\n" +
            "Belief 4: priority: 0, clause: (D OR not A) AND (D OR not B)\n"
            "Belief 5: priority: 0, clause: (p) AND (r OR not q)\n"
            "Belief 6: priority: 0, clause: (c OR not a) AND (c OR not b) AND (a OR b OR not c)"
        )

        # Act
        for i in range(len(input)):
            self.agent.add_belief(input[i])

        # Assert
        self.assertEqual(self.agent.belief_base.pretty_print(), expected_output)


    @unittest.mock.patch('builtins.print')
    def test_agent_check_clause_A(self, mock_print):
        # Example A - Arrange
        self.agent.add_belief(p)
        self.agent.add_belief(p >> q)
        # Example A - Act
        result_q = self.agent.check_clause(q)
        result_a = self.agent.check_clause(a)
        # Example A - Assert
        self.assertTrue(result_q)
        self.assertFalse(result_a)
        mock_print.assert_called_with("Belief is not entailed: [[(True, 'a')]]")


    @unittest.mock.patch('builtins.print')
    def test_agent_check_clause_B(self, mock_print):
        # Example B - Arrange
        self.agent.add_belief((p & q) >> s)
        self.agent.add_belief(p)
        self.agent.add_belief(q)
        # Example B - Act
        result_s = self.agent.check_clause(s)
        result_p = self.agent.check_clause(p)
        # Example B - Assert
        self.assertTrue(result_s)
        self.assertTrue(result_p)


    @unittest.mock.patch('builtins.print')
    def test_agent_check_clause_C(self, mock_print):
        # Example C - Arrange
        self.agent.add_belief((a | b) >> c)
        self.agent.add_belief(b)
        # Example C - Act
        result_c = self.agent.check_clause(c)
        # Example C - Assert
        self.assertTrue(result_c)


    @unittest.mock.patch('builtins.print')
    def test_agent_check_clause_D(self, mock_print):
        # Example D - Arrange
        self.agent.add_belief(p >> q)
        self.agent.add_belief(r >> s)
        self.agent.add_belief(p >> r)
        self.agent.add_belief(p)
        # Example D - Act
        result_s = self.agent.check_clause(s)
        result_q = self.agent.check_clause(q)
        result_r = self.agent.check_clause(r)
        # Example D - Assert
        self.assertTrue(result_s)
        self.assertTrue(result_q)
        self.assertTrue(result_r)


    @unittest.mock.patch('builtins.print')
    def test_agent_check_clause(self, mock_print):
        # Example E - Arrange
        self.agent.add_belief((~r | p | s) & (~p | r) & (~s | r) & (~r))
        # Example E - Act
        result_not_p = self.agent.check_clause(~p)
        # Example E - Assert
        self.assertTrue(result_not_p)


if __name__ == '__main__':
    unittest.main()
