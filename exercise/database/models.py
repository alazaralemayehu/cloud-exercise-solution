from .db import db


class Professor(db.Document):
    name = db.StringField(max_length=20,required=True, unique=True)
    designation = db.StringField(required=True, choices=("Professor", "Assistant Professor", "Associate Professor"))
    email = db.StringField()
    interests = db.ListField(db.StringField(max_length=30))
    researchGroups = db.ListField(db.ReferenceField('ResearchGroup'))


class ResearchGroup(db.Document):
    name = db.StringField(max_length=20, required=True, unique=True)
    description = db.StringField()
    founder = db.ReferenceField('Professor', required=True, reverse_delete_rule=db.CASCADE,DBRef = False)

class Student(db.Document):
    name = db.StringField(required=True)
    studentNumber = db.StringField(required=True)
    researchGroups = db.ListField(db.ReferenceField('ResearchGroup'))
