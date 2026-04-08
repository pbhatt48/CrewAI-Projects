import unittest
from accounts import get_share_price, Account


class TestGetSharePrice(unittest.TestCase):
    """Test cases for the get_share_price function."""
    
    def test_valid_symbols(self):
        """Test that valid symbols return correct prices."""
        self.assertEqual(get_share_price('AAPL'), 150.00)
        self.assertEqual(get_share_price('TSLA'), 700.00)
        self.assertEqual(get_share_price('GOOGL'), 2800.00)
    
    def test_case_insensitive(self):
        """Test that symbols are case-insensitive."""
        self.assertEqual(get_share_price('aapl'), 150.00)
        self.assertEqual(get_share_price('tsla'), 700.00)
        self.assertEqual(get_share_price('googl'), 2800.00)
        self.assertEqual(get_share_price('ApPl'), 150.00)
    
    def test_invalid_symbol(self):
        """Test that invalid symbols return 0.0."""
        self.assertEqual(get_share_price('INVALID'), 0.0)
        self.assertEqual(get_share_price('XYZ'), 0.0)
        self.assertEqual(get_share_price(''), 0.0)


class TestAccount(unittest.TestCase):
    """Test cases for the Account class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.account = Account('TEST001', 1000.0)
    
    def test_account_initialization(self):
        """Test account initialization with proper values."""
        self.assertEqual(self.account.account_id, 'TEST001')
        self.assertEqual(self.account.balance, 1000.0)
        self.assertEqual(self.account.initial_deposit, 1000.0)
        self.assertEqual(self.account.holdings, {})
        self.assertEqual(len(self.account.transactions), 1)
        self.assertIn("Initial deposit: $1000.00", self.account.transactions[0])
    
    def test_deposit_valid_amount(self):
        """Test depositing valid amounts."""
        initial_balance = self.account.balance
        self.account.deposit(500.0)
        self.assertEqual(self.account.balance, initial_balance + 500.0)
        self.assertIn("Deposit: $500.00", self.account.transactions[-1])
    
    def test_deposit_invalid_amount(self):
        """Test depositing invalid amounts raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.deposit(0)
        self.assertEqual(str(context.exception), "Deposit amount must be positive")
        
        with self.assertRaises(ValueError) as context:
            self.account.deposit(-100)
        self.assertEqual(str(context.exception), "Deposit amount must be positive")
    
    def test_withdraw_valid_amount(self):
        """Test withdrawing valid amounts."""
        initial_balance = self.account.balance
        self.account.withdraw(300.0)
        self.assertEqual(self.account.balance, initial_balance - 300.0)
        self.assertIn("Withdrawal: $300.00", self.account.transactions[-1])
    
    def test_withdraw_invalid_amount(self):
        """Test withdrawing invalid amounts raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(0)
        self.assertEqual(str(context.exception), "Withdrawal amount must be positive")
        
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(-100)
        self.assertEqual(str(context.exception), "Withdrawal amount must be positive")
    
    def test_withdraw_insufficient_funds(self):
        """Test withdrawing more than available balance raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(2000.0)
        self.assertIn("Insufficient funds", str(context.exception))
        self.assertIn("Current balance: $1000.00", str(context.exception))
        self.assertIn("Requested withdrawal: $2000.00", str(context.exception))
    
    def test_buy_shares_valid(self):
        """Test buying shares with sufficient funds."""
        initial_balance = self.account.balance
        self.account.buy_shares('AAPL', 2)
        
        expected_cost = 150.0 * 2  # 300.0
        self.assertEqual(self.account.balance, initial_balance - expected_cost)
        self.assertEqual(self.account.holdings['AAPL'], 2)
        self.assertIn("Buy: 2 shares of AAPL at $150.00 each (Total: $300.00)", self.account.transactions[-1])
    
    def test_buy_shares_multiple_purchases(self):
        """Test buying shares multiple times for the same symbol."""
        self.account.buy_shares('AAPL', 2)
        self.account.buy_shares('AAPL', 3)
        
        self.assertEqual(self.account.holdings['AAPL'], 5)
    
    def test_buy_shares_invalid_quantity(self):
        """Test buying shares with invalid quantity raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.buy_shares('AAPL', 0)
        self.assertEqual(str(context.exception), "Quantity must be positive")
        
        with self.assertRaises(ValueError) as context:
            self.account.buy_shares('AAPL', -5)
        self.assertEqual(str(context.exception), "Quantity must be positive")
    
    def test_buy_shares_unknown_symbol(self):
        """Test buying shares with unknown symbol raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.buy_shares('UNKNOWN', 1)
        self.assertEqual(str(context.exception), "Unknown stock symbol: UNKNOWN")
    
    def test_buy_shares_insufficient_funds(self):
        """Test buying shares with insufficient funds raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.buy_shares('GOOGL', 1)  # GOOGL costs 2800, we only have 1000
        self.assertIn("Insufficient funds to buy 1 shares of GOOGL", str(context.exception))
        self.assertIn("Cost: $2800.00", str(context.exception))
        self.assertIn("Balance: $1000.00", str(context.exception))
    
    def test_sell_shares_valid(self):
        """Test selling shares when sufficient shares are held."""
        # First buy some shares
        self.account.buy_shares('AAPL', 5)
        initial_balance = self.account.balance
        
        # Then sell some
        self.account.sell_shares('AAPL', 2)
        
        expected_value = 150.0 * 2  # 300.0
        self.assertEqual(self.account.balance, initial_balance + expected_value)
        self.assertEqual(self.account.holdings['AAPL'], 3)
        self.assertIn("Sell: 2 shares of AAPL at $150.00 each (Total: $300.00)", self.account.transactions[-1])
    
    def test_sell_shares_all_holdings(self):
        """Test selling all shares removes the symbol from holdings."""
        self.account.buy_shares('AAPL', 2)
        self.account.sell_shares('AAPL', 2)
        
        self.assertNotIn('AAPL', self.account.holdings)
    
    def test_sell_shares_invalid_quantity(self):
        """Test selling shares with invalid quantity raises ValueError."""
        self.account.buy_shares('AAPL', 2)
        
        with self.assertRaises(ValueError) as context:
            self.account.sell_shares('AAPL', 0)
        self.assertEqual(str(context.exception), "Quantity must be positive")
        
        with self.assertRaises(ValueError) as context:
            self.account.sell_shares('AAPL', -1)
        self.assertEqual(str(context.exception), "Quantity must be positive")
    
    def test_sell_shares_insufficient_holdings(self):
        """Test selling more shares than held raises ValueError."""
        self.account.buy_shares('AAPL', 2)
        
        with self.assertRaises(ValueError) as context:
            self.account.sell_shares('AAPL', 5)
        self.assertIn("Insufficient shares to sell", str(context.exception))
        self.assertIn("You have 2 shares of AAPL, trying to sell 5", str(context.exception))
    
    def test_sell_shares_no_holdings(self):
        """Test selling shares when no shares are held raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.sell_shares('AAPL', 1)
        self.assertIn("Insufficient shares to sell", str(context.exception))
        self.assertIn("You have 0 shares of AAPL, trying to sell 1", str(context.exception))
    
    def test_sell_shares_unknown_symbol(self):
        """Test selling shares with unknown symbol raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.sell_shares('UNKNOWN', 1)
        self.assertEqual(str(context.exception), "Unknown stock symbol: UNKNOWN")
    
    def test_get_portfolio_value_cash_only(self):
        """Test portfolio value with cash only."""
        expected_value = self.account.balance
        self.assertEqual(self.account.get_portfolio_value(), expected_value)
    
    def test_get_portfolio_value_with_holdings(self):
        """Test portfolio value with cash and holdings."""
        self.account.buy_shares('AAPL', 2)  # Costs 300, leaves 700 cash
        self.account.buy_shares('TSLA', 1)  # Costs 700, leaves 0 cash
        
        expected_value = 0 + (2 * 150.0) + (1 * 700.0)  # 0 + 300 + 700 = 1000
        self.assertEqual(self.account.get_portfolio_value(), expected_value)
    
    def test_get_profit_or_loss_no_change(self):
        """Test profit/loss calculation when value hasn't changed."""
        self.assertEqual(self.account.get_profit_or_loss(), 0.0)
    
    def test_get_profit_or_loss_with_profit(self):
        """Test profit/loss calculation with profit."""
        self.account.deposit(500.0)  # Add more money
        expected_profit = 500.0
        self.assertEqual(self.account.get_profit_or_loss(), expected_profit)
    
    def test_get_profit_or_loss_with_loss(self):
        """Test profit/loss calculation with loss."""
        self.account.withdraw(200.0)  # Withdraw money
        expected_loss = -200.0
        self.assertEqual(self.account.get_profit_or_loss(), expected_loss)
    
    def test_get_holdings_empty(self):
        """Test getting holdings when no shares are held."""
        holdings = self.account.get_holdings()
        self.assertEqual(holdings, {})
        self.assertIsNot(holdings, self.account.holdings)  # Should be a copy
    
    def test_get_holdings_with_shares(self):
        """Test getting holdings when shares are held."""
        self.account.buy_shares('AAPL', 2)
        self.account.buy_shares('TSLA', 1)
        
        holdings = self.account.get_holdings()
        expected_holdings = {'AAPL': 2, 'TSLA': 1}
        self.assertEqual(holdings, expected_holdings)
        self.assertIsNot(holdings, self.account.holdings)  # Should be a copy
    
    def test_get_transactions(self):
        """Test getting transaction history."""
        self.account.deposit(100.0)
        self.account.withdraw(50.0)
        self.account.buy_shares('AAPL', 1)
        
        transactions = self.account.get_transactions()
        self.assertEqual(len(transactions), 4)  # Initial + 3 new transactions
        self.assertIn("Initial deposit: $1000.00", transactions[0])
        self.assertIn("Deposit: $100.00", transactions[1])
        self.assertIn("Withdrawal: $50.00", transactions[2])
        self.assertIn("Buy: 1 shares of AAPL", transactions[3])
        self.assertIsNot(transactions, self.account.transactions)  # Should be a copy
    
    def test_complex_trading_scenario(self):
        """Test a complex trading scenario with multiple operations."""
        # Start with 1000
        self.account.deposit(500.0)  # Now 1500
        self.account.buy_shares('AAPL', 4)  # Spend 600, now 900 cash + 4 AAPL
        self.account.buy_shares('TSLA', 1)  # Spend 700, now 200 cash + 4 AAPL + 1 TSLA
        self.account.sell_shares('AAPL', 2)  # Gain 300, now 500 cash + 2 AAPL + 1 TSLA
        
        # Check final state
        self.assertEqual(self.account.balance, 500.0)
        self.assertEqual(self.account.holdings['AAPL'], 2)
        self.assertEqual(self.account.holdings['TSLA'], 1)
        
        # Portfolio value: 500 + (2 * 150) + (1 * 700) = 500 + 300 + 700 = 1500
        self.assertEqual(self.account.get_portfolio_value(), 1500.0)
        
        # Profit: 1500 - 1000 = 500
        self.assertEqual(self.account.get_profit_or_loss(), 500.0)


if __name__ == '__main__':
    unittest.main()