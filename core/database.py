import mongoengine as me


class User(me.Document):
    uuid = me.StringField(unique=True, primary=True,
                          required=True)  # This will never change
    userid = me.StringField()
    name = me.StringField(default="user")
    description = me.StringField(default="")


class UserPrivate(me.Document):
    uuid = me.StringField(unique=True, primary=True, required=True)
    email = me.EmailField(unique=True)
    registerationTime = me.FloatField()


class EmailVerification(me.Document):
    email = me.StringField(unique=True, required=True)
    otp = me.StringField(required=True)
    timestamp = me.FloatField(required=True)
    scope = me.StringField(required=True)
    attemptsLeft = me.IntField(default=4)


class Token(me.EmbeddedDocument):
    token = me.StringField(required=True)
    scope = me.StringField(required=True)
    expiry = me.FloatField(required=True)


class UserStatus(me.Document):
    uuid = me.StringField(unique=True, required=True)
    tokens = me.EmbeddedDocumentListField(Token, default=[])


class UserRelations(me.Document):
    uuid = me.StringField(unique=True, required=True)
    # A list of uuids that the user is following
    following = me.ListField(me.StringField(), default=[])
    pinned = me.ListField(me.StringField(), default=[])


# class QRLogin(me.Document):
#     requestid = me.StringField(unique=True, required=True)
#     status = me.IntField(default=0)
#     # -1: rejected
#     # 0: not authenticated
#     # 1: scanned, approval needed
#     #
#     expiry = me.FloatField()
#     uuid = me.StringField()
#     scope = me.StringField()

# class Biometrics(me.Document):
#     deviceid = me.StringField(unique = True, required = True)
#     uuid = me.StringField()
#     challenge = me.StringField()
#     pubkey = me.StringField()
#     counter = me.IntField()

# class Box(me.Document):
#     uuid = me.StringField() # UUID of user
#     boxid = me.StringField() # ID of the box
#     name = me.StringField() # Name of the box
#     description = me.StringField() # Box description
#  # At this stage, allow only 1 box for each user.

class Post(me.Document):
    uuid = me.StringField()
    postid = me.StringField(unique=True)
    posttype = me.StringField()
    content = me.StringField()
    time = me.FloatField()
    privacy = me.StringField(default='inherit')


class UserPrivacy(me.Document):
    uuid = me.StringField(unique=True, required=True)
    post = me.StringField(default='public')
    dm = me.StringField(default='public')
    # search-with options
