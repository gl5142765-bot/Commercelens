import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

DB_URL = os.getenv("DB_URL", "sqlite:///commerce.db")
DB_PATH = os.path.join(PROJECT_ROOT, "commerce.db")

ORDERS_CSV = os.path.join(DATA_DIR, "orders.csv")
ORDER_ITEMS_CSV = os.path.join(DATA_DIR, "order_items.csv")
PRODUCTS_CSV = os.path.join(DATA_DIR, "products.csv")
USERS_CSV = os.path.join(DATA_DIR, "users.csv")

LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "gpt-4o-mini")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1/chat/completions")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

print("LLM_MODEL_NAME:", LLM_MODEL_NAME)
print("LLM_BASE_URL:", LLM_BASE_URL)
print("OPENAI_API_KEY:", OPENAI_API_KEY[:6], "...")