# Create twitter steamer that monitors tweets related to a given keyword
import tweepy
from tweepy.auth import OAuthHandler
import csv
import config

# streamTerm = "National Cyber League"
streamTerm = "Python" # Terms that you are wanting to listen for. Python is the sample term
outputFile = "StreamTest.csv"

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if 'RT @' not in status.text: # find what attribute can be used to get the retweet status
            print("Original Tweet ||| " + status.user.name + " ||| " + status.text)
        
        # Do not need to specify if they are retweets are not. Retweets are being filtered out. 
            try:
                writeToFile(outputFile, getOutput(streamTerm, "Tweet", status.user.name, status.user.screen_name, status.extended_tweet['full_text'], status.id_str, status.created_at, status.lang, status.user.location, status.place))
            except AttributeError:
                writeToFile(outputFile, getOutput(streamTerm, "Tweet", status.user.name, status.user.screen_name, status.text, status.id_str, status.created_at, status.lang, status.user.location, status.place))
        else:
            print("Retweeted Tweet ||| " + status.user.name + " ||| " + status.text)
            try:
                writeToFile(outputFile, getOutput(streamTerm, "Retweet", status.user.name, status.user.screen_name, status.extended_tweet['full_text'], status.id_str, status.created_at, status.lang, status.user.location, status.place))
            except AttributeError:
                writeToFile(outputFile, getOutput(streamTerm, "Retweet", status.user.name, status.user.screen_name, status.text, status.id_str, status.created_at, status.lang, status.user.location, status.place))                

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_error disconnects the stream
            return False
        #returning True reconnects the stream, with backoff

def writeToFile(file, outputArray):
    with open(file, mode='a') as tweets:
        tweetWriter = csv.writer(tweets, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        tweetWriter.writerow(outputArray)                               
        tweets.close()

def getOutput(streamTerm, tweetType, user, screen_name, text, id, created, lang, userLoc, place ):
    output = [streamTerm, tweetType, user, screen_name, text, id, created, lang, userLoc, place]
    return output

collectStreamData = True
inputString = ""

auth = OAuthHandler(config.consumer_key, config.consumer_secret)# create authorization 
auth.set_access_token(config.access_token, config.access_secret)

print("Connected to Twitter\n")

# while True:
api = tweepy.API(auth, wait_on_rate_limit=True)# connect to twitter api
# while(collectStreamData):
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener = myStreamListener)# creates a stream listener to begin searching for tweets

print("Searching for term: " + streamTerm)

running = False

#---------------------------------------------
#Ctrl + C to stop program running in terminal
#---------------------------------------------

while(True): # search for tweets matching the streamTerm, and if rate limit is hit, it will wait for an amount of time before starting again.
    try:
        if(running == False):
            print("Beginning Twitter Stream")
            myStream.filter(track=[streamTerm, "-filter:retweets", "tweet_mode=extended"], is_async=True)
            running = True
    except TweepError: # when the rate limit is reached, it should return an error, and then wait for a specified time to continue running.  
        print("Rate Limit Exceeded...Beginning sleep")
        time.sleep(60 * 15)
        running = False


    # inputString = input("Please enter a key to cancel the stream")
    # if(inputString != ""):
        # collectStreamData = False
#Save tweets to csv

#Add some method to quit and close the stream

