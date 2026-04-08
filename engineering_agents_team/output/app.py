import gradio as gr
from accounts import Account, get_share_price

# Initialize a global account instance
account = Account("demo_user", 10000.0)

def deposit_funds(amount):
    try:
        account.deposit(float(amount))
        return f"Successfully deposited ${amount}. New balance: ${account.balance:.2f}"
    except Exception as e:
        return f"Error: {str(e)}"

def withdraw_funds(amount):
    try:
        account.withdraw(float(amount))
        return f"Successfully withdrew ${amount}. New balance: ${account.balance:.2f}"
    except Exception as e:
        return f"Error: {str(e)}"

def buy_shares(symbol, quantity):
    try:
        account.buy_shares(symbol.upper(), int(quantity))
        return f"Successfully bought {quantity} shares of {symbol.upper()}. New balance: ${account.balance:.2f}"
    except Exception as e:
        return f"Error: {str(e)}"

def sell_shares(symbol, quantity):
    try:
        account.sell_shares(symbol.upper(), int(quantity))
        return f"Successfully sold {quantity} shares of {symbol.upper()}. New balance: ${account.balance:.2f}"
    except Exception as e:
        return f"Error: {str(e)}"

def get_account_info():
    balance = account.balance
    portfolio_value = account.get_portfolio_value()
    profit_loss = account.get_profit_or_loss()
    holdings = account.get_holdings()
    
    info = f"Cash Balance: ${balance:.2f}\n"
    info += f"Total Portfolio Value: ${portfolio_value:.2f}\n"
    info += f"Profit/Loss: ${profit_loss:.2f}\n\n"
    info += "Holdings:\n"
    
    if holdings:
        for symbol, quantity in holdings.items():
            price = get_share_price(symbol)
            value = price * quantity
            info += f"  {symbol}: {quantity} shares @ ${price:.2f} = ${value:.2f}\n"
    else:
        info += "  No shares held\n"
    
    return info

def get_transaction_history():
    transactions = account.get_transactions()
    if transactions:
        return "\n".join(transactions)
    else:
        return "No transactions yet"

def get_share_prices():
    return "Current Share Prices:\nAAPL: $150.00\nTSLA: $700.00\nGOOGL: $2800.00"

# Create Gradio interface
with gr.Blocks(title="Trading Simulation Account Demo") as demo:
    gr.Markdown("# Trading Simulation Account Demo")
    gr.Markdown("Demo account initialized with $10,000")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### Account Operations")
            
            with gr.Group():
                gr.Markdown("**Deposit/Withdraw**")
                deposit_amount = gr.Number(label="Amount to Deposit", value=1000)
                deposit_btn = gr.Button("Deposit")
                deposit_output = gr.Textbox(label="Deposit Result", interactive=False)
                
                withdraw_amount = gr.Number(label="Amount to Withdraw", value=500)
                withdraw_btn = gr.Button("Withdraw")
                withdraw_output = gr.Textbox(label="Withdraw Result", interactive=False)
            
            with gr.Group():
                gr.Markdown("**Trading**")
                buy_symbol = gr.Textbox(label="Stock Symbol to Buy", value="AAPL")
                buy_quantity = gr.Number(label="Quantity to Buy", value=10)
                buy_btn = gr.Button("Buy Shares")
                buy_output = gr.Textbox(label="Buy Result", interactive=False)
                
                sell_symbol = gr.Textbox(label="Stock Symbol to Sell", value="AAPL")
                sell_quantity = gr.Number(label="Quantity to Sell", value=5)
                sell_btn = gr.Button("Sell Shares")
                sell_output = gr.Textbox(label="Sell Result", interactive=False)
        
        with gr.Column():
            gr.Markdown("### Account Information")
            
            account_info = gr.Textbox(label="Account Summary", lines=10, interactive=False)
            refresh_info_btn = gr.Button("Refresh Account Info")
            
            transaction_history = gr.Textbox(label="Transaction History", lines=8, interactive=False)
            refresh_history_btn = gr.Button("Refresh Transaction History")
            
            share_prices = gr.Textbox(label="Available Stocks", lines=4, interactive=False, value=get_share_prices())
    
    # Event handlers
    deposit_btn.click(deposit_funds, inputs=deposit_amount, outputs=deposit_output)
    withdraw_btn.click(withdraw_funds, inputs=withdraw_amount, outputs=withdraw_output)
    buy_btn.click(buy_shares, inputs=[buy_symbol, buy_quantity], outputs=buy_output)
    sell_btn.click(sell_shares, inputs=[sell_symbol, sell_quantity], outputs=sell_output)
    refresh_info_btn.click(get_account_info, outputs=account_info)
    refresh_history_btn.click(get_transaction_history, outputs=transaction_history)
    
    # Initialize the display
    demo.load(get_account_info, outputs=account_info)
    demo.load(get_transaction_history, outputs=transaction_history)

if __name__ == "__main__":
    demo.launch()