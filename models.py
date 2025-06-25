class User: 
    def __init__(self, name, email, role):
        self.name = name
        self.email = email
        self.role = role
        self.skills_has = []
        self.skills_wants = []

class Match: 
    def __init__(self, mentor_id, mentee_id, score):
        self.mentor_id = mentor_id
        self.mentee_id = mentee_id
        self.score = score # it's a numeric value that helps us rank or choose better mentor–mentee pairs.