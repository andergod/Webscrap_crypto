import requests
from bs4 import BeautifulSoup
import config

def cryptonews_relevantpost()->tuple:
    # Make a request to the Cryptonews URL
    r=requests.get(config.cryptonews_url, headers=config.headers)
    soup = BeautifulSoup(r.text, 'lxml')
    
    # Extract relevant post headlines
    headlines=soup.find_all('a', class_="post-loop__link")
    return [headline.get('href') for headline in headlines],"cryptonews_relevantpost"

def coindesk_relevantpost()->tuple:
    # Make a request to the Coindesk URL
    r=requests.get(config.coindesk_url, headers=config.headers)
    soup = BeautifulSoup(r.text, 'lxml')
    
    # Extract relevant post headlines
    headlines=soup.find_all('a', class_="card-titlestyles__CardTitleWrapper-sc-1ptmy9y-0 junCw card-title-link")
    return ["https://www.coindesk.com/" + str(headline.get('href')) for headline in headlines], "coindesk_relevantpost"

def yahoo_relevantpost()->tuple:
    # Make a request to the Yahoo Finance URL
    r=requests.get(config.yahoo_url, headers=config.headers)
    soup = BeautifulSoup(r.text, 'lxml')
    
    # Extract relevant post headlines
    headlines=soup.find_all('a', class_='js-content-viewer wafer-caas Fw(b) Fz(18px) Lh(23px) LineClamp(2,46px) ' 
                            'Fz(17px)--sm1024 Lh(19px)--sm1024 LineClamp(2,38px)--sm1024 mega-item-header-link '
                            'Td(n) C(#0078ff):h C(#000) LineClamp(2,46px) LineClamp(2,38px)--sm1024 not-isInStreamVideoEnabled')
    
    return ["https://finance.yahoo.com/"+ str(headline.get('href')) for headline in headlines], "yahoo_relevantpost"

def independent_relevantpost()->tuple:
    # Make a request to the Independent URL
    r=requests.get(config.independent_url, headers=config.headers)
    soup=BeautifulSoup(r.text, 'lxml')
    
    # Extract relevant post headlines
    headlines_object=soup.find_all('h2', class_='sc-9tb5ao-0 bXiXts')
    headlines=[headline.find('a',class_="title") for headline in headlines_object]
    
    # Return URLs of top 10 independent headlines
    return ["https://www.independent.co.uk"+ str(headline.get('href')) for headline in headlines[:10]], "independent_relevantpost"

def text_from_relevant(link:str, type:str)->tuple:
    # Make a request to the specified link
    r=requests.get(link, headers=config.headers)
    soup = BeautifulSoup(r.text, 'lxml')
    
    # Extract text based on the specified type
    if type=='cryptonews_relevantpost':
        text=soup.find_all('p')
    elif type=='coindesk_relevantpost':
        text=soup.find_all('div', class_="typography__StyledTypography-sc-owin6q-0 dbtmOA at-text")
    elif type=='yahoo_relevantpost':
        text=soup.find_all('div', class_='caas-body')
    elif type=='independent_relevantpost':
        text=soup.find_all('p')    
        
    # Process and join paragraphs into a single string
    paragraph=[p.text for p in text]
    b_paragraph=' '.join(paragraph)
    
    # Specific processing based on the type
    if type=='independent_relevantpost':
        # Remove content specified in 'Remove_independent.txt'
        with open(config.remove_independent_file, 'r') as file:
            remove_independent=file.read()
        b_paragraph=b_paragraph.replace(remove_independent, '')
    elif type=='cryptonews_relevantpost':
        # Remove content after the specified substring
        substring_to_end = "Read more about"
        position = b_paragraph.find(substring_to_end)
        if position != -1:
            # Extract the portion of the string before the substring
            b_paragraph = b_paragraph[:position]                  
    return b_paragraph