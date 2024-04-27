import unittest
import unittest.mock
from belief_base import BeliefBase, Belief
from belief_revision_agent import BeliefRevisionAgent
from sympy import symbols, Not, Or, And, Equivalent, Implies

A, B, D, p, q, r, s, w, a, b, c = symbols('A B D p q r s w a b c')

class TestBeliefBase(unittest.TestCase):
    def setUp(self):
        self.agent = BeliefRevisionAgent()
        self.common_logs = { # dictionary to store commonly used logs (it is annoying to edit them every time for every occurence)
            "belief_added" : "Belief added to the database.",
            "no_contradiction_found" : "No contradiction found. Belief added to the database.",
            "higher_priority_contradiction" : "Contradicting clause of higher or equal priority found. The belief was not added to the database.",
            "lower_priority_contradiction" : "Contradicting clause(s) of lower priority found. The belief was added to the database.",
            "beliefs_removed" : "Following beliefs were removed:"
        }


    @unittest.mock.patch('builtins.print')
    def test_agent_check_clause_for_entailment_A(self, mock_print):
        # Example A - Arrange
        self.agent.add_belief(p)
        self.agent.add_belief(p >> q)
        # Example A - Act
        result_q = self.agent.check_clause_for_entilement(q)
        result_a = self.agent.check_clause_for_entilement(a)
        # Example A - Assert
        self.assertTrue(result_q)
        self.assertFalse(result_a)
        mock_print.assert_called_with("Belief is not entailed: [[(True, 'a')]]")


    @unittest.mock.patch('builtins.print')
    def test_agent_check_clause_for_entailment_B(self, mock_print):
        # Example B - Arrange
        self.agent.add_belief((p & q) >> s)
        self.agent.add_belief(p)
        self.agent.add_belief(q)
        # Example B - Act
        result_s = self.agent.check_clause_for_entilement(s)
        result_p = self.agent.check_clause_for_entilement(p)
        # Example B - Assert
        self.assertTrue(result_s)
        self.assertTrue(result_p)


    @unittest.mock.patch('builtins.print')
    def test_agent_check_clause_for_entailment_C(self, mock_print):
        # Example C - Arrange
        self.agent.add_belief((a | b) >> c)
        self.agent.add_belief(b)
        # Example C - Act
        result_c = self.agent.check_clause_for_entilement(c)
        # Example C - Assert
        self.assertTrue(result_c)


    @unittest.mock.patch('builtins.print')
    def test_agent_check_clause_for_entailment_D(self, mock_print):
        # Example D - Arrange
        self.agent.add_belief(p >> q)
        self.agent.add_belief(r >> s)
        self.agent.add_belief(p >> r)
        self.agent.add_belief(p)
        # Example D - Act
        result_s = self.agent.check_clause_for_entilement(s)
        result_q = self.agent.check_clause_for_entilement(q)
        result_r = self.agent.check_clause_for_entilement(r)
        # Example D - Assert
        self.assertTrue(result_s)
        self.assertTrue(result_q)
        self.assertTrue(result_r)


    @unittest.mock.patch('builtins.print')
    def test_agent_check_clause_for_entailment_E(self, mock_print):
        # Example E - Arrange
        self.agent.add_belief((~r | p | s) & (~p | r) & (~s | r) & (~r))
        # Example E - Act
        result_not_p = self.agent.check_clause_for_entilement(~p)
        # Example E - Assert
        self.assertTrue(result_not_p)
        
        
    @unittest.mock.patch('builtins.print')
    def test_agent_check_clause_for_entailment_F(self, mock_print):
        # Example F - Arrange
        self.agent.add_belief(p)
        self.agent.add_belief(p >> q)
        self.agent.add_belief(r)
        # Example F - Act
        result_q = self.agent.check_clause_for_entilement(q)
        result_a = self.agent.check_clause_for_entilement(a)
        # Example F - Assert
        self.assertTrue(result_q)
        self.assertFalse(result_a)


    @unittest.mock.patch('builtins.print')
    def test_agent_check_contradiction_A(self, mock_print):        
        self.agent.add_belief_with_revision(w, 0.7)
        mock_print.assert_called_with(self.common_logs["belief_added"])
        self.agent.add_belief_with_revision(~w, 0.3)
        mock_print.assert_called_with(self.common_logs["higher_priority_contradiction"])
        self.agent.add_belief_with_revision(~w, 0.9)
        mock_print.assert_has_calls([
            unittest.mock.call(self.common_logs["lower_priority_contradiction"]),
            unittest.mock.call(self.common_logs["beliefs_removed"]),
            unittest.mock.call("Priority: 0.7, Belief: [[(True, 'w')]]")
        ])
        self.agent.show_beliefs()
        mock_print.assert_called_with("Belief 1 -> priority: 0.9, clause: (not w)")


    @unittest.mock.patch('builtins.print')
    def test_agent_check_equal_priority_contradiction(self, mock_print):
        # Adding a belief
        self.agent.add_belief_with_revision(w, 0.5)
        mock_print.assert_called_with(self.common_logs["belief_added"])
        
        # Adding a contradictory belief with the same priority
        self.agent.add_belief_with_revision(~w, 0.5)
        mock_print.assert_called_with(self.common_logs["higher_priority_contradiction"])


    @unittest.mock.patch('builtins.print')
    def test_agent_no_contradiction(self, mock_print):
        # Adding a belief
        self.agent.add_belief_with_revision(w, 0.8)
        mock_print.assert_called_with(self.common_logs["belief_added"])
        
        # Adding another non-contradictory belief
        self.agent.add_belief_with_revision(p, 0.6)
        mock_print.assert_called_with(self.common_logs["no_contradiction_found"])
        
        # Ensure no contradiction related logs are called
        with self.assertRaises(AssertionError):
            mock_print.assert_called_with(self.common_logs["higher_priority_contradiction"])
            mock_print.assert_called_with(self.common_logs["lower_priority_contradiction"])


if __name__ == '__main__':
    unittest.main()
