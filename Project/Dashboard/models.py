from Dashboard import db

class User(db.Model):
    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    google_accessToken = db.Column(db.String, default='')
    is_googleConnected =  db.Column(db.Boolean, default=False)
    google_widget1 =  db.Column(db.Boolean, default=False)
    google_widget2 = db.Column(db.Boolean, default=False)
    twitter_accessToken = db.Column(db.String, default='')
    twitter_accessTokenSecret = db.Column(db.String, default='')
    is_twitterConnected =  db.Column(db.Boolean, default=False)
    twitter_widget1 = db.Column(db.Boolean, default=False)
    widget1 =  db.Column(db.Boolean, default=False)
    widget2 =  db.Column(db.Boolean, default=False)
    widget3 =  db.Column(db.Boolean, default=False)

    def __init__(self, uuid, username, password):
        self.id = uuid
        self.username = username
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


