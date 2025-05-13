# Rastreador de Despesas CLI

Uma aplicação de linha de comando para gerenciar suas finanças pessoais.

## Funcionalidades
- Adicionar despesas com descrição, valor e categoria
- Atualizar despesas existentes
- Remover despesas por ID
- Listar todas as despesas (com filtro por categoria)
- Resumo total das despesas e por mês
- Definir orçamento mensal e receber alerta ao ultrapassar
- Exportar despesas para arquivo CSV

## Requisitos
- Python 3.x

## Como usar

### Adicionar uma despesa
```sh
python expense_tracker.py add --description "Almoço" --amount 20 --category Alimentação
```

### Listar todas as despesas
```sh
python expense_tracker.py list
```

### Listar despesas de uma categoria
```sh
python expense_tracker.py list --category Alimentação
```

### Atualizar uma despesa
```sh
python expense_tracker.py update --id 1 --description "Jantar" --amount 30
```

### Remover uma despesa
```sh
python expense_tracker.py delete --id 1
```

### Resumo total das despesas
```sh
python expense_tracker.py summary
```

### Resumo das despesas de um mês específico
```sh
python expense_tracker.py summary --month 8
```

### Definir orçamento para um mês
```sh
python expense_tracker.py set-budget --year 2024 --month 8 --amount 500
```

### Exportar despesas para CSV
```sh
python expense_tracker.py export-csv --output minhas_despesas.csv
```

## Observações
- Os dados são salvos nos arquivos `expenses.json` e `budgets.json` na mesma pasta do script.
- Todos os comandos e mensagens estão em português brasileiro.
- Para ver a ajuda de cada comando, use:
  ```sh
  python expense_tracker.py <comando> --help
  ```

## Exemplo de saída
```
# ID  Data       Descrição    Categoria     Valor
# 1   2024-08-06  Almoço      Alimentação   R$20
# 2   2024-08-06  Jantar      Alimentação   R$30
```

---

Desenvolvido para praticar lógica de programação, manipulação de arquivos e criação de aplicações CLI em Python.
