from .player import Player


class Captain(Player):
    def __init__(self, id=0, firstname=None, lastname=None, age=0, experience=None, grade=0):
        super().__init__(id, firstname, lastname, age, experience)
        self.grade = grade

    def input(self, data):
        super().input(data)
        self.grade = data.get("grade")
