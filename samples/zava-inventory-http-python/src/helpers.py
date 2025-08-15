import os
import json
from typing import Any, Dict, List

def is_duplicate_product(products, name, category, exclude_id=None):
    name = name.strip().lower()
    category = category.strip().lower()
    for product in products:
        if exclude_id is not None and product['id'] == exclude_id:
            continue
        if product['name'].strip().lower() == name and product['category'].strip().lower() == category:
            return True
    return False

def is_duplicate_store(stores, name, address, exclude_id=None):
    name = name.strip().lower()
    address = address.strip().lower()
    for store in stores:
        if exclude_id is not None and store['id'] == exclude_id:
            continue
        if store['name'].strip().lower() == name and store['address'].strip().lower() == address:
            return True
    return False

def build_inventory_per_store(product_id: int, stores: list, inventory: list) -> list:
    """
    Build inventory per store for a given product.
    :param product_id: The product ID.
    :param stores: List of store dicts.
    :param inventory: List of inventory dicts.
    :return: List of inventory info per store.
    """
    store_inventory = []
    for store in stores:
        store_id = store["id"]
        inv_record = next((item for item in inventory if item["productId"] == product_id and item["storeId"] == store_id), None)
        store_inventory.append({
            "storeId": store_id,
            "storeName": store["name"],
            "quantity": inv_record["quantity"] if inv_record else 0
        })
    return store_inventory

def get_data_file_path(filename: str) -> str:
    # Try /code/data (container) first, then ../data (local dev)
    container_data_dir = "/code/data"
    local_data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
    container_path = os.path.join(container_data_dir, filename)
    local_path = os.path.join(local_data_dir, filename)
    if os.path.exists(container_path):
        return container_path
    return local_path

def load_json_data(filename: str) -> List[Dict[str, Any]]:
    try:
        with open(get_data_file_path(filename), 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_json_data(filename: str, data: List[Dict[str, Any]]) -> None:
    with open(get_data_file_path(filename), 'w') as file:
        json.dump(data, file, indent=2)

def get_next_id(items: List[Dict[str, Any]]) -> int:
    if items:
        return max(item.get('id', 0) for item in items) + 1
    return 1

def generate_sku(product_name: str, product_id: int) -> str:
    common_words = {'and', 'the', 'a', 'an', 'with', 'for', 'of', 'in', 'on', 'at', 'to', 'from'}
    words = [word for word in product_name.lower().split() if word not in common_words]
    abbreviation = ''.join([word[0].upper() for word in words[:3]])
    if len(abbreviation) < 2:
        abbreviation = product_name.replace(' ', '')[:3].upper()
    return f"{abbreviation}-{product_id:03d}"

def tool_error_handler(default_return=None):
    from functools import wraps
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                result = {
                    "success": False,
                    "error": f"An error occurred: {str(e)}"
                }
                if default_return is not None:
                    result.update(default_return)
                return result
        return wrapper
    return decorator
