from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

load_dotenv()

ORDERS_CSV = DATA_DIR / "orders.csv"
ORDER_ITEMS_CSV = DATA_DIR / "order_items.csv"
PRODUCTS_CSV = DATA_DIR / "products.csv"
USERS_CSV = DATA_DIR / "users.csv"
