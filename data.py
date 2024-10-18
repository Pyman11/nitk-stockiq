
import yfinance as yf
import json

def get_data ( symbol ):
    stock = yf.Ticker(symbol)
    stock_info = stock.info

    d = {}
    
    eps = stock.info['trailingEps']
    d['Earnings per share (EPS)'] = eps

    pe_ratio = stock_info.get('trailingPE', 'N/A')
    d['Price/Earnings (P/E)'] = pe_ratio

    pb_ratio = stock_info.get('priceToBook', 'N/A')
    d['Price/Book (P/B)'] = pb_ratio

    current_price = stock.info['currentPrice']
    annual_dividend = stock.info.get('dividendRate', 0)
    if current_price > 0:  
        dividend_yield = (annual_dividend / current_price) * 100
        d['Dividend Yield'] = dividend_yield
    else:
        d['Dividend Yield'] = "N/A"
        
    def calculate_rsi(data, n_days):
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=n_days).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=n_days).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    history = stock.history(period="1mo")
    rsi = calculate_rsi(history,14).iloc[-1]
    d["Relative Strength Index"] = rsi

    beta = stock_info.get('beta', 'N/A')
    d['Beta'] = beta

    esg_data = stock.sustainability
    if esg_data is not None:
        environmental_score = esg_data.loc['environmentScore'].values[0] if 'environmentScore' in esg_data.index else 'N/A'
        social_score = esg_data.loc['socialScore'].values[0] if 'socialScore' in esg_data.index else 'N/A'
        governance_score = esg_data.loc['governanceScore'].values[0] if 'governanceScore' in esg_data.index else 'N/A'

        d['Environmental Score'] = environmental_score
        d['Social Score'] = social_score
        d['Governance Score'] = governance_score
        
    else:
        d['Environmental Score'] = 0
        d['Social Score'] = 0
        d['Governance Score'] = 0

    return d

def get_current ( symbol ):
    stock = yf.Ticker(symbol)
    stock_info = stock.info
    return stock_info['currentPrice']

def get_name ( symbol ):
    stock = yf.Ticker(symbol)
    stock_info = stock.info
    return stock_info['shortName']

def check_validity ( symbol ):
    try:
        stock = yf.Ticker(symbol)
        stock_info = stock.info
        return 1
    except:
        return 0
