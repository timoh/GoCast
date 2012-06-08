'''
Includes database models for Idea main view and for dataobject of ideas.
'''

import mongokit
from mongokit import OR, NOT, IS
from datetime import datetime

from pymongo.objectid import ObjectId
from pymongo.dbref import DBRef

DATABASE = "ideabag"
db = None
conn = None


def register(conn):
    #update this list manually, if you add new model
    if conn:
        conn.register([Meta, User, Action, Idea, Revision, Chat])

def make_conn(host = "192.168.100.6", port = 27017):
    '''do local connection'''
    conn = mongokit.Connection(host, port)
    register(conn)
    return conn



class Meta(mongokit.Document):
    '''holds all metadata,like when data is created, changed and etc'''
    __database___ = DATABASE
    __collection__ = "metas"
    structure = {
        "created" : datetime,
        "changed" : datetime,
        "deleted" : datetime,
        "ip"      : unicode,
        "client"  : unicode,
    }
    default_values = {
        "created" : datetime.utcnow(),
        "changed" : datetime.utcnow()
    }


class User(mongokit.Document):
    ''' '''
    __database___ = DATABASE
    __collection__ = 'users'

    structure = {
        "name"      : unicode,
        "email"     : unicode,
        "friends"   : list, #list of FB friends, who are using system
        "is_banned" : bool,
        "avatar"   : unicode,
        "social" : {
                "link" : unicode,
                "id"    : unicode,
        },
        "stats" : dict,
    }


    default_values = {
        "is_banned" : False,
        "stats": {
            "upvotes" : 0,
            "follows" : 0,
            "investments" : 0.0,
            "edits" : 0,
            "translations": 0,
            "flags" : 0,
            "ideas"    : 0,
            "rankings" : []
            }
    }

class Action(mongokit.Document):
    '''holds activity log about some specific activity with Idea
    Action activity is name of activity, which involved/happend with the idea.
    Example actions are just singular verbs:
        upvote, follow, invest, etc
    '''
    __database___ = DATABASE
    __collection__ = 'actions'

    structure = {
        "activator"     : ObjectId,
        "action"      : unicode,
        "subject"       : ObjectId,
        "subject_author" : None, #or objectid, if there exists owner
        "amount"        : float,
        "added"         : datetime
    }

    default_values = {
        "added" : datetime.utcnow(),
        "amount": 0.0,
    }


class Chat(mongokit.Document):
    '''user conversation ''' 
    __database__ = DATABASE
    __collection__ = "chats"

    structure = {
        "author" : ObjectId,
        "content" : unicode,
        "subject" : ObjectId,
        "added" : datetime,
    }

class Revision(mongokit.Document):
    ''' Holds revision changes'''
    __database___ = DATABASE
    __collection__ = "revisions"

    structure = {
        "author" : ObjectId,
        "original" : ObjectId,
        "is_source" :  bool,
        "closed"  : bool,
        "accepted": bool,
        "difference" : int,
        "length" : int,
        "patch": unicode,
        "content" : unicode, #if difference >= original.length, then we'll hold new original
        "message" : unicode,
        "comments" : list,
        "votes" : list,
        "added" : datetime,
    }

    default_values = {
        "is_source" : False,
        "closed" : False,
        "accepted" : False,
        "content" :  u"",
        "difference" : -1,
        "added" : datetime.utcnow(),
    }


class Idea(mongokit.Document):
    '''Holds an Idea'''
    __database___ = DATABASE
    __collection__= "ideas"

    structure = {
        "author"      : ObjectId,
        "is_active"   : bool,
        "visibility"  : int,
        "status"      : unicode,
        "punchline"   : unicode,
        "content"     : unicode,
        "problem"     : unicode, 
        "tags"        : list,
        "chats"       : list,

        #-- META DATA
        "translations" : list, # objectid to translated object
        "language"    : unicode,
        "encoding"    : unicode,
        "revisions"   : dict,
        "added"       : datetime,
        "edited"      : datetime,
        "stats"  : {
            'follows'     : int,
            'upvotes'     : int,
            'shares'      : int,
            'bookmarks'   : int,
            'investments' : float,
            'edits'    : int,
        }
    }

    default_values = {
         "added"          : datetime.utcnow(),
         "is_active"      : True,
         "visibility"     : 1,
         "language"       : u"en",
         "encoding"       : u"utf8",
         "stats"    : {
            'followers'   : 0,
            'upvotes'     : 0,
            'shares'      : 0,
            'hangouts'   : 0,
            'investments' : 0,
            'edits'    : 1
            }
    }
    use_dot_notation = True

