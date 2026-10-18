# project3.py
# Personal Expense Tracker with CSV

import csv
from datetime import datetime
from collections import defaultdict
import os

FILE = "expenses.csv"
FIELDS = ["date", "category", "description", "amount"]
CATEGORIES = ["Food", "Travel", "Study", "Bills", "Fun", "Other"]

def initialize_file():
    '''Creates the CSV file with headers if it does not exist.'''
    if not os.path.exists(FILE):
        with open(FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()

def save_expense(row):
    '''Saves a single expense row to the CSV file.'''
    initialize_file()
    with open(FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writerow(row)

def load_expenses():
    '''Loads all expenses from the CSV file.'''
    try:
        with open(FILE, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []

def read_date(prompt):
    '''Reads and validates a date string in YYYY-MM-DD format.'''
    while True:
        date_str = input(prompt).strip()
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

def read_amount(prompt):
    '''Reads and validates a positive float amount.'''
    while True:
        try:
            val = float(input(prompt))
            if val < 0:
                print("Amount cannot be negative.")
                continue
            return val
        except ValueError:
            print("Invalid amount. Please enter a number.")

def add_expense():
    '''Prompts the user to enter a new expense and saves it.'''
    print("\n--- Add Expense ---")
    date = read_date("Date (YYYY-MM-DD): ")
    
    print("Categories:", ", ".join(CATEGORIES))
    category = input("Category: ").strip().capitalize()
    if category not in CATEGORIES:
        print(f"Warning: '{category}' is not a standard category, but it will be saved.")
        
    description = input("Description: ").strip()
    amount = read_amount("Amount: ")
    
    expense = {
        "date": date,
        "category": category,
        "description": description,
        "amount": f"{amount:.2f}"
    }
    save_expense(expense)
    print("Expense added successfully!")

def print_table(expenses):
    '''Prints a list of expenses in a formatted table.'''
    if not expenses:
        print("No expenses found.")
        return
        
    print(f"\n{'Date':<12} | {'Category':<15} | {'Description':<25} | {'Amount':<10}")
    print("-" * 70)
    for row in expenses:
        print(f"{row['date']:<12} | {row['category']:<15} | {row['description']:<25} | ${float(row['amount']):<9.2f}")
    print("-" * 70)

def filter_expenses():
    '''Filters expenses by category or month.'''
    expenses = load_expenses()
    if not expenses:
        print("No expenses to filter.")
        return

    print("\n1) Filter by Category")
    print("2) Filter by Month")
    choice = input("Choose filter type: ").strip()
    
    if choice == "1":
        cat = input("Enter category to filter by: ").strip().capitalize()
        filtered = [e for e in expenses if e["category"].lower() == cat.lower()]
        print(f"\n--- Expenses for Category: {cat} ---")
        print_table(filtered)
    elif choice == "2":
        month = input("Enter month (YYYY-MM): ").strip()
        filtered = [e for e in expenses if e["date"].startswith(month)]
        print(f"\n--- Expenses for Month: {month} ---")
        print_table(filtered)
    else:
        print("Invalid choice.")

def show_summary():
    '''Displays total spending per category, grand total, and largest single expense.'''
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return

    totals = defaultdict(float)
    grand_total = 0.0
    biggest_expense = None
    max_amount = -1.0

    for r in expenses:
        amt = float(r["amount"])
        totals[r["category"]] += amt
        grand_total += amt
        
        if amt > max_amount:
            max_amount = amt
            biggest_expense = r

    print("\n--- Spending Summary ---")
    print(f"{'Category':<15} | {'Total':<10}")
    print("-" * 30)
    for cat, total in sorted(totals.items()):
        print(f"{cat:<15} | ${total:<9.2f}")
    print("-" * 30)
    print(f"Grand Total: ${grand_total:.2f}")
    
    if biggest_expense:
        print(f"\nLargest Single Expense: ${max_amount:.2f} on {biggest_expense['date']} ({biggest_expense['description']})")

def main():
    '''Main menu loop.'''
    initialize_file()
    while True:
        print("\n=== Expense Tracker ===")
        print("1) Add expense")
        print("2) View all")
        print("3) Filter")
        print("4) Summary")
        print("5) Quit")
        
        choice = input("Choose an option (1-5): ").strip()
        
        if choice == "1":
            add_expense()
        elif choice == "2":
            print_table(load_expenses())
        elif choice == "3":
            filter_expenses()
        elif choice == "4":
            show_summary()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == '__main__':
    main()
