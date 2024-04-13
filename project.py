import tkinter as tk
from tkinter import ttk
import ccxt
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import time

exchange = ccxt.coinex()

# Function to fetch futures symbols from the exchange
def fetch_futures_symbols():
    futures_markets = exchange.load_markets(True)
    futures_symbols = [symbol for symbol in futures_markets if '/usd' in symbol.lower()]
    return futures_symbols

# Function to analyze each symbol and decide on entry and exit points
def analyze_symbol(symbol):
    orderbook = exchange.fetch_order_book(symbol)
    highest_bid = orderbook['bids'][0][0] if len(orderbook['bids']) > 0 else None
    lowest_ask = orderbook['asks'][0][0] if len(orderbook['asks']) > 0 else None

    if highest_bid is not None and lowest_ask is not None:
        buy_price = float(highest_bid) * 0.99  
        sell_price = float(lowest_ask) * 1.01  
        
        # Simulate analysis time
        time.sleep(1)
        
        # Analyze more and decide on trade
        if buy_price < sell_price:
            order_type = 'Long'
            signal = 'Buy Long'
        else:
            order_type = 'Short'
            signal = 'Sell Short'
        
        return buy_price, sell_price, order_type, signal
    else:
        return None, None, None, None

# Function to handle when the user selects a symbol from the dropdown
def on_symbol_selected(event):
    selected_symbol = symbol_combobox.get()
    print(f'Selected Symbol: {selected_symbol}')
    buy_price, sell_price, order_type, signal = analyze_symbol(selected_symbol)
    if buy_price is not None and sell_price is not None:
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        display_orders_table(current_time, current_time, selected_symbol, buy_price, sell_price, order_type, signal)
        plot_trades(selected_symbol, buy_price, sell_price)
    else:
        print("Error: Unable to fetch order book data for the selected symbol")

# Function to handle search
def on_search(event):
    search_text = search_entry.get()
    filtered_symbols = [symbol for symbol in futures_symbols if search_text.lower() in symbol.lower()]
    symbol_combobox['values'] = filtered_symbols

# Function to display order table
def display_orders_table(buy_time, sell_time, best_symbol, buy_price, sell_price, order_type, signal):
    orders_table_data = {
        'Time': [buy_time, sell_time],
        'Symbol': [best_symbol, best_symbol],
        'Price': [buy_price, sell_price],
        'Action': [signal, signal],
        'Type': [order_type, order_type]  # Add the order type to the table
    }

    orders_table_df = pd.DataFrame(orders_table_data)

    orders_text.delete('1.0', tk.END)
    orders_text.insert(tk.END, orders_table_df.to_string(index=False))

# Function to plot trades
def plot_trades(symbol, buy_price, sell_price):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the main trades
    ax.plot([0, 1], [buy_price, sell_price], marker='o')
    ax.set_title(f"Trades for {symbol}")
    ax.set_xlabel("Trade Type")
    ax.set_ylabel("Price")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Buy', 'Sell'])
    ax.grid(True)

    # Create an inset to display the sub-signal
    inset_width = 0.2
    inset_height = 0.2
    inset = ax.inset_axes([0.05, 0.1, inset_width, inset_height])
    inset.plot([0, 1, 2, 3, 4], [30, 35, 40, 38, 37])  # Sample sub-signal data
    inset.set_title('Sub-Signal')
    inset.set_xlabel('Time')
    inset.set_ylabel('Value')
    inset.grid(True)

    plt.show()

# Create the main window
root = tk.Tk()
root.title("Futures Analysis")

# Create a search entry
search_entry = ttk.Entry(root)
search_entry.pack(pady=10)
search_entry.bind("<KeyRelease>", on_search)

# Create a label
label = tk.Label(root, text="Select a futures symbol:")
label.pack()

# Fetch futures symbols
futures_symbols = fetch_futures_symbols()

# Create a dropdown for selecting the futures symbol
selected_symbol = tk.StringVar()
symbol_combobox = ttk.Combobox(root, textvariable=selected_symbol)
symbol_combobox['values'] = futures_symbols
symbol_combobox.pack(pady=5)
symbol_combobox.bind("<<ComboboxSelected>>", on_symbol_selected)

# Create a text widget to display orders
orders_text = tk.Text(root, height=10, width=50)
orders_text.pack(pady=10)

root.mainloop()
