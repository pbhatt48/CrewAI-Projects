def get_share_price(symbol: str) -> float:
    """
    Returns the current price of a share for a given stock symbol.
    
    Args:
        symbol: A string representing the stock symbol (e.g., 'AAPL', 'TSLA', 'GOOGL').
        
    Returns:
        A float representing the current price of the share.
    """
    prices = {
        'AAPL': 150.00,
        'TSLA': 700.00,
        'GOOGL': 2800.00
    }
    return prices.get(symbol.upper(), 0.0)


class Account:
    """
    A simple account management system for a trading simulation platform.
    """
    
    def __init__(self, account_id: str, initial_deposit: float):
        """
        Initializes a new account with the given account ID and initial deposit.
        
        Args:
            account_id: A string representing the unique ID for the account.
            initial_deposit: A float representing the initial amount of money deposited into the account.
        """
        self.account_id = account_id
        self.balance = initial_deposit
        self.holdings = {}
        self.transactions = []
        self.initial_deposit = initial_deposit
        
        # Record the initial deposit as a transaction
        self.transactions.append(f"Initial deposit: ${initial_deposit:.2f}")
    
    def deposit(self, amount: float) -> None:
        """
        Deposits a specified amount into the account.
        
        Args:
            amount: A float representing the amount to deposit.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        self.balance += amount
        self.transactions.append(f"Deposit: ${amount:.2f}")
    
    def withdraw(self, amount: float) -> None:
        """
        Withdraws a specified amount from the account if sufficient funds are available.
        
        Args:
            amount: A float representing the amount to withdraw.
            
        Raises:
            ValueError: If the withdrawal would result in a negative balance.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        if self.balance < amount:
            raise ValueError(f"Insufficient funds. Current balance: ${self.balance:.2f}, Requested withdrawal: ${amount:.2f}")
        
        self.balance -= amount
        self.transactions.append(f"Withdrawal: ${amount:.2f}")
    
    def buy_shares(self, symbol: str, quantity: int) -> None:
        """
        Buys a specified quantity of shares for a given stock symbol if funds are available.
        
        Args:
            symbol: A string representing the stock symbol to purchase shares of.
            quantity: An integer representing the number of shares to buy.
            
        Raises:
            ValueError: If funds are insufficient to buy the shares.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        share_price = get_share_price(symbol)
        if share_price == 0:
            raise ValueError(f"Unknown stock symbol: {symbol}")
        
        total_cost = share_price * quantity
        
        if self.balance < total_cost:
            raise ValueError(f"Insufficient funds to buy {quantity} shares of {symbol}. Cost: ${total_cost:.2f}, Balance: ${self.balance:.2f}")
        
        self.balance -= total_cost
        
        # Update holdings
        if symbol in self.holdings:
            self.holdings[symbol] += quantity
        else:
            self.holdings[symbol] = quantity
        
        self.transactions.append(f"Buy: {quantity} shares of {symbol} at ${share_price:.2f} each (Total: ${total_cost:.2f})")
    
    def sell_shares(self, symbol: str, quantity: int) -> None:
        """
        Sells a specified quantity of shares for a given stock symbol if sufficient shares are held.
        
        Args:
            symbol: A string representing the stock symbol to sell shares of.
            quantity: An integer representing the number of shares to sell.
            
        Raises:
            ValueError: If the user does not own enough shares to sell.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            current_holding = self.holdings.get(symbol, 0)
            raise ValueError(f"Insufficient shares to sell. You have {current_holding} shares of {symbol}, trying to sell {quantity}")
        
        share_price = get_share_price(symbol)
        if share_price == 0:
            raise ValueError(f"Unknown stock symbol: {symbol}")
        
        total_value = share_price * quantity
        
        self.balance += total_value
        self.holdings[symbol] -= quantity
        
        # Remove the stock from holdings if quantity becomes 0
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        
        self.transactions.append(f"Sell: {quantity} shares of {symbol} at ${share_price:.2f} each (Total: ${total_value:.2f})")
    
    def get_portfolio_value(self) -> float:
        """
        Calculates the total value of the user's portfolio based on current share prices.
        
        Returns:
            A float representing the total value of the portfolio.
        """
        total_value = self.balance
        
        for symbol, quantity in self.holdings.items():
            share_price = get_share_price(symbol)
            total_value += share_price * quantity
        
        return total_value
    
    def get_profit_or_loss(self) -> float:
        """
        Calculates the profit or loss from the initial deposit based on current share prices and balance.
        
        Returns:
            A float representing the profit or loss.
        """
        current_value = self.get_portfolio_value()
        return current_value - self.initial_deposit
    
    def get_holdings(self) -> dict:
        """
        Returns the current holdings of the user as a dictionary.
        
        Returns:
            A dictionary where keys are stock symbols and values are the quantity of shares held.
        """
        return self.holdings.copy()
    
    def get_transactions(self) -> list:
        """
        Lists all transactions that have been made in the account.
        
        Returns:
            A list of strings detailing each transaction.
        """
        return self.transactions.copy()