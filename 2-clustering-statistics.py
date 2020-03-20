import pandas as pd
import joblib

df = pd.read_pickle("tweets.pkl")
df = df.drop_duplicates(subset="id_str")

km = joblib.load("km-clusters.pkl")

clusters = km.labels_.tolist()
df["cluster"] = clusters

df.to_pickle("df_with_cluster.pkl")
cluster_counts = df["cluster"].value_counts().sort_index()

for i in range(0, 8):
    df_c = df.loc[df["cluster"] == i]

    entities = df_c["entities"]
    hashtags = {}
    user_mentions = {}

    for e in entities:
        if(len(e["hashtags"]) > 0):
            ht = e["hashtags"][0]["text"]
            if (ht in hashtags):
                hashtags[ht] += 1
            else:
                hashtags[ht] = 1
        if (len(e["user_mentions"]) > 0):
            mention  = e["user_mentions"][0]["screen_name"]
            if (mention in user_mentions):
                user_mentions[mention] += 1
            else:
                user_mentions[mention] = 1
    
    sorted_ht = sorted(hashtags, key = hashtags.get, reverse = True)
    sorted_um = sorted(user_mentions, key = user_mentions.get, reverse = True)

    df_users = df_c["user"]
    users = {}

    for u in df_users:
        user = u["screen_name"]
        if (user in users):
            users[user] += 1
        else:
            users[user] = 1
    
    sorted_u = sorted(users, key = users.get, reverse = True)

    print("---")
    print("Cluster", i)
    print("Number of tweets:", df_c.shape[0])
    print("Number of independent accounts:", len(users.keys()))
    print("Hashtags:", sorted_ht[:10])
    print("Users:", sorted_u[0:10])
    print("Mentions:", sorted_um[0:10])