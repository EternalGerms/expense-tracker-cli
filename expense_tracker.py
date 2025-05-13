import argparse
import json
import os
from datetime import datetime
import csv

DATA_FILE = 'expenses.json'
BUDGET_FILE = 'budgets.json'

def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_expenses(expenses):
    with open(DATA_FILE, 'w') as f:
        json.dump(expenses, f, indent=2)

def load_budgets():
    if not os.path.exists(BUDGET_FILE):
        return {}
    with open(BUDGET_FILE, 'r') as f:
        return json.load(f)

def save_budgets(budgets):
    with open(BUDGET_FILE, 'w') as f:
        json.dump(budgets, f, indent=2)

def get_month_key(year, month):
    return f"{year}-{month:02d}"

def main():
    parser = argparse.ArgumentParser(description='Expense Tracker CLI')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new expense')
    add_parser.add_argument('--description', required=True, help='Expense description')
    add_parser.add_argument('--amount', required=True, type=float, help='Expense amount')
    add_parser.add_argument('--category', required=True, help='Expense category')

    # List command
    list_parser = subparsers.add_parser('list', help='List all expenses')
    list_parser.add_argument('--category', help='Filter expenses by category')

    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete an expense by ID')
    delete_parser.add_argument('--id', required=True, type=int, help='Expense ID to delete')

    # Summary command
    summary_parser = subparsers.add_parser('summary', help='Show expenses summary')
    summary_parser.add_argument('--month', type=int, help='Show summary for a specific month (1-12)')

    # Update command
    update_parser = subparsers.add_parser('update', help='Update an expense by ID')
    update_parser.add_argument('--id', required=True, type=int, help='Expense ID to update')
    update_parser.add_argument('--description', help='New description')
    update_parser.add_argument('--amount', type=float, help='New amount')

    # Set budget command
    budget_parser = subparsers.add_parser('set-budget', help='Set a budget for a specific month and year')
    budget_parser.add_argument('--year', type=int, required=True, help='Year for the budget (e.g. 2024)')
    budget_parser.add_argument('--month', type=int, required=True, help='Month for the budget (1-12)')
    budget_parser.add_argument('--amount', type=float, required=True, help='Budget amount')

    # Export CSV command
    export_parser = subparsers.add_parser('export-csv', help='Export all expenses to a CSV file')
    export_parser.add_argument('--output', default='expenses.csv', help='Output CSV file name (default: expenses.csv)')

    args = parser.parse_args()

    # Placeholder for command logic
    if args.command == 'add':
        expenses = load_expenses()
        budgets = load_budgets()
        new_id = 1 if not expenses else max(e['id'] for e in expenses) + 1
        today = datetime.now().strftime('%Y-%m-%d')
        if args.amount < 0:
            print('Error: Amount cannot be negative.')
            return
        new_expense = {
            'id': new_id,
            'date': today,
            'description': args.description,
            'amount': args.amount,
            'category': args.category
        }
        expenses.append(new_expense)
        save_expenses(expenses)
        # Check budget
        now = datetime.now()
        month_key = get_month_key(now.year, now.month)
        budget = budgets.get(month_key)
        month_total = sum(e['amount'] for e in expenses if datetime.strptime(e['date'], '%Y-%m-%d').year == now.year and datetime.strptime(e['date'], '%Y-%m-%d').month == now.month)
        print(f'Expense added successfully (ID: {new_id})')
        if budget is not None and month_total > budget:
            print(f'Warning: You have exceeded your budget for {now.strftime("%B %Y")} (${budget})!')
    elif args.command == 'list':
        expenses = load_expenses()
        if args.category:
            expenses = [e for e in expenses if e.get('category', '').lower() == args.category.lower()]
        if not expenses:
            print('No expenses found.')
            return
        print(f'# ID  Date       Description  Category     Amount')
        for e in expenses:
            print(f"# {e['id']}   {e['date']}  {e['description']:<12}  {e.get('category',''):<12}  ${int(e['amount']) if e['amount'].is_integer() else e['amount']}")
    elif args.command == 'delete':
        expenses = load_expenses()
        expense_to_delete = next((e for e in expenses if e['id'] == args.id), None)
        if not expense_to_delete:
            print('Error: Expense ID not found.')
            return
        expenses = [e for e in expenses if e['id'] != args.id]
        save_expenses(expenses)
        print('Expense deleted successfully')
    elif args.command == 'set-budget':
        budgets = load_budgets()
        if args.amount < 0:
            print('Error: Budget amount cannot be negative.')
            return
        month_key = get_month_key(args.year, args.month)
        budgets[month_key] = args.amount
        save_budgets(budgets)
        print(f'Budget set for {args.year}-{args.month:02d}: ${args.amount}')
    elif args.command == 'summary':
        expenses = load_expenses()
        budgets = load_budgets()
        if args.month:
            now = datetime.now()
            year = now.year
            month = args.month
            filtered = [e for e in expenses if datetime.strptime(e['date'], '%Y-%m-%d').month == month and datetime.strptime(e['date'], '%Y-%m-%d').year == year]
            total = sum(e['amount'] for e in filtered)
            month_name = datetime(year, month, 1).strftime('%B')
            month_key = get_month_key(year, month)
            budget = budgets.get(month_key)
            print(f'Total expenses for {month_name}: ${int(total) if float(total).is_integer() else total}')
            if budget is not None:
                print(f'Budget for {month_name}: ${int(budget) if float(budget).is_integer() else budget}')
                if total > budget:
                    print(f'Warning: You have exceeded your budget for {month_name}!')
        else:
            total = sum(e['amount'] for e in expenses)
            print(f'Total expenses: ${int(total) if float(total).is_integer() else total}')
    elif args.command == 'update':
        expenses = load_expenses()
        expense = next((e for e in expenses if e['id'] == args.id), None)
        if not expense:
            print('Error: Expense ID not found.')
            return
        updated = False
        if args.description is not None:
            expense['description'] = args.description
            updated = True
        if args.amount is not None:
            if args.amount < 0:
                print('Error: Amount cannot be negative.')
                return
            expense['amount'] = args.amount
            updated = True
        if updated:
            save_expenses(expenses)
            print('Expense updated successfully')
        else:
            print('No updates provided.')
    elif args.command == 'export-csv':
        expenses = load_expenses()
        if not expenses:
            print('No expenses to export.')
            return
        fieldnames = ['id', 'date', 'description', 'amount', 'category']
        with open(args.output, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for e in expenses:
                # Ensure all fields are present for each expense
                row = {k: e.get(k, '') for k in fieldnames}
                writer.writerow(row)
        print(f'Expenses exported to {args.output}')

if __name__ == '__main__':
    main() 