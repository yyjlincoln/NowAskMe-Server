from core.database import Post
import core.userlib
import secrets
import time
import utils.PrivacyControl


def get_post_by_postid(postid):
    p = Post.objects(postid__iexact=postid).first()
    return p


def new_post(uuid, content, posttype, privacy):
    postid = secrets.token_hex(16)
    p = Post(uuid=uuid, postid=postid, content=content,
             posttype=posttype, privacy=privacy, time=time.time())
    try:
        p.save()
        return postid
    except:
        return None


def get_stream(uuid):
    p = Post.objects(
        uuid__in=[*core.userlib.get_following_by_uuid(uuid), uuid]).order_by('-time')
    r = []
    for post in p:
        if utils.PrivacyControl.post_privacy(post.postid, uuid):
            r.append(post.postid)
    return r


def get_user_stream(uuid, target):
    p = Post.objects(uuid__iexact=target).order_by('-time')
    r = []
    for post in p:
        if utils.PrivacyControl.post_privacy(post.postid, uuid):
            r.append(post.postid)
    return r
