class Exercise:
    def __init__(self, date,  name, repetitions=0, weight=0):
        self.date = date
        self.name = name
        self.repetitions = repetitions
        self.weight = weight

    def UpdateExercise(self, date, name, repetitions=None, weight=None):
        self.date = date
        self.name = name  
        self.repetitions = repetitions
        self.weight = weight
