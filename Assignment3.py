from datetime import datetime, timezone
import pandas as pd
import matplotlib.pyplot as plt
import tweepy
from datetime import date

consumer_key = "tX6x8Kz0ntLLTEB6P2y5b64nB"
consumer_secret = "ppgkCA7OR8DKjUwE7yTfy7oCwDSHa80WsdgDHhaohPwN0SonXJ"
access_token = "1457374016277303297-dNg6ino7PdGr90uHK0lxfXXpzgFq5l"
access_token_secret = "j9a4mXWXifdR5m7DSrXXdaXFD2V6tT3HCIFVprzHcR9PT"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)
tag = "#MahsaAmini"

# 2A
tweets = tweepy.Cursor(api.search_tweets, q=tag).items(1001)
tweet_count = sum(1 for tweet in tweets)
if(tweet_count > 1000):
    print("More than 1000 tweets with #MahsaAmini")
else:
    print(tweet_count, "tweets with #MahsaAmini")

# 2B

today = date.today()
tweets = tweepy.Cursor(api.search_tweets, q=tag, until=today).items()
dataset = []
for tweet in tweets:
    tweet_info = {
        'Tweet ID': tweet.id,
        'Twitter ID': tweet.user.screen_name,
        'Tweet': tweet.text,
        'Created Date': tweet.created_at
        }
    dataset.append(tweet_info)
dataframe = pd.DataFrame(dataset)
dataframe['Day'] = dataframe['Created Date'].dt.to_period('D')
count = dataframe.groupby('Day').size()
print(len(count))

count.plot(kind='bar', xlabel='Day', ylabel='Number of Tweets')
plt.title('Number of Tweets with #MahsaAmini in the Past 7 Days')
plt.show()


# 2C
tweets = tweepy.Cursor(api.search_tweets, q=tag, lang='en').items(20)
for tweet in tweets:
    print("Tweet ID:", tweet.id, "\nTwitter ID:", tweet.user.screen_name, "\nTweet:", tweet.text, "\nCreated Date:", tweet.created_at)
    print("-" * 40, "\n")

# 2D 
tweets = tweepy.Cursor(api.search_tweets, q=tag, result_type = "recent").items(10)
for tweet in tweets:
    print("Tweet ID:", tweet.id, "\nTwitter ID:", tweet.user.screen_name, "\nTweet:", tweet.text, "\nCreated Date:", tweet.created_at)
    print("-" * 40, "\n")

# 2E
tweets = tweepy.Cursor(api.search_tweets, q=tag).items(300)
id = []
for tweet in tweets:
    id.append(tweet.user.id_str)
    if len(id) == 50:
        break
print(id)

#3A
account = "IUBloomington"
tweets = api.user_timeline(screen_name=account, count="50")
Tweets, Time = [], []
for tweet in tweets:
    Tweets.append(tweet.text)
    Time.append(tweet.created_at)
data = pd.DataFrame({"Tweets": Tweets, "Time": Time})
print(data)

# 3B
data.to_csv("tweets.csv",columns=["Tweets","Time"], index=False)