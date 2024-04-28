import unittest
import unittest.mock
from copy import copy
from solver import Solver
from belief_base import Belief
from belief_revision_agent import BeliefRevisionAgent
from sympy import symbols, Not, Or, And, Equivalent, Implies

A, B, C, D, p, q, r, s, a, b, c = symbols('A B C D p q r s a b c')

class TestAGMPostulatesPartA(unittest.TestCase):
    def setUp(self):
        self.agent_a = BeliefRevisionAgent()
        self.agent_b = BeliefRevisionAgent()


    @unittest.mock.patch('builtins.print') # just to hide the prints
    def test_agent_AGM_revision_success_true(self, mock_print):
        # check if the belief base is updated with the new belief
        # Arrange
        self.agent_a.add_belief(A)
        expected_clause = [[(True, 'A')], [(True, 'B')], [(True, 'C')]]
        # Act
        self.agent_a.add_belief_with_revision((A & B & C))
        # Assert
        self.assertTrue(any([expected_clause == belief.clause for belief in self.agent_a.belief_base.beliefs]))

    @unittest.mock.patch('builtins.print')
    def test_agent_AGM_revision_success_false(self, mock_print):
        # check if the belief base is not updated with random belief
        # Arrange
        self.agent_a.add_belief(A)
        # Act
        self.agent_a.add_belief_with_revision(B)
        # Assert
        self.assertNotEqual(self.agent_a.belief_base.beliefs, [[A], [C]])


    @unittest.mock.patch('builtins.print')
    def test_agent_AGM_revision_inclusion_true(self, mock_print):
        # check if the belief base of agent_a is a subset of agent_b
        # Arrange
        self.agent_a.add_belief(p)
        self.agent_a.add_belief(q)
        self.agent_a.add_belief(Implies(p, q))

        agent_b_beliefs = [
            [[(True, 'p')]],
            [[(True, 'q')]],
            [[(True, 'q'), (False, 'p')]],
            [[(False, 'q')]]
            ]

        # Act
        self.agent_a.add_belief_with_revision(Not(q))

        # Assert

        # All beliefs in agent_a should be in agent_b
        for belief_a in self.agent_a.belief_base.beliefs:
            match = False
            for belief_b in agent_b_beliefs:
                if belief_a.clause == belief_b:
                    match = True
            self.assertTrue(match)

    @unittest.mock.patch('builtins.print')
    def test_agent_AGM_revision_inclusion_false(self, mock_print):
        # check if the belief base of agent_b is not a subset of agent_a
        # Arrange
        self.agent_a.add_belief(p)
        self.agent_a.add_belief(q)
        self.agent_a.add_belief(Implies(p, q))

        agent_b_beliefs = [
            [[(True, 'p')]],
            [[(True, 'q')]],
            [[(True, 'q'), (False, 'p')]],
            [[(False, 'q')]]
            ]

        # Act
        self.agent_a.add_belief_with_revision(Not(q))

        # Assert
        # at least one belief in agent_b should not be in agent_a
        matches = []
        for belief_b in agent_b_beliefs:
            match = False
            for belief_a in self.agent_a.belief_base.beliefs:
                if belief_a.clause == belief_b:
                    print(belief_a.clause)
                    match = True
            matches.append(match)

        # passes if there is at least one true in the matches list
        self.assertTrue(any(matches))
        # passes if there is at least one false in the matches list
        self.assertFalse(all(matches))



    @unittest.mock.patch('builtins.print')
    def test_agent_AGM_revision_vacuity_true(self, mock_print):
        # check if ~phi is not in the belief base then revision of B with phi is should be the same as B expanded with phi
        # Arrange
        self.agent_a.add_belief(p)
        self.agent_a.add_belief(Implies(p, q))

        agent_b_beliefs = [
            [[(True, 'p')]],
            [[(True, 'q'), (False, 'p')]],
            [[(True, 'q')]]
            ]

        # Act
        self.agent_a.add_belief_with_revision(q)

        # Assert
        agent_a_beliefs = [belief.clause for belief in self.agent_a.belief_base.beliefs]
        self.assertEqual(agent_a_beliefs, agent_b_beliefs)

    @unittest.mock.patch('builtins.print')
    def test_agent_AGM_revision_vacuity_false(self, mock_print):
        # Arrange
        self.agent_a.add_belief(p)
        self.agent_a.add_belief(Implies(p, q))

        agent_b_beliefs = [
            [[(True, 'p')]],
            [[(True, 'q'), (False, 'p')]],
            [[(False, 'q')]]
            ]

        # Act
        self.agent_a.add_belief_with_revision(~q)

        # Assert
        agent_a_beliefs = [belief.clause for belief in self.agent_a.belief_base.beliefs]
        self.assertNotEqual(agent_a_beliefs, agent_b_beliefs)


    # @unittest.mock.patch('builtins.print')
    # def test_agent_AGM_revision_consistency_true(self, mock_print):
    #     #check if the belief base and phi is not contradictory then the revision of B with phi should still be consistent
    #     pass

    # @unittest.mock.patch('builtins.print')
    # def test_agent_AGM_revision_consistency_false(self, mock_print):
    #     pass


    @unittest.mock.patch('builtins.print')
    def test_agent_AGM_revision_extensionality_true(self, mock_print):
        # check if revision with [p] and [p || p] gives the same belief base
        # Arrange
        self.agent_a.add_belief(q)

        agent_b_beliefs = [
            [[(True, 'q')]],
            [[(True, 'p')]]
        ]

        # Act
        self.agent_a.add_belief_with_revision(Or(p, p))

        # Assert
        agent_a_beliefs = [belief.clause for belief in self.agent_a.belief_base.beliefs]
        self.assertEqual(agent_a_beliefs, agent_b_beliefs)


    @unittest.mock.patch('builtins.print')
    def test_agent_AGM_revision_extensionality_false(self, mock_print):
        # Arrange
        self.agent_a.add_belief(q)

        agent_b_beliefs = [
            [[(True, 'q')]],
            [[(True, 'p')], [(True, 'p')]]
        ]

        # Act
        self.agent_a.add_belief_with_revision(Or(p, p))

        # Assert
        agent_a_beliefs = [belief.clause for belief in self.agent_a.belief_base.beliefs]
        self.assertNotEqual(agent_a_beliefs, agent_b_beliefs)


class TestAGMPostulatesPartB(unittest.TestCase):
    @unittest.mock.patch('builtins.print')
    def setUp(self, mock_print):
        self.agent = BeliefRevisionAgent()
        self.agent.add_belief(s,0.2)
        self.agent.add_belief(a,0.2)
        self.agent.show_beliefs(pretty=False)

    @unittest.mock.patch('builtins.print')
    def test_agent_AGM_consitency(self, mock_print):
        # Arrange
        phi = BeliefRevisionAgent()
        phi.add_belief(s, 0.2)

        solver =  Solver()
        solver1 = Solver()
        # phi = BeliefRevisionAgent()
        # Add all beliefs to the solver
        for belief in phi.belief_base.beliefs:
            solver.add_belief(belief)
            print(solver.resolution())

        # Act
        #check phi is consistent or not
        phi_consistent = solver.check_clauses()

        # Assert
        if  phi_consistent:
            print("q")
            return False

        B1 = copy(self.agent)
        B1.show_beliefs(pretty=False)
        for belief in phi.belief_base.beliefs:
            B1.revise_belief(belief)
            B1.show_beliefs(pretty=False)
            for belief in phi.belief_base.beliefs:
                solver1.add_belief(belief)
                new = solver1.resolution()
                self.assertFalse(new)

    @unittest.mock.patch('builtins.print')
    def test_agent_AGM_extensionality(self, mock_print):
        # Arrange
        x = BeliefRevisionAgent()
        y = BeliefRevisionAgent()
        x.add_belief(s,0.2)
        y.add_belief(s,0.2)
        # Act
        B2 = copy(self.agent)
        B3 = copy(self.agent)
        for belief in x.belief_base.beliefs:
            B2.revise_belief(belief)
        for belief in y.belief_base.beliefs:
            B3.revise_belief(belief)
        # Assert
        beliefs_B2 = [belief.clause for belief in B2.belief_base.beliefs]
        beliefs_B3 = [belief.clause for belief in B3.belief_base.beliefs]
        self.assertEqual(beliefs_B2, beliefs_B3)
