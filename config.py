# Set user agent and other headers for making requests        
headers=({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36','Accept-Language': 'en-UK, en;q=0.5'})

# Define URLs for different news sources
cryptonews_url='https://crypto.news/markets/'
coindesk_url='https://www.coindesk.com/markets/'
yahoo_url='https://finance.yahoo.com/topic/crypto'
independent_url='https://www.independent.co.uk/topic/bitcoin'

# File name to store content to remove for 'independent_relevantpost'
remove_independent_file="Remove_independent.txt"