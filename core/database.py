import mongoengine as me


class User(me.Document):
    uuid = me.StringField(unique=True, primary=True)  # This will never change
    userid = me.StringField()
    name = me.StringField()

class UserPrivate(me.Document):
    uuid = me.StringField(unique=True, primary=True)  # This will never change
    email = me.EmailField(unique=True)
    registerationTime = me.FloatField()

class EmailVerification(me.Document):
    email = me.StringField(unique=True, required = True)
    verification=me.StringField(required = True)
    timestamp = me.FloatField()