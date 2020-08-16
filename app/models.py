from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    description = db.Column(db.String(140), index=True, default='')
    done = db.Column(db.Boolean, index=True, default=False)

    def __repr__(self):
        return f'Task {self.id}\
                \nTitle: {self.title}\
                \nDescription: {self.description}'