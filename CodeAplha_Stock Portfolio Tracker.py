# ==========================================================
# CodeAlpha Internship - Task 2: Stock Portfolio Tracker
# Features: Buy, Sell, Cash Wallet, Portfolio Summary & Export
# ==========================================================

# 1. Market Benchmark Stock Prices
STOCK_PRICES = {
    "AAPL": 180.0,
    "TSLA": 250.0,
    "GOOGL": 140.0,
    "MSFT": 420.0,
    "TCS": 3500.0,
    "INFY": 1600.0
}

# Initial Account State
wallet_balance = 10000.0  # Starting with $10,000 in cash
portfolio = {}            # Format: {"STOCK_SYMBOL": quantity}


def display_market():
    """Display current market prices."""
    print("\n" + "=" * 45)
    print(f"{'Stock':<10} | {'Price ($)':>12}")
    print("-" * 45)
    for stock, price in STOCK_PRICES.items():
        print(f"{stock:<10} | ${price:>11.2f}")
    print("=" * 45)


def view_wallet():
    """Check current liquid cash balance."""
    print(f"\n💵 Current Wallet Balance: ${wallet_balance:,.2f}")


def buy_stock():
    """Purchase shares by deducting funds from the cash wallet."""
    global wallet_balance

    stock = input("\nEnter stock symbol to BUY: ").strip().upper()
    if stock not in STOCK_PRICES:
        print(f"❌ Error: '{stock}' is not listed in active market symbols.")
        return

    try:
        qty = int(input(f"Enter quantity of shares to buy for {stock}: "))
        if qty <= 0:
            print("❌ Quantity must be greater than zero.")
            return
    except ValueError:
        print("❌ Invalid entry! Please enter a valid whole number.")
        return

    price = STOCK_PRICES[stock]
    total_cost = qty * price

    # Verify wallet has sufficient funds
    if total_cost > wallet_balance:
        print(f"\n❌ Transaction Failed: Insufficient funds!")
        print(f"   Required: ${total_cost:,.2f} | Available in Wallet: ${wallet_balance:,.2f}")
        return

    # Process Transaction
    wallet_balance -= total_cost
    portfolio[stock] = portfolio.get(stock, 0) + qty

    print(f"\n✅ Bought {qty} share(s) of {stock} at ${price:,.2f} each.")
    print(f"   Amount Debited: ${total_cost:,.2f}")
    print(f"   Remaining Wallet Balance: ${wallet_balance:,.2f}")


def sell_stock():
    """Sell shares and credit funds back to the cash wallet."""
    global wallet_balance

    if not portfolio:
        print("\n❌ Your portfolio is empty! Nothing to sell.")
        return

    stock = input("\nEnter stock symbol to SELL: ").strip().upper()
    if stock not in portfolio:
        print(f"❌ You do not hold any shares of '{stock}'.")
        return

    current_qty = portfolio[stock]

    try:
        qty = int(input(f"Enter quantity to sell (You currently own {current_qty}): "))
        if qty <= 0:
            print("❌ Quantity must be greater than zero.")
            return
    except ValueError:
        print("❌ Invalid entry! Please enter a valid whole number.")
        return

    # Check holdings limit
    if qty > current_qty:
        print(f"❌ Transaction Failed: Cannot sell {qty} shares! You only own {current_qty}.")
        return

    price = STOCK_PRICES[stock]
    total_revenue = qty * price

    # Update holdings
    if qty == current_qty:
        del portfolio[stock]
    else:
        portfolio[stock] -= qty

    # Credit proceeds to wallet
    wallet_balance += total_revenue

    print(f"\n✅ Sold {qty} share(s) of {stock} at ${price:,.2f} each.")
    print(f"   Amount Credited: ${total_revenue:,.2f}")
    print(f"   Updated Wallet Balance: ${wallet_balance:,.2f}")


def display_portfolio():
    """Display portfolio holdings, current equity, and net worth."""
    stock_value = 0.0

    print("\n" + "=" * 60)
    print("                     PORTFOLIO SUMMARY")
    print("=" * 60)

    if not portfolio:
        print(" [!] No stocks owned currently.")
    else:
        print(f"{'Stock':<10} {'Qty':>10} {'Price ($)':>18} {'Total Value ($)':>18}")
        print("-" * 60)
        for stock, qty in portfolio.items():
            price = STOCK_PRICES[stock]
            item_total = qty * price
            stock_value += item_total
            print(f"{stock:<10} {qty:>10} ${price:>17.2f} ${item_total:>17.2f}")

    total_net_worth = wallet_balance + stock_value

    print("-" * 60)
    print(f"💰 Stock Holdings Value: ${stock_value:>15,.2f}")
    print(f"💵 Available Cash:       ${wallet_balance:>15,.2f}")
    print("=" * 60)
    print(f"📊 NET ACCOUNT WORTH:    ${total_net_worth:>15,.2f}")
    print("=" * 60)


def export_report():
    """Optionally export account statement to a text file."""
    if not portfolio and wallet_balance == 10000.0:
        print("\n[!] No transaction activity to save.")
        return

    filename = "portfolio_statement.txt"
    stock_value = sum(qty * STOCK_PRICES[stock] for stock, qty in portfolio.items())
    total_net_worth = wallet_balance + stock_value

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("==================================================\n")
            f.write("           STOCK PORTFOLIO STATEMENT\n")
            f.write("==================================================\n\n")
            f.write(f"{'Stock':<10} {'Qty':>8} {'Unit Price':>14} {'Total Value':>14}\n")
            f.write("-" * 50 + "\n")
            for stock, qty in portfolio.items():
                price = STOCK_PRICES[stock]
                f.write(f"{stock:<10} {qty:>8} ${price:>13.2f} ${qty * price:>13.2f}\n")
            f.write("-" * 50 + "\n")
            f.write(f"Stock Holdings:   ${stock_value:,.2f}\n")
            f.write(f"Cash Balance:     ${wallet_balance:,.2f}\n")
            f.write("=" * 50 + "\n")
            f.write(f"TOTAL NET WORTH:  ${total_net_worth:,.2f}\n")
            f.write("==================================================\n")
        print(f"\n📁 Statement saved successfully as '{filename}'!")
    except OSError as err:
        print(f"❌ Failed to save file: {err}")


def main():
    """Main dashboard menu loop."""
    print("=" * 60)
    print("   📈 ADVANCED STOCK PORTFOLIO TRACKER WITH CASH WALLET 📈")
    print("=" * 60)

    while True:
        print("\nAction Menu:")
        print("1. View Market Prices")
        print("2. Check Wallet Balance")
        print("3. Buy Shares")
        print("4. Sell Shares")
        print("5. View Portfolio Summary & Net Worth")
        print("6. Export Summary to TXT")
        print("7. Exit")

        choice = input("\nSelect an option (1-7): ").strip()

        if choice == "1":
            display_market()
        elif choice == "2":
            view_wallet()
        elif choice == "3":
            buy_stock()
        elif choice == "4":
            sell_stock()
        elif choice == "5":
            display_portfolio()
        elif choice == "6":
            export_report()
        elif choice == "7":
            print("\nThank you for using Stock Portfolio Tracker. Goodbye!")
            break
        else:
            print("❌ Invalid option. Please enter a number between 1 and 7.")


if __name__ == "__main__":
    main()