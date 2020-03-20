import sys
import time
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import math
import joblib

df = pd.read_pickle("tweets.pkl")
print(df.shape)

start = time.time()

text = df["full_text"]
tfidf_vectorizer = TfidfVectorizer(max_df=0.4, stop_words='english', use_idf=True, max_features=100000)
tfidf_matrix = tfidf_vectorizer.fit_transform(text)

end = time.time()

print(f'Time to perform Tfidf: {round(end - start)}')
print(tfidf_matrix.shape)

start = time.time()

km = KMeans(n_clusters=8)
km.fit(tfidf_matrix)
joblib.dump(km, "km-clusters.pkl")
end = time.time()
print(f'Time to perform K-means: {round(end - start)}')
print("km-clusters.pkl saved")