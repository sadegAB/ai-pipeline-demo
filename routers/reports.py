from fastapi import APIRouter
from core.storage import load_db
from schemas.base import ResponseSchema

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/low-stock", response_model=list[ResponseSchema])
def get_low_stock_report():
    db = load_db()
    products = db.get("products", [])
    inventory_items = db.get("inventory_items", [])
    
    low_stock_items = []
    
    for product in products:
        product_id = product["id"]
        reorder_level = product["reorder_level"]
        
        total_quantity = 0
        for item in inventory_items:
            if item["product_id"] == product_id:
                total_quantity += item["quantity"]
        
        if total_quantity <= reorder_level:
            low_stock_items.append({
                "product_id": product_id,
                "product_name": product["name"],
                "total_quantity": total_quantity,
                "reorder_level": reorder_level
            })
    
    return low_stock_items

@router.get("/inventory-by-warehouse", response_model=list[ResponseSchema])
def get_inventory_by_warehouse_report():
    db = load_db()
    warehouses = db.get("warehouses", [])
    inventory_items = db.get("inventory_items", [])
    products = {product["id"]: product for product in db.get("products", [])}
    
    inventory_reports = []
    
    for warehouse in warehouses:
        warehouse_id = warehouse["id"]
        warehouse_name = warehouse["name"]
        
        warehouse_inventory = []
        for item in inventory_items:
            if item["warehouse_id"] == warehouse_id:
                product = products.get(item["product_id"])
                if product:
                    warehouse_inventory.append({
                        "product_id": item["product_id"],
                        "product_name": product["name"],
                        "quantity": item["quantity"]
                    })
        
        inventory_reports.append({
            "warehouse_id": warehouse_id,
            "warehouse_name": warehouse_name,
            "inventory": warehouse_inventory
        })
    
    return inventory_reports

@router.get("/unpaid-invoices", response_model=list[ResponseSchema])
def get_unpaid_invoices_report():
    db = load_db()
    invoices = db.get("invoices", [])
    
    unpaid_invoices = [
        invoice for invoice in invoices if invoice["status"] in ["unpaid", "partially_paid"]
    ]
    
    return unpaid_invoices

@router.get("/customer-balance", response_model=list[ResponseSchema])
def get_customer_balance_report():
    db = load_db()
    customers = db.get("customers", [])
    invoices = db.get("invoices", [])
    
    customer_balances = {}
    
    for invoice in invoices:
        customer_id = invoice["customer_id"]
        balance_due = invoice["balance_due"]
        
        if customer_id not in customer_balances:
            customer_balances[customer_id] = 0
        
        customer_balances[customer_id] += balance_due
    
    balance_report = []
    
    for customer in customers:
        customer_id = customer["id"]
        customer_name = customer["name"]
        balance = customer_balances.get(customer_id, 0)
        
        balance_report.append({
            "customer_id": customer_id,
            "customer_name": customer_name,
            "balance": balance
        })
    
    return balance_report

@router.get("/product-sales-summary", response_model=list[ResponseSchema])
def get_product_sales_summary_report():
    db = load_db()
    products = db.get("products", [])
    sales_orders = db.get("sales_orders", [])
    
    product_sales_summary = {}
    
    for product in products:
        product_id = product["id"]
        product_name = product["name"]
        
        product_sales_summary[product_id] = {
            "product_id": product_id,
            "product_name": product_name,
            "total_quantity_sold": 0,
            "total_sales_amount": 0
        }
    
    for order in sales_orders:
        if order["status"] == "confirmed":
            for item in order["items"]:
                product_id = item["product_id"]
                quantity = item["quantity"]
                unit_price = item["unit_price"]
                
                if product_id in product_sales_summary:
                    product_sales_summary[product_id]["total_quantity_sold"] += quantity
                    product_sales_summary[product_id]["total_sales_amount"] += quantity * unit_price
    
    return list(product_sales_summary.values())