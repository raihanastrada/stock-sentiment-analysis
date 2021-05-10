import re
import datetime
from lq45 import lq45
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

# Extracting content from this website
main_url = 'https://id.investing.com/equities/indonesia'
# Regex pattern to extract Stock Name
stock_name_pattern = r'>[\w\s(&amp;)]*</a>'
# Regex pattern to extract Stock URL
stock_link_pattern = r'href="[\w\-\/]*'
# Regex pattern to extract news date
date_pattern = r'(\d{2})[/-](\d{2})[/-](\d{4})'
# Regex pattern to extract news headline
headline_pattern = r'title=\"[\w\s!@#$%^&()-`.+,/]*\"'

def get_stocks():
    '''
    Get the list of stocks and it's unique link
    F.S : Returning List<Tuple<Name, Link>>
    '''
    stocks = []
    try:
        # Get the website html content
        r = Request(url=main_url, headers={'user-agent': 'my-app/0.01'})
        c = urlopen(r).read()
        soup = BeautifulSoup(c, 'html.parser')

        # Get the content in tr tag
        tr_tag = []
        for i in soup.find('div', {'class':'js-ga-on-sort marketInnerContent filteredMarketsDiv'}).find_all('tr'):
            tr_tag.append(i)

        # For all the tags, extract the name of the stocks and it's unique web link
        for tags in tr_tag:
            name = re.search(stock_name_pattern,str(tags))
            link = re.search(stock_link_pattern,str(tags))
            if(name and link):
                name = name.group(0)
                link = link.group(0)

                # Clean the conntent
                name = re.sub('>','',name)
                name = re.sub('</a','',name)
                name = re.sub('&amp;', '&', name)
                link = re.sub('href="','',link)

                # Only add if stock is a part of LQ45
                if (name in lq45):
                    stocks.append((name,link))
    except:
        print("Error")

    return stocks
    
def get_news(stocks):
    '''
    Get the headline news of the stocks
    I.S : stocks is a List<Tuple<Name, Link>>
    F.S : returning List<[Name, Headline]>
    '''
    news_list = []

    for stock in stocks:
        news_url = re.sub('/equities/indonesia',stock[1]+'-news',main_url)
        try:
            # Get the content in news url
            r = Request(url=news_url, headers={'user-agent': 'my-app/0.01'})
            c = urlopen(r).read()
            soup = BeautifulSoup(c, 'html.parser')

            # Extract the 'headline' and 'date' of the aricle list
            for article in soup.find('section', {'id':'leftColumn'}).find('div', {'class':'mediumTitle1'}).find_all('div', {'class':'textDiv'}):
                article = str(article)
                headline = re.search(headline_pattern, article)
                date = re.search(date_pattern, article)
                if (headline and date):
                    headline = headline.group(0)
                    date = date.group(0)
                    
                    # Clean the 'headline'
                    headline = re.sub('title=','',headline)
                    headline = re.sub('&amp;', '&', headline)
                    headline = re.sub('"','',headline)
                    
                    # Check if is date has a timespan of one week before today's date
                    # If 'True' then add to news_list; Else go to next stock
                    if (is_one_week_before(date)):
                        news_list.append([stock[0],headline])
                    else:
                        break
        except:
            print("Error")

    return news_list

def is_one_week_before(x):
    '''
    Check if x is in range of one week before today's date
    F.S : Return Boolean based on result
    '''
    d = datetime.datetime.strptime(x, "%d/%m/%Y")
    now = datetime.datetime.now()
    return (now - d).days < 7

# if __name__ == "__main__":
#     stocks = get_stocks()
#     print(stocks)
#     news = get_news(stocks)
#     print(news)