from flask import Flask, render_template, request, url_for
import wikipedia
from flask_bootstrap import Bootstrap


from textblob import TextBlob
import tweepy


app = Flask(__name__)
Bootstrap(app)

consumer_key= '9N4LhWmdtUZT0sbVpgbMyqEY5'
consumer_secret= '89HtqbHBzmaD9YQSPO6hdU7PQHoMHRSF6NvwxlTCfsY0HZZtZ6'
access_token='863387980492414976-6ljbFkaBtFMQv3RO8pwAcZGlkI3HXzP'
access_token_secret='mkxCMzl3p9Eydhenw0iTyN0kKmgnXI8WyI813khmwDSfq'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/analyse', methods=['POST'])
def analyse():
	if request.method == 'POST':
		query = request.form['query']
		number_of_item = request.form['num']
		number_of_item = int(number_of_item)

		public_tweets = tweepy.Cursor(api.search, q=query, lang = "en").items(number_of_item)

		polarity = 0
		positive = 0
		negative = 0
		neutral = 0

		for tweet in public_tweets:
			tweets = tweet.text
			analysis = TextBlob(tweet.text)
			polarity += analysis.sentiment.polarity
			if (analysis.sentiment.polarity == 0):
				neutral += 1
			elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
				positive += 1
			elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
				negative += 1


		positive = 100 * float(positive) / float(number_of_item)
		polarity = polarity / number_of_item
		negative = 100 * float(negative) / float(number_of_item)
		neutral = 100 * float(neutral) / float(number_of_item)
		summary = wikipedia.summary(query,sentences=5)






	return render_template('index.html',polarity=str(polarity),positive=str(positive),negative=str(negative), neutral=str(neutral),summary=summary,tweets=tweets)




if __name__=='__main__':
	app.run(debug=True)





# positive = avg(positive,100)
# polarity = polarity / 100
# negative = avg(negative,100)
# neutral = avg(negative,100)

# print(str(positive) + "% people thought it was positive")
# print(str(negative) + "% people thought it was negative")
# print(str(neutral) + "% people thought it was neutral")

# print(wikipedia.summary('trump'))

