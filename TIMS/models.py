from run import dbAlchemy

ROLE_USER = 0
ROLE_ADMIN = 1

class User(dbAlchemy.Model):
    id = dbAlchemy.Column(dbAlchemy.Integer, primary_key = True)
    nickname = dbAlchemy.Column(dbAlchemy.String(64), unique = True)
    email = dbAlchemy.Column(dbAlchemy.String(120), unique = True)
    posts = dbAlchemy.relationship('Post', backref = 'author', lazy = 'dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Post(dbAlchemy.Model):
    id = dbAlchemy.Column(dbAlchemy.Integer, primary_key = True)
    body = dbAlchemy.Column(dbAlchemy.String(140))
    timestamp = dbAlchemy.Column(dbAlchemy.DateTime)
    user_id = dbAlchemy.Column(dbAlchemy.Integer, dbAlchemy.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)