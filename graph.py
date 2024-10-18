
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def create_graph ( stock_symbol ):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)

    closing_prices = stock_data['Close'].tolist()
    x = list ( range ( len ( closing_prices ) ) )
    y = closing_prices
    plt.xticks([])  
    plt.yticks([])  

    plt.plot(x, y)
    plt.savefig('{}.png'.format ( stock_symbol.lower() ), format='png', dpi=40, bbox_inches='tight')  
    plt.clf()
    plt.cla()
    plt.close()

    return sum ( y ) / len ( y ) 

