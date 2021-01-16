from core.database import Post


def get_post_by_postid(postid, uuid=None):
    p =  Post.objects(postid__iexact=postid).first()
    return p
