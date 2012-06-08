'''
Json wrapper that provides traditional simplejson interface append
adds similar methods that supports mongoDB objects naitively.
'''

__all__ = ['dumps', 'loads', 'mongo_dumps', 'mongo_loads']

import datetime

try:
    import json
except ImportError:
    import simplejson as json

try:
    from pymongo import json_util
except ImportError:
    from bson import json_util

#TODO add Objectid support

ISOFORMAT = '%Y-%m-%dT%H:%M:%S.%f'

class JSONDateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        else:
            return json.JSONEncoder.default(self, obj)

def datetime_decoder(d, list):
    if isinstance(d, list):
        pairs = enumerate(d)
    elif isinstance(d, dict):
        pairs = d.items()

    result = []
    for k,v in pairs:
        if isinstance(v, basestring):
            v = datetime.datetime(v, ISOFORMAT)
        elif isinstance(v, (dict, list)):
            v = datetime_decoder(v)

        result.append((k,v))

    if isinstance(d, list):
        return [x[1] for x in result]
    elif isinstance(d, dict):
        return dict(result)


def dumps(obj):
    '''dumps Python object,that includes datetime objects, into JSON'''
    return json.dumps(obj)

def mongo_dumps(obj):
    '''transforms native pymongo objects into JSON'''
    return  json.dumps(obj, default = json_util.default)

def mongo_loads(obj):
    '''transforms JSON to into pymongo native objects'''
    return json.loads(obj, object_hook = json_util.object_hook)

def loads(obj):
    return json.loads(obj)

def test():
    timestamp = datetime.datetime.utcnow()
    mydate = datetime.date.today()

    data = dict(
                foo = 42,
                bar = [timestamp, mydate],
                date = mydate,
                timestamp = timestamp,
                struct = dict(
                        date2 = mydate,
                        timestamp2 = timestamp
                    )
            )
    print repr(data)
    jsonstring = dumps(data)
    print jsonstring
    print repr(loads(jsonstring))

if __name__ == '__main__':
    test()


