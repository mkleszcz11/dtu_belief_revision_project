

class BeliefBase:
    def __init__(self):
        self.beliefs = []
        self.belief_sets = []

    def add_belief(self, clause):
        self.beliefs.append(clause)
        self.belief_sets.append(set(clause))