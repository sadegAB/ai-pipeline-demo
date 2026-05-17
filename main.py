from fastapi import FastAPI
from config import settings
from middleware.cors import add_cors
from routers import health, customers, suppliers, products, warehouses, inventory, stock_movements, purchase_orders, sales_orders, invoices, payments, reports

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
)

add_cors(app)

# ── Routers ──
app.include_router(health.router)
app.include_router(customers.router)
app.include_router(suppliers.router)
app.include_router(products.router)
app.include_router(warehouses.router)
app.include_router(inventory.router)
app.include_router(stock_movements.router)
app.include_router(purchase_orders.router)
app.include_router(sales_orders.router)
app.include_router(invoices.router)
app.include_router(payments.router)
app.include_router(reports.router)

# ── Add new routers here ──
# from routers import books
# app.include_router(books.router)


@app.get("/", tags=["Root"])
def root():
    return {"message": f"Welcome to {settings.app_name}", "docs": "/docs"}