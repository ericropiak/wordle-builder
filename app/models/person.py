from .database import db


class Person(db.Model):
    """Person Table."""

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Person {self.name}>"