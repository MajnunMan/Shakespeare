import codecs
import collections
import csv
import json
import numpy as np
import pandas as pd
import datetime as dt
import time

from sklearn import preprocessing
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
        # Create CSV
        #process('food')
        #process('sport')

        # Order by rating
        #ratingOrder('food.csv')
        #ratingOrder('sport.csv')

        # Normalize rating
        #normalize("food.csv")
        normalize("sport.csv")


def process(category):
    # Save the retrieved tweets to file:
    dict_list = []
    for tweet in query_tweets(category, limit=3000, begindate=dt.date(2013, 1, 1), enddate=dt.date(2014, 1, 1),
                              poolsize=100, lang='en'):
        # print(json.dumps(tweet, cls=JSONEncoder))

        # Eliminate unnecessary fields from tweet
        optimised_data = optimiser(json.dumps(tweet, cls=JSONEncoder),
                                   unnecessary_field=['fullname', 'timestamp'])
        dict_list.append(optimised_data)

    # Sorting tweets by rating (likes + replies + retweets)
    sorted_dict = sorted(dict_list, key=lambda d: d['rating'], reverse=True)
    timestr = time.strftime("%Y%m%d-%H%M%S")
    dictToCSV(category + "-data" + timestr + ".csv", sorted_dict[0].keys(), sorted_dict)

    return


def optimiser(data, unnecessary_field=None):
    # Convert string to dict
    tweet = json.loads(data)
    if unnecessary_field is not None:
        for data in unnecessary_field:
            tweet.pop(data, None)
    array = np.array([int(tweet['likes']), int(tweet['replies']), int(tweet['retweets'])])
    tweet['rating'] = np.mean(array)

    return tweet


def dictToCSV(csv_file, csv_columns, dict_data):
    with codecs.open(csv_file, 'w', "utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in dict_data:
            writer.writerow(data)
    return


def normalize(csv):
    # Normalization
    data = pd.read_csv(csv)
    rating_norm = preprocessing.MinMaxScaler().fit_transform(data[['rating']])
    data['rating_norm'] = rating_norm
    data.to_csv(csv)

    return


def ratingOrder(csv):
    # Sort combined CSV by rating
    df = pd.read_csv(csv, delimiter=',')
    data = df.sort_values(by='rating', ascending=False)
    data.to_csv(csv, encoding='utf-8')

    return

main()
