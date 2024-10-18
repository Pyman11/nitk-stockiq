
import requests
from bs4 import BeautifulSoup

def scrape_article_summary(article_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(article_url, headers=headers)
    
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.find_all(['p', 'div'])

    summary_set = set()
    keywords = ['layoff', 'increase', 'decrease', 'rise', 'fall', 'restructuring', 
                'merger', 'acquisition', 'bankruptcy', 'earnings', 'profit', 
                'loss', 'growth', 'job', 'employment', 'report', 'settlement']

    for element in content:
        text = element.get_text()
        if any(keyword in text.lower() for keyword in keywords):
            summary_set.add(text.strip())

    return list(summary_set)

def scrape_multiple_links(symbol):
    global code
    url = f'https://finance.yahoo.com/quote/{symbol}/news/'
    code = symbol
    stock_summary = scrape_article_summary(url)
    return {url: stock_summary}

def analyze_sentiment(output_string):
    positive_keywords = ['increase', 'rise', 'growth', 'profit', 'merger', 'acquisition', 'expansion']
    negative_keywords = ['decrease', 'fall', 'loss', 'layoff', 'restructuring', 'bankruptcy', 'closure']

    positive_count = sum(1 for word in positive_keywords if word in output_string.lower())
    negative_count = sum(1 for word in negative_keywords if word in output_string.lower())

    insights = []
    if positive_count > negative_count:
        insights.append("Overall sentiment is positive.")
        insights.append("Look for potential growth opportunities.")
    elif negative_count > positive_count:
        insights.append("Overall sentiment is negative.")
        insights.append("Consider exercising caution and researching further.")
    else:
        insights.append("Sentiment is neutral. Keep monitoring the news.")

    return insights

def get_news ( user_symbol ):

    summaries = scrape_multiple_links(user_symbol)

    final = ""
    final_news = [ "" ]
    final_insights = []

    for link, summary in summaries.items():
        final += f"\nLink: {link}\n"
        if summary:
            final += "Summary of the article content:\n"
            for line in summary:
                output_string = f"{line}"
                final += output_string
                if ( len ( output_string ) > 100 and len ( output_string ) < 1000 and code.lower() in output_string.lower() ):
                    final_news.append ( "• " + output_string )
                    l = output_string.lower().split()
                    try:
                        if l.index ( 'ago' ) and l[l.index ( 'ago' ) - 1] == 'hours':
                            final_news.append ( "(" + l[l.index ( 'ago' ) - 2]+ " hours ago)" )
                    except:
                        pass
                    final_news.append ( "" )
        else:
            final += "  - No relevant content found in this article.\n"
            
    insights = analyze_sentiment(final)

    for insight in insights:
        final_insights.append ( f"{insight}" )

    final = [ final_news, final_insights ]
    return final
