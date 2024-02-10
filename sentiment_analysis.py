# Description: This file contains the functions to analyze the sentiment of news articles and provide trading recommendations.
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy

nltk.download('vader_lexicon')
nltk.download('vader_lexicon')
nltk.download('stopwords')
nltk.download('punkt')

# Load cryptocurrency data from an Excel file
cryptocurrencies = pd.read_excel('Criptocurrency_list.xlsx')
# Create a dictionary mapping cryptocurrency names to tickers
crypto_dict={name.lower().strip(): ticker for name, ticker in zip(cryptocurrencies['Name'], cryptocurrencies['Ticker'])}
# Load the spaCy English model
nlp = spacy.load('en_core_web_sm')


def clean_text(text)->str:
    # Tokenize the text
    words = word_tokenize(text)
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    filtered_words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
    return ' '.join(filtered_words)
        
def analyze_sentiment(text)->str:
    #Analyze sentiment of the text and return a trading recommendation.
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(text)['compound']
    # Assume a simple threshold for sentiment
    if sentiment_score >= 0.1:
        return 'Buy'
    elif sentiment_score <= -0.1:
        return 'Sell'
    else:
        return 'Hold'
    
def get_main_currency(text)->str:
    doc = nlp(text)
    # Extract entities recognized as cryptocurrencies
    recognized_currencies = [ent.text.lower() for ent in doc.ents if ent.text.lower() in crypto_dict]
    # If there are recognized cryptocurrencies, return the first one, otherwise return None
    if recognized_currencies:
        return crypto_dict[recognized_currencies[0]].upper()
    else:   
        return None

    

    