from app import db
import datetime
class ms_mi_log(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    ip = db.Column(db.String(64))
    rc = db.Column(db.BigInteger)
    uin = db.Column(db.String(64))
    mbox = db.Column(db.String(120))
    des = db.Column(db.String(800))
    def __repr__(self):
        return '<ms_mi_log %r>' % (self.ip)

class total_log(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.String(64))
    app_name = db.Column(db.String(64))
    total = db.Column(db.BigInteger)


    def __repr__(self):
        return '<total_log %r>' % (self.ip)