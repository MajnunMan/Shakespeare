import codecs
import collections
import csv
import datetime as dt
import json

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

    if __name__ == '__main__':
        # Or save the retrieved tweets to file:
        dict_list = []
        for tweet in query_tweets("food", limit=1000, begindate=dt.date(2017, 1, 1), poolsize=100, lang='en'):
            # print(json.dumps(tweet, cls=JSONEncoder))

            # Eliminate unnecessary fields from tweet
            optimised_data = optimiser(json.dumps(tweet, cls=JSONEncoder), unnecessary_field=['fullname', 'timestamp'])
            dict_list.append(optimised_data)
        dictToCSV("data\\food-data.csv", dict_list[0].keys(), dict_list)

        dict_list.clear()
        for tweet in query_tweets("sport", limit=1000, begindate=dt.date(2017, 1, 1), poolsize=100, lang='en'):
            # print(json.dumps(tweet, cls=JSONEncoder))

            # Eliminate unnecessary fields from tweet
            optimised_data = optimiser(json.dumps(tweet, cls=JSONEncoder), unnecessary_field=['fullname', 'timestamp'])
            dict_list.append(optimised_data)
        dictToCSV("data\\sport-data.csv", dict_list[0].keys(), dict_list)


def optimiser(data, unnecessary_field=None):
    # Convert string to dict
    tweet = json.loads(data)
    if unnecessary_field is not None:
        for data in unnecessary_field:
            tweet.pop(data, None)

    return tweet


def dictToCSV(csv_file, csv_columns, dict_data):
    with codecs.open(csv_file, 'w', "utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in dict_data:
            writer.writerow(data)
    return


main()
