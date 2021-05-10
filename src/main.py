import scrap as s
import process as p

if __name__ == "__main__":
    print("Getting stocks list...")
    stocks = s.get_stocks()
    print("DONE")
    print("Getting each stock news...")
    news = s.get_news(stocks)
    print("DONE")
    print("Translating news...")
    p.translate(news)
    print("DONE")
    print("Getting news sentiment...")
    res = p.sentiment_analysis(news)
    print("DONE")
    print("Visualizing the result...")
    p.visualize_data(res)
    print("ALL PROCESS DONE")