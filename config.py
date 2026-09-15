"""Общие константы проекта: URL, учётные данные, таймауты, лимиты из ТЗ."""

# ---------- URL ----------
BASE_URL: str = "http://91.197.96.80/"
ADMIN_MANAGE_URL: str = "http://91.197.96.80/manageProductsPage"
ADMIN_CREATE_URL: str = "http://91.197.96.80/createProduct"
EDIT_PRODUCT_URL_PART: str = "/editProduct/"
CREATE_PRODUCT_URL_PART: str = "/createProduct"

# ---------- Учётные данные ----------
BUYER_LOGIN: str = "покупатель1"
BUYER_PASSWORD: str = "покупатель1"
ADMIN_LOGIN: str = "admin"
ADMIN_PASSWORD: str = "admin"

# ---------- Таймауты (секунды) ----------
DEFAULT_TIMEOUT: int = 10
SHORT_TIMEOUT: int = 5
ANIMATION_DELAY: float = 1.5

# ---------- Лимиты из ТЗ ----------
MAX_UNITS_PER_PRODUCT: int = 100
MAX_CART_TOTAL: int = 100_000