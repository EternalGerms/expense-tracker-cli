import argparse
import json
import os
from datetime import datetime

DATA_FILE = 'expenses.json'

def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_expenses(expenses):
    with open(DATA_FILE, 'w') as f:
        json.dump(expenses, f, indent=2)

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

    args = parser.parse_args()

    # Placeholder for command logic
    if args.command == 'add':
        expenses = load_expenses()
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
        print(f'Expense added successfully (ID: {new_id})')
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
    elif args.command == 'summary':
        expenses = load_expenses()
        if args.month:
            # Filter by month (current year)
            now = datetime.now()
            filtered = [e for e in expenses if datetime.strptime(e['date'], '%Y-%m-%d').month == args.month and datetime.strptime(e['date'], '%Y-%m-%d').year == now.year]
            total = sum(e['amount'] for e in filtered)
            month_name = datetime(now.year, args.month, 1).strftime('%B')
            print(f'Total expenses for {month_name}: ${int(total) if float(total).is_integer() else total}')
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

if __name__ == '__main__':
    main() 