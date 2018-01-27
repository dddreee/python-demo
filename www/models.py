#!/user/bin/evv python3
# -*- coding: utf-8 -*-


'''
Models for user, blog, comment.
'''

import time, uuid

from orm import Model, StringField, BooleanField, FloatFlied, TextField

def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

class Net_Ease_Lrc(Model):
    __table__ = 'net_ease_lrc'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    song_id = StringField(ddl="varchar(50)")
    song_name = StringField(ddl="varchar(50)")
    singer_name = StringField(ddl="varchar(50)")
    lrc = StringField(ddl="varchar(3000)")
    usr_img = StringField(ddl="varchar(50)")
    cover_img = StringField(ddl="varchar(50)")

class User(Model):
    __table__ = 'users'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    email = StringField(ddl="varchar(50)")
    passwd = StringField(ddl="varchar(50)")
    admin = BooleanField()
    name = StringField(ddl="varchar(50)")
    image = StringField(ddl="varchar(500)")
    created_at = FloatFlied(default=time.time)
    
class Blog(Model):
    __table__ = 'blogs'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    user_id = StringField(ddl="varchar(50)")
    user_name = StringField(ddl="varchar(50)")
    user_image = StringField(ddl="varchar(500)")
    name = StringField(ddl="varchar(50)")
    summary = StringField(ddl="varchar(200)")
    content = TextField()
    created_at = FloatFlied(default=time.time)


class Comment(Model):
    __table__ = 'comments'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    blog_id = StringField(ddl='varchar(50)')
    user_id = StringField(ddl="varchar(50)")
    user_name = StringField(ddl="varchar(50)")
    user_image = StringField(ddl="varchar(500)")
    name = StringField(ddl="varchar(50)")
    content = TextField()
    created_at = FloatFlied(default=time.time)

