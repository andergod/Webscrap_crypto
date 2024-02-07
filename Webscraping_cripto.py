from bs4 import BeautifulSoup
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy
from website_data import cryptonews_relevantpost, coindesk_relevantpost, yahoo_relevantpost, independent_relevantpost, text_from_relevant

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
    return recognized_currencies[0] if recognized_currencies else None

def run_process(website:str)->None:
    #Run the process for a specific website, extract relevant posts, and analyze sentiment.
    if website=="cryptonews_relevantpost":
        posts=cryptonews_relevantpost()
        type="cryptonews_relevantpost"
    elif website=="coindesk_relevantpost":
        posts=coindesk_relevantpost()
        type="coindesk_relevantpost"
    elif website=="yahoo_relevantpost":
        posts=yahoo_relevantpost()
        type="yahoo_relevantpost"
    elif website=="independent_relevantpost":
        posts=independent_relevantpost()
        type="independent_relevantpost"
    for post in posts:
        text=text_from_relevant(post, type)
        clean=clean_text(text)
        sentiment=analyze_sentiment(clean)
        currency=get_main_currency(text)
        if currency:
            print(f'I should {sentiment} {crypto_dict[currency].upper()}')
        else:
            print('No relevant currency found')       
    

if __name__ == '__main__':
    run_process("cryptonews_relevantpost")
    run_process("coindesk_relevantpost")
    run_process("yahoo_relevantpost")
    run_process("independent_relevantpost")
    