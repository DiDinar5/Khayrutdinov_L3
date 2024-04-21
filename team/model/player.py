class Player:
    def __init__(self, id=0, firstname=None, lastname=None, age=0, experience=None):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.experience = experience

    def input(self, data):
        self.id = data.get('id')
        self.firstname = data.get('firstname')
        self.lastname = data.get('lastname')
        self.age = data.get('age')
        self.experience = data.get('experience')
