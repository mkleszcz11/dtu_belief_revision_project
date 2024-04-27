import unittest
import unittest.mock
from belief_base import Belief
from belief_revision_agent import BeliefRevisionAgent
from sympy import symbols, Not, Or, And, Equivalent, Implies

A, B, C, D, p, q, r, s, a, b, c = symbols('A B C D p q r s a b c')

class TestBeliefBase(unittest.TestCase):
    def setUp(self):
        self.agent_a = BeliefRevisionAgent()
        self.agent_b = BeliefRevisionAgent()


    @unittest.mock.patch('builtins.print') # just to hide the prints
    def test_agent_AGM_revision_success_true(self, mock_print):
        # check if the belief base is updated with the new belief
        # Arrange
        self.agent_a.add_belief(A)
        # Act
        self.agent_a.revise_belief((A & B & C))
        # Assert
        self.assertTrue(any([A & B & C in belief for belief in self.agent_a.belief_base.beliefs]))

    @unittest.mock.patch('builtins.print')
    def test_agent_AGM_revision_success_false(self, mock_print):
        # check if the belief base is not updated with random belief
        # Arrange
        self.agent_a.add_belief(A)
        # Act
        self.agent_a.revise_belief(B)
        # Assert
        self.assertNotEqual(self.agent.belief_base.beliefs, [[A], [C]])


    @unittest.mock.patch('builtins.print')
    def test_agent_AGM_revision_inclusion_true(self, mock_print):
        # check if the belief base of agent_a is a subset of agent_b
        # Arrange
        self.agent_a.add_belief(p)
        self.agent_a.add_belief(q)
        self.agent_a.add_belief(Implies(p, q))

        self.agent_b.add_belief(p)
        self.agent_b.add_belief(q)
        self.agent_b.add_belief(Implies(p, q))
        self.agent_b.add_belief(Not(q))

        # Act
        self.agent_a.revise_belief(Not(q))

        # Assert
        self.assertTrue(all([belief_a in self.agent_b.belief_base.beliefs for belief_a in self.agent_a.belief_base.beliefs]))

    @unittest.mock.patch('builtins.print')
    def test_agent_AGM_revision_inclusion_false(self, mock_print):
        # check if the belief base of agent_b is not a subset of agent_a
        # Arrange
        self.agent_a.add_belief(p)
        self.agent_a.add_belief(q)
        self.agent_a.add_belief(Implies(p, q))

        self.agent_b.add_belief(p)
        self.agent_b.add_belief(q)
        self.agent_b.add_belief(Implies(p, q))
        self.agent_b.add_belief(Not(q))

        # Act
        self.agent_a.revise_belief(Not(q))
        # Assert
        self.assertFalse(all([belief_b in self.agent_a.belief_base.beliefs for belief_b in self.agent_b.belief_base.beliefs]))


    @unittest.mock.patch('builtins.print')
    def test_agent_AGM_revision_vacuity_true(self, mock_print):
        # check if ~phi is not in the belief base then revision of B with phi is should be the same as B expanded with phi
        # Arrange
        self.agent_a.add_belief(p)
        self.agent_a.add_belief(Implies(p, q))
        self.agent_a.add_belief(q)

        self.agent_b.add_belief(p)
        self.agent_b.add_belief(Implies(p, q))

        # Act
        self.agent_b.revise_belief(q)

        # Assert
        self.assertEqual(self.agent_a.belief_base.beliefs, self.agent_b.belief_base.beliefs)

    @unittest.mock.patch('builtins.print')
    def test_agent_AGM_revision_vacuity_false(self, mock_print):
        # Arrange
        self.agent_a.add_belief(p)
        self.agent_a.add_belief(Implies(p, q))
        self.agent_a.add_belief(~q)

        self.agent_b.add_belief(p)
        self.agent_b.add_belief(Implies(p, q))

        # Act
        self.agent_b.revise_belief(~q)

        # Assert
        self.assertNotEqual(self.agent_a.belief_base.beliefs, self.agent_b.belief_base.beliefs)


    @unittest.mock.patch('builtins.print')
    def test_agent_AGM_revision_consistency_true(self, mock_print):
        #check if the belief base and phi is not contradictory then the revision of B with phi should still be consistent
        pass

    @unittest.mock.patch('builtins.print')
    def test_agent_AGM_revision_consistency_false(self, mock_print):
        pass


    @unittest.mock.patch('builtins.print')
    def test_agent_AGM_revision_extensionality_true(self, mock_print):
        # check if revision with [p] and [p || p] gives the same belief base
        pass

    @unittest.mock.patch('builtins.print')
    def test_agent_AGM_revision_extensionality_false(self, mock_print):
        pass
