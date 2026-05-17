# Task: Build Mini ERP API From Zero on FastAPI Template

You are working inside a clean FastAPI template.

Build a new Mini ERP / Operations API from zero using the existing template conventions.

Do not reuse or reference the previous books CRUD test.
Do not assume books.py exists.
Do not create a new framework or project structure.

Use the existing FastAPI template structure:
- schemas/
- routers/
- main.py
- core/storage.py
- core/utils.py

No authentication is required.

Follow HANDOFF.md and AGENT_INSTRUCTIONS.md exactly.

Use:
- load_db()
- save_db()
- generate_id()
- now_iso()
- not_found()

Do not use SQLAlchemy.
Do not install new packages.
Use existing JSON db.json storage.

## Required System

Build APIs for these business areas:

1. Customers
2. Suppliers
3. Products
4. Warehouses
5. Inventory
6. Stock Movements
7. Purchase Orders
8. Sales Orders
9. Invoices
10. Payments
11. Reports

## Required DB Keys

- customers
- suppliers
- products
- warehouses
- inventory_items
- stock_movements
- purchase_orders
- sales_orders
- invoices
- payments

## High-Level Rules

Customers:
- CRUD.
- name required.
- email unique if provided.

Suppliers:
- CRUD.
- name required.
- email unique if provided.

Products:
- CRUD.
- fields: name, sku, description, unit_price, reorder_level.
- sku unique.
- unit_price >= 0.
- reorder_level >= 0.

Warehouses:
- CRUD.
- name required and unique.

Inventory:
- inventory item links product_id + warehouse_id + quantity.
- one inventory item per product_id + warehouse_id.
- quantity cannot be negative.
- low-stock means quantity <= product.reorder_level.

Stock Movements:
- add stock.
- remove stock.
- adjust stock.
- transfer stock between warehouses.
- every stock change creates a movement record.
- stock cannot go negative.

Purchase Orders:
- supplier_id required.
- items include product_id, quantity, unit_cost, line_total.
- starts as draft.
- approve draft.
- receive approved PO into warehouse and increase inventory.
- cannot receive twice.
- cannot cancel after received.

Sales Orders:
- customer_id required.
- warehouse_id required.
- items include product_id, quantity, unit_price, line_total.
- starts as draft.
- confirm validates stock and deducts inventory.
- cancel draft marks cancelled.
- cancel confirmed restores inventory.
- cannot confirm/cancel invalid statuses.

Invoices:
- create from confirmed sales order.
- one invoice per sales order.
- unpaid, partially_paid, paid.
- tracks total_amount, paid_amount, balance_due.

Payments:
- pay invoice.
- amount > 0.
- cannot exceed invoice balance.
- updates invoice paid_amount, balance_due, status.

Reports:
- low-stock report.
- inventory by warehouse.
- unpaid invoices.
- customer balance.
- product sales summary.

## Important Planning Rule

The Manager must not plan the whole project as one giant task queue.

Split the project into high-level phases first.

Then each phase should be planned into file-level tasks only when that phase starts.


## Planning Rules

- Do not create environment setup phases.
- Do not create configuration setup phases.
- The FastAPI template already exists and already runs.
- Every phase must directly produce application code or validation.
- Good phase examples:
  - Core entity schemas
  - Core CRUD routers
  - Inventory and stock movement logic
  - Purchase and sales order logic
  - Invoice and payment logic
  - Reports
  - Router registration and compile validation
- Bad phase examples:
  - Initial setup
  - Prepare environment
  - Configure project

## Dependency Rules

- You may install new packages if needed. If you add a new package, also add it to `requirements.txt` with the exact package name.
- Do not use EmailStr unless email-validator is already in requirements.txt.
- Use Optional[str] for email fields by default.

## Test Rules

- Do not create test files unless explicitly requested.
- For validation, use compile check:
  python3 -m compileall .

## Schema Rules

- Schemas define request/response shape and basic field constraints only.
- Do not read or write db.json inside schemas.
- Do not call load_db(), save_db(), or generate_id() inside schemas.
- Business rules such as unique sku, unique email, stock availability, order status transitions, and payment balance checks belong in routers or helper functions.
