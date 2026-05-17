from pydantic import BaseModel
from typing import List

class CustomerBalanceItem(BaseModel):
    customer_id: str
    total_balance: float

class CustomerBalanceReport(BaseModel):
    items: List[CustomerBalanceItem]

class ProductSalesSummaryItem(BaseModel):
    product_id: str
    total_quantity_sold: int
    total_sales_amount: float

class ProductSalesSummaryReport(BaseModel):
    items: List[ProductSalesSummaryItem]