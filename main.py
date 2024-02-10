
from website_data import cryptonews_relevantpost, coindesk_relevantpost, yahoo_relevantpost, independent_relevantpost, text_from_relevant 
from sentiment_analysis import clean_text, analyze_sentiment, get_main_currency 

def run_process(website:callable)->None:
    #Run the process for a specific website, extract relevant posts, and analyze sentiment.
    posts, type = website()
    for post in posts:
        text=text_from_relevant(post, type)
        clean=clean_text(text)
        sentiment=analyze_sentiment(clean)
        currency=get_main_currency(text)
        if currency:
            print(f'I should {sentiment} {currency}')
        else:
            print('No relevant currency found')       

if __name__ == '__main__':
    run_process(cryptonews_relevantpost)
    run_process(coindesk_relevantpost)
    run_process(yahoo_relevantpost)
    run_process(independent_relevantpost)