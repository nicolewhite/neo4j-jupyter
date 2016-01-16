import os
import sys
import time
import requests
from py2neo import Graph, Relationship

graph = Graph()

graph.cypher.execute("CREATE CONSTRAINT ON (u:User) ASSERT u.username IS UNIQUE")
graph.cypher.execute("CREATE CONSTRAINT ON (t:Tweet) ASSERT t.id IS UNIQUE")
graph.cypher.execute("CREATE CONSTRAINT ON (h:Hashtag) ASSERT h.name IS UNIQUE")

TWITTER_BEARER = os.environ["TWITTER_BEARER"]

headers = dict(accept="application/json", Authorization="Bearer " + TWITTER_BEARER)

payload = dict(
    count=100,
    result_type="recent",
    lang="en",
    q=sys.argv[1]
)

base_url = "https://api.twitter.com/1.1/search/tweets.json?"


def find_tweets(since_id):
    payload["since_id"] = since_id
    url = base_url + "q={q}&count={count}&result_type={result_type}&lang={lang}&since_id={since_id}".format(**payload)

    r = requests.get(url, headers=headers)
    tweets = r.json()["statuses"]

    return tweets


def upload_tweets(tweets):
    for t in tweets:
        u = t["user"]
        e = t["entities"]

        tweet = graph.merge_one("Tweet", "id", t["id"])
        tweet.properties["text"] = t["text"]
        tweet.push()

        user = graph.merge_one("User", "username", u["screen_name"])
        graph.create_unique(Relationship(user, "POSTS", tweet))

        for h in e.get("hashtags", []):
            hashtag = graph.merge_one("Hashtag", "name", h["text"].lower())
            graph.create_unique(Relationship(hashtag, "TAGS", tweet))

        for m in e.get('user_mentions', []):
            mention = graph.merge_one("User", "username", m["screen_name"])
            graph.create_unique(Relationship(tweet, "MENTIONS", mention))

        reply = t.get("in_reply_to_status_id")

        if reply:
            reply_tweet = graph.merge_one("Tweet", "id", reply)
            graph.create_unique(Relationship(tweet, "REPLY_TO", reply_tweet))

        ret = t.get("retweeted_status", {}).get("id")

        if ret:
            retweet = graph.merge_one("Tweet", "id", ret)
            graph.create_unique(Relationship(tweet, "RETWEETS", retweet))


since_id = -1

while True:
    try:
        tweets = find_tweets(since_id=since_id)

        if not tweets:
            print "No tweets found."
            time.sleep(60)
            continue

        since_id = tweets[0].get("id")
        upload_tweets(tweets)

        print "{} tweets uploaded!".format(len(tweets))
        time.sleep(60)

    except Exception, e:
        print e
        time.sleep(60)
        continue