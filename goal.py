class Goal:
    def __init__(self, exercise, target, date):
        self.exercise = exercise
        self.target = target
        self.date = date

    def CheckProgress(self, current_value):
        return current_value >= self.target

    def UpdateGoal(self,exercise, target, date):
        self.exercise = exercise
        self.target = target
        self.date = date
