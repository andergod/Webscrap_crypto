import requests
from bs4 import BeautifulSoup

class website_data:
    def __init__(self):
        self.headers=({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36','Accept-Language': 'en-UK, en;q=0.5'})
        self.cryptonews_url='https://crypto.news/markets/'
        self.coindesk_url='https://www.coindesk.com/markets/'
        self.yahoo_url='https://finance.yahoo.com/topic/crypto'
        self.independent_url='https://www.independent.co.uk/topic/bitcoin'
        self.remove_independent_file="Remove_independent.txt"
    def cryptonews_relevantpost(self)->list:
        r=requests.get(self.cryptonews_url, headers=self.headers)
        soup = BeautifulSoup(r.text, 'lxml')
        headlines=soup.find_all('a', class_="post-loop__link")
        return [headline.get('href') for headline in headlines]

    def coindesk_relevantpost(self)->list:
        r=requests.get(self.coindesk_url, headers=self.headers)
        soup = BeautifulSoup(r.text, 'lxml')
        headlines=soup.find_all('a', class_="card-titlestyles__CardTitleWrapper-sc-1ptmy9y-0 junCw card-title-link")
        return ["https://www.coindesk.com/" + str(headline.get('href')) for headline in headlines]
    
    def yahoo_relevantpost(self)->list:
        r=requests.get(self.yahoo_url, headers=self.headers)
        soup = BeautifulSoup(r.text, 'lxml')
        headlines=soup.find_all('a', class_='js-content-viewer wafer-caas Fw(b) Fz(18px) Lh(23px) LineClamp(2,46px) ' 
                                'Fz(17px)--sm1024 Lh(19px)--sm1024 LineClamp(2,38px)--sm1024 mega-item-header-link '
                                'Td(n) C(#0078ff):h C(#000) LineClamp(2,46px) LineClamp(2,38px)--sm1024 not-isInStreamVideoEnabled')
        
        return ["https://finance.yahoo.com/"+ str(headline.get('href')) for headline in headlines]
    
    def independent_relevantpost(self)->list:
        r=requests.get(self.independent_url, headers=self.headers)
        soup=BeautifulSoup(r.text, 'lxml')
        headlines_object=soup.find_all('h2', class_='sc-9tb5ao-0 bXiXts')
        headlines=[headline.find('a',class_="title") for headline in headlines_object]
        return ["https://www.independent.co.uk"+ str(headline.get('href')) for headline in headlines[:10]]

    def text_from_relevant(self, link:str, type:str)->str:
        r=requests.get(link, headers=self.headers)
        soup = BeautifulSoup(r.text, 'lxml')
        if type=='cryptonews_relevantpost':
            text=soup.find_all('p')
        elif type=='coindesk_relevantpost':
            text=soup.find_all('div', class_="typography__StyledTypography-sc-owin6q-0 dbtmOA at-text")
        elif type=='yahoo_relevantpost':
            text=soup.find_all('div', class_='caas-body')
        elif type=='independent_relevantpost':
            text=soup.find_all('p')    
        paragraph=[p.text for p in text]
        b_paragraph=' '.join(paragraph)
        if type=='independent_relevantpost':
            with open(self.remove_independent_file, 'r') as file:
                remove_independent=file.read()
            b_paragraph=b_paragraph.replace(remove_independent, '')
        elif type=='cryptonews_relevantpost':
            substring_to_end = "Read more about"
            position = b_paragraph.find(substring_to_end)
            if position != -1:
                # Extract the portion of the string before the substring
                b_paragraph = b_paragraph[:position]                  
        return b_paragraph