import yfinance as yf
import matplotlib.pyplot as plt

def plot_market_depth(stock_symbol):
    stock = yf.Ticker(stock_symbol)

    # Fetch real-time market depth data
    market_depth = stock.get_order_book()

    # Extract bid and ask data
    bids = market_depth["bids"]
    asks = market_depth["asks"]

    # Create lists to store price and size information
    bid_prices = [bid[0] for bid in bids]
    bid_sizes = [bid[1] for bid in bids]
    ask_prices = [ask[0] for ask in asks]
    ask_sizes = [ask[1] for ask in asks]

    # Plot market depth
    plt.figure(figsize=(10, 6))
    plt.plot(bid_prices, bid_sizes, label="Bid", marker="o", markersize=5, color="green")
    plt.plot(ask_prices, ask_sizes, label="Ask", marker="o", markersize=5, color="red")

    plt.xlabel("Price")
    plt.ylabel("Size")
    plt.title(f"Market Depth for {stock_symbol} - Real Time")
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    stock_symbol = "FMG.AX"  # Replace with the desired ASX stock symbol
    plot_market_depth(stock_symbol)
