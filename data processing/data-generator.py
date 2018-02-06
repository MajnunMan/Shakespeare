import collections
import datetime as dt
import json
import settings
import os

import sys
from twitterscraper.query import query_tweets

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__json__'):
            return obj.__json__()
        elif isinstance(obj, collections.Iterable):
            return list(obj)
        elif isinstance(obj, dt.datetime):
            return obj.isoformat()
        elif hasattr(obj, '__getitem__') and hasattr(obj, 'keys'):
            return dict(obj)
        elif hasattr(obj, '__dict__'):
            return {member: getattr(obj, member)
                    for member in dir(obj)
                    if not member.startswith('_') and
                    not hasattr(getattr(obj, member), '__call__')}

        return json.JSONEncoder.default(self, obj)


def main():
    # Print out tweets
    """list_of_tweets = query_tweets("Sport", 10)
    # print the retrieved tweets to the screen:
    for tweet in query_tweets("Sport", 10):
        print(json.dumps(tweet, cls=JSONEncoder))"""

    if __name__ == '__main__':
        # Or save the retrieved tweets to file:
        file = open("data\\food-data.txt", "w")
        for tweet in query_tweets("food", limit=1000, begindate=dt.date(2016, 1, 1), poolsize=10):
            # print(json.dumps(tweet, cls=JSONEncoder))
            file.write(json.dumps(tweet, cls=JSONEncoder) + "\n")
        file.close()

        file = open("data\\sport-data.txt", "w")
        for tweet in query_tweets("sport", limit=1000, begindate=dt.date(2016, 1, 1), poolsize=10):
            # print(json.dumps(tweet, cls=JSONEncoder))
            file.write(json.dumps(tweet, cls=JSONEncoder) + "\n")
        file.close()


main()
