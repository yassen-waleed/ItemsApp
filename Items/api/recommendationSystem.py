def important_features(datasets):
    data = datasets.copy()
    for i in range(0, datasets.shape[0]):
        data["imp"] = data["name"].apply(str) + " " + data["location"].apply(str) + " " + data["price"].apply(
            str) + " " + data[
                          "reserved"].apply(str) + " " + data["rate"].apply(str) + " " + data["types"].apply(str)
    return data


import re
from urllib.request import urlopen

import json
import pandas as pd

url = "http://127.0.0.1:8000/item/items/"

response = urlopen(url)

data = json.loads(response.read())
pd.options.display.width = 0
dataf = pd.json_normalize(data, record_prefix='_')
dataf["types"] = [re.sub(r"[\([{})\]]", '', str(types)) for types in dataf.types]
dataf["types"] = [re.sub(r"""['"]+""", '', str(types)) for types in dataf.types]
dataf.drop("images", axis=1, inplace=True)
dataf.drop("amenities", axis=1, inplace=True)
dataf.drop("vendor_id", axis=1, inplace=True)
dataf.drop("about", axis=1, inplace=True)
dataf.drop("link", axis=1, inplace=True)

dataf.drop("phone", axis=1, inplace=True)
dataf.drop("address", axis=1, inplace=True)
dataf.drop("availability_date", axis=1, inplace=True)

dataf.shape

dataf.info()

data = important_features(dataf)

data["ids"] = [i for i in range(0, data.shape[0])]

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

vec = TfidfVectorizer()

vecs = vec.fit_transform(data["imp"].apply(lambda x: np.str_(x)))

vecs.shape

from sklearn.metrics.pairwise import cosine_similarity

sim = cosine_similarity(vecs)

sim.shape


def recommend(imp):
    venue_id = data[data.imp == imp]["ids"].values[0]
    scores = list(enumerate(sim[venue_id]))
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    sorted_scores = sorted_scores[0:]
    venues = [data[venues[0] == data["ids"]]["id"].values[0] for venues in sorted_scores]
    return venues



lst = recommend("Beverly Banquets rammallah 3600 False 0 id: 1, type_name: Banquet")

for i in lst:
    print(i)
