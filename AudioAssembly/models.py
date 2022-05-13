from AudioAssembly import db

class element(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(100))

    def __init__(self, value):
        self.value = value