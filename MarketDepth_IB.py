import ib_insync
import matplotlib.pyplot as plt

# Connect to Interactive Brokers TWS or Gateway
ib = ib_insync.IB()
ib.connect("YourHost", 7497, clientId=1)  # Replace with your TWS/Gateway host and port

def plot_market_depth(stock_symbol):
    contract = ib_insync.Stock(stock_symbol, "SMART", "USD")  # Replace "USD" with your desired currency
    ib.qualifyContracts(contract)

    # Request real-time market depth data
    ib.reqMktDepth(contract, numRows=5)

    # Wait for data to be received
    ib.sleep(2)

    # Extract bid and ask data
    bids = ib.tickers()[0].domBids
    asks = ib.tickers()[0].domAsks

    # Create lists to store price and size information
    bid_prices = [bid.price for bid in bids]
    bid_sizes = [bid.size for bid in bids]
    ask_prices = [ask.price for ask in asks]
    ask_sizes = [ask.size for ask in asks]

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
    stock_symbol = "FMG"  # Replace with the desired ASX stock symbol
    plot_market_depth(stock_symbol)
