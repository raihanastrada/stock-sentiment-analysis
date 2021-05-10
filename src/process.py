from textblob import TextBlob
import nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt

def translate(news_list):
    '''
    Translate the news headline to english
    I.S : news_list is a List<[Name, Headline]>
    F.S : IF could acces the translation API, headline is translated
          ELSE headline is not translated
    '''
    for news in news_list:
        try:
            blob = TextBlob(news[1])
            news[1] = blob.translate(to="en")
        except:
            print("",end="")
            # DO NOTHING

def sentiment_analysis(stock_news):
    '''
    Get the sentiment analysis for each stock_news
    I.S : stock_news is a List<[Name, Headline]>
    F.S : return a dataframe of stock_news with it's sentiment
    '''
    vader = SentimentIntensityAnalyzer()
    # Convert into DataFrame
    stock_df = pd.DataFrame(stock_news, columns=['ticker','headline'])
    # Iterate through the headlines and get the polarity scores using vader
    scores = stock_df['headline'].apply(vader.polarity_scores).tolist()
    # Convert the 'scores' list of dicts into a DataFrame
    scores_df = pd.DataFrame(scores)
    # Join the DataFrames of the news and the list of dicts
    stock_df = stock_df.join(scores_df, rsuffix='_right')
    return stock_df

def visualize_data(df):
    '''
    Visualize the dataframe to a bar chart
    I.S : df not empty
    F.S : a bar chart of the df is shown
    '''
    # Group by ticker and calculate the mean
    data = df.groupby(['ticker']).mean()

    # Use compund column only
    data = data.drop(columns=['neg','neu','pos'])

    # Plot a bar chart with pandas
    data.plot(kind = 'bar', title='Analisis Sentimen Saham', color='#FFC412')
    plt.xlabel('Saham')
    plt.ylabel('Sentimen')
    
    plt.grid()
    plt.show()

def test():
    vader = SentimentIntensityAnalyzer()
    headline = "Harga Emas Antam Naik Lagi Jadi Rp937.000/Gram"
    blob = TextBlob(headline)
    headline = blob.translate(to="en")
    print(headline)
    print(vader.polarity_scores(headline))

if __name__ == "__main__":
    test()