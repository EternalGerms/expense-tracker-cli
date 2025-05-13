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
    parser = argparse.ArgumentParser(description='Rastreador de Despesas CLI')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Comando adicionar
    add_parser = subparsers.add_parser('add', help='Adicionar uma nova despesa')
    add_parser.add_argument('--description', required=True, help='Descrição da despesa')
    add_parser.add_argument('--amount', required=True, type=float, help='Valor da despesa')
    add_parser.add_argument('--category', required=True, help='Categoria da despesa')

    # Comando listar
    list_parser = subparsers.add_parser('list', help='Listar todas as despesas')
    list_parser.add_argument('--category', help='Filtrar despesas por categoria')

    # Comando deletar
    delete_parser = subparsers.add_parser('delete', help='Remover uma despesa pelo ID')
    delete_parser.add_argument('--id', required=True, type=int, help='ID da despesa a ser removida')

    # Comando resumo
    summary_parser = subparsers.add_parser('summary', help='Mostrar resumo das despesas')
    summary_parser.add_argument('--month', type=int, help='Mostrar resumo para um mês específico (1-12)')

    # Comando atualizar
    update_parser = subparsers.add_parser('update', help='Atualizar uma despesa pelo ID')
    update_parser.add_argument('--id', required=True, type=int, help='ID da despesa a ser atualizada')
    update_parser.add_argument('--description', help='Nova descrição')
    update_parser.add_argument('--amount', type=float, help='Novo valor')

    # Comando definir orçamento
    budget_parser = subparsers.add_parser('set-budget', help='Definir um orçamento para um mês e ano específicos')
    budget_parser.add_argument('--year', type=int, required=True, help='Ano do orçamento (ex: 2024)')
    budget_parser.add_argument('--month', type=int, required=True, help='Mês do orçamento (1-12)')
    budget_parser.add_argument('--amount', type=float, required=True, help='Valor do orçamento')

    # Comando exportar CSV
    export_parser = subparsers.add_parser('export-csv', help='Exportar todas as despesas para um arquivo CSV')
    export_parser.add_argument('--output', default='expenses.csv', help='Nome do arquivo CSV de saída (padrão: expenses.csv)')

    args = parser.parse_args()

    if args.command == 'add':
        expenses = load_expenses()
        budgets = load_budgets()
        new_id = 1 if not expenses else max(e['id'] for e in expenses) + 1
        today = datetime.now().strftime('%Y-%m-%d')
        if args.amount < 0:
            print('Erro: O valor não pode ser negativo.')
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
        # Verificar orçamento
        now = datetime.now()
        month_key = get_month_key(now.year, now.month)
        budget = budgets.get(month_key)
        month_total = sum(e['amount'] for e in expenses if datetime.strptime(e['date'], '%Y-%m-%d').year == now.year and datetime.strptime(e['date'], '%Y-%m-%d').month == now.month)
        print(f'Despesa adicionada com sucesso (ID: {new_id})')
        if budget is not None and month_total > budget:
            print(f'Atenção: Você excedeu seu orçamento para {now.strftime("%B de %Y")} (R${budget})!')
    elif args.command == 'list':
        expenses = load_expenses()
        if args.category:
            expenses = [e for e in expenses if e.get('category', '').lower() == args.category.lower()]
        if not expenses:
            print('Nenhuma despesa encontrada.')
            return
        print(f'# ID  Data       Descrição    Categoria     Valor')
        for e in expenses:
            print(f"# {e['id']}   {e['date']}  {e['description']:<12}  {e.get('category',''):<12}  R${int(e['amount']) if e['amount'] and float(e['amount']).is_integer() else e['amount']}")
    elif args.command == 'delete':
        expenses = load_expenses()
        expense_to_delete = next((e for e in expenses if e['id'] == args.id), None)
        if not expense_to_delete:
            print('Erro: ID da despesa não encontrado.')
            return
        expenses = [e for e in expenses if e['id'] != args.id]
        save_expenses(expenses)
        print('Despesa removida com sucesso')
    elif args.command == 'set-budget':
        budgets = load_budgets()
        if args.amount < 0:
            print('Erro: O valor do orçamento não pode ser negativo.')
            return
        month_key = get_month_key(args.year, args.month)
        budgets[month_key] = args.amount
        save_budgets(budgets)
        print(f'Orçamento definido para {args.year}-{args.month:02d}: R${args.amount}')
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
            print(f'Despesas totais para {month_name}: R${int(total) if float(total).is_integer() else total}')
            if budget is not None:
                print(f'Orçamento para {month_name}: R${int(budget) if float(budget).is_integer() else budget}')
                if total > budget:
                    print(f'Atenção: Você excedeu seu orçamento para {month_name}!')
        else:
            total = sum(e['amount'] for e in expenses)
            print(f'Despesas totais: R${int(total) if float(total).is_integer() else total}')
    elif args.command == 'update':
        expenses = load_expenses()
        expense = next((e for e in expenses if e['id'] == args.id), None)
        if not expense:
            print('Erro: ID da despesa não encontrado.')
            return
        updated = False
        if args.description is not None:
            expense['description'] = args.description
            updated = True
        if args.amount is not None:
            if args.amount < 0:
                print('Erro: O valor não pode ser negativo.')
                return
            expense['amount'] = args.amount
            updated = True
        if updated:
            save_expenses(expenses)
            print('Despesa atualizada com sucesso')
        else:
            print('Nenhuma atualização fornecida.')
    elif args.command == 'export-csv':
        expenses = load_expenses()
        if not expenses:
            print('Nenhuma despesa para exportar.')
            return
        fieldnames = ['id', 'date', 'description', 'amount', 'category']
        with open(args.output, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for e in expenses:
                row = {k: e.get(k, '') for k in fieldnames}
                writer.writerow(row)
        print(f'Despesas exportadas para {args.output}')

if __name__ == '__main__':
    main() 