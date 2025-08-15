# region Imports

import os
import multiprocessing
import uvicorn
import logging
from typing import Any, Dict
from helpers import (
    load_json_data,
    save_json_data,
    get_next_id,
    generate_sku,
    tool_error_handler,
    is_duplicate_product,
    is_duplicate_store,
    build_inventory_per_store
)
from starlette.responses import PlainTextResponse
from middleware import AuthMiddleware
from mcp.server.fastmcp import FastMCP

# endregion

# region Logging Setup

logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(levelname)s %(message)s')

# endregion

# region MCP Server Setup

mcp = FastMCP("\U0001F4E6 Zava Inventory MCP", stateless_http=True)
app = mcp.streamable_http_app()
app.add_middleware(AuthMiddleware)
app.debug = False

# endregion

# region MCP Tool Functions - Products


@tool_error_handler(default_return={"products": []})
@mcp.tool()
def get_products() -> Dict[str, Any]:
    """Retrieve all products from the inventory."""
    products = load_json_data("products.json")
    stores = load_json_data("stores.json")
    inventory = load_json_data("inventory.json")
    logging.info("All products retrieved: %d products", len(products))
    products_with_inventory = []
    for product in products:
        product_id = product["id"]
        product_with_inventory = dict(product)
        product_with_inventory["inventoryPerStore"] = build_inventory_per_store(product_id, stores, inventory)
        products_with_inventory.append(product_with_inventory)
    return {
        "success": True,
        "count": len(products_with_inventory),
        "products": products_with_inventory
    }

@tool_error_handler()
@mcp.tool()
def get_product_by_id(product_id: int) -> Dict[str, Any]:
    """
    Retrieve a product by its ID.

    :param product_id: The unique integer ID of the product to retrieve.
    :return: A dictionary with the result and the product details if found.
    """
    products = load_json_data("products.json")
    stores = load_json_data("stores.json")
    inventory = load_json_data("inventory.json")
    product = next((product for product in products if product['id'] == product_id), None)
    if product is None:
        logging.warning("Failed to get product: Product ID %s not found", product_id)
        return {
            "success": False,
            "error": f"Product with ID {product_id} not found"
        }
    product_with_inventory = dict(product)
    product_with_inventory["inventoryPerStore"] = build_inventory_per_store(product_id, stores, inventory)
    logging.info("Product retrieved: ID %s", product_id)
    return {
        "success": True,
        "product": product_with_inventory
    }

@tool_error_handler()
@mcp.tool()
def add_product(name: str, category: str, price: float, description: str = "") -> Dict[str, Any]:
    """
    Add a new product to the inventory.

    :param name: The name of the product (required).
    :param category: The category of the product (required).
    :param price: The price of the product (required, must be non-negative).
    :param description: A short description of the product (optional).
    :return: A dictionary with the result and the new product details.
    """
    products = load_json_data("products.json")
    if is_duplicate_product(products, name, category):
        logging.warning("Duplicate product detected: name='%s', category='%s'", name, category)
        return {"success": False, "error": f"A product with the name '{name}' and category '{category}' already exists."}
    if not name or not isinstance(name, str):
        logging.warning("Failed to add product: Invalid name '%s'", name)
        return {"success": False, "error": "Product name is required and must be a string."}
    if not category or not isinstance(category, str):
        logging.warning("Failed to add product: Invalid category '%s'", category)
        return {"success": False, "error": "Product category is required and must be a string."}
    if price is None or not isinstance(price, (int, float)) or price < 0:
        logging.warning("Failed to add product: Invalid price '%s'", price)
        return {"success": False, "error": "Product price is required and must be a non-negative number."}
    products = load_json_data("products.json")
    next_id = get_next_id(products)
    sku = generate_sku(name, next_id)
    new_product = {
        "id": next_id,
        "name": name,
        "category": category,
        "price": price,
        "sku": sku,
        "description": description
    }
    products.append(new_product)
    save_json_data("products.json", products)
    logging.info(f"Product added: {new_product}")
    return {
        "success": True,
        "message": f"Product '{name}' added successfully with SKU {sku}",
        "product": new_product
    }

@tool_error_handler()
@mcp.tool()
def update_product(product_id: int, name: str = None, category: str = None, price: float = None, description: str = None) -> Dict[str, Any]:
    """
    Update an existing product's details by ID.

    :param product_id: The unique integer ID of the product to update.
    :param name: The new name for the product (optional).
    :param category: The new category for the product (optional).
    :param price: The new price for the product (optional, must be non-negative).
    :param description: The new description for the product (optional).
    :return: A dictionary with the result and the updated product details.
    """
    products = load_json_data("products.json")
    # Duplicate detection: if name or category is being updated, check for another product with the same name and category (excluding this product)
    check_name = name if name is not None else None
    check_category = category if category is not None else None
    if check_name is not None or check_category is not None:
        # Use current product values if not provided
        product = next((product for product in products if product['id'] == product_id), None)
        if product:
            name_to_check = check_name if check_name is not None else product['name']
            category_to_check = check_category if check_category is not None else product['category']
            if is_duplicate_product(products, name_to_check, category_to_check, exclude_id=product_id):
                logging.warning("Duplicate product detected on update: name='%s', category='%s'", name_to_check, category_to_check)
                return {"success": False, "error": f"A product with the name '{name_to_check}' and category '{category_to_check}' already exists."}
    product = next((product for product in products if product['id'] == product_id), None)
    if product is None:
        logging.warning("Failed to update product: Product ID %s not found", product_id)
        return {
            "success": False,
            "error": f"Product with ID {product_id} not found"
        }
    updated_fields = []
    if name is not None:
        if not name or not isinstance(name, str):
            logging.warning("Failed to update product: Invalid name '%s' for product ID %s", name, product_id)
            return {"success": False, "error": "Product name must be a non-empty string."}
        product['name'] = name
        updated_fields.append('name')
    if category is not None:
        if not category or not isinstance(category, str):
            logging.warning("Failed to update product: Invalid category '%s' for product ID %s", category, product_id)
            return {"success": False, "error": "Product category must be a non-empty string."}
        product['category'] = category
        updated_fields.append('category')
    if price is not None:
        if not isinstance(price, (int, float)) or price < 0:
            logging.warning("Failed to update product: Invalid price '%s' for product ID %s", price, product_id)
            return {"success": False, "error": "Product price must be a non-negative number."}
        product['price'] = price
        updated_fields.append('price')
    if description is not None:
        product['description'] = description
        updated_fields.append('description')
    if not updated_fields:
        logging.warning("Failed to update product: No fields provided for product ID %s", product_id)
        return {
            "success": False,
            "error": "No fields provided to update"
        }
    save_json_data("products.json", products)
    logging.info(f"Product updated (ID {product_id}): fields {updated_fields}")
    return {
        "success": True,
        "message": f"Product ID {product_id} updated successfully. Updated fields: {', '.join(updated_fields)}",
        "product": product,
        "updated_fields": updated_fields
    }

@tool_error_handler()
@mcp.tool()
def remove_product(product_id: int) -> Dict[str, Any]:
    """
    Remove a product from the inventory by ID.

    :param product_id: The unique integer ID of the product to remove.
    :return: A dictionary with the result and the removed product details.
    """
    products = load_json_data("products.json")
    product_to_remove = None
    for product in products:
        if product['id'] == product_id:
            product_to_remove = product
            break
    if product_to_remove is None:
        logging.warning("Failed to remove product: Product ID %s not found", product_id)
        return {
            "success": False,
            "error": f"Product with ID {product_id} not found"
        }
    products.remove(product_to_remove)
    save_json_data("products.json", products)
    logging.info(f"Product removed: {product_to_remove}")
    return {
        "success": True,
        "message": f"Product '{product_to_remove['name']}' (ID: {product_id}) removed successfully",
        "removed_product": product_to_remove
    }

# endregion

# region MCP Tool Functions - Stores

@tool_error_handler(default_return={"stores": []})
@mcp.tool()
def get_stores() -> Dict[str, Any]:
    """Retrieve all stores."""
    stores = load_json_data("stores.json")
    logging.info("All stores retrieved: %d stores", len(stores))
    return {
        "success": True,
        "stores": stores
    }

@tool_error_handler()
@mcp.tool()
def get_store_by_id(store_id: int) -> Dict[str, Any]:
    """
    Retrieve a store by its ID.

    :param store_id: The unique integer ID of the store to retrieve.
    :return: A dictionary with the result and the store details if found.
    """
    stores = load_json_data("stores.json")
    store = next((store for store in stores if store['id'] == store_id), None)
    if store is None:
        logging.warning("Failed to get store: Store ID %s not found", store_id)
        return {
            "success": False,
            "error": f"Store with ID {store_id} not found"
        }
    logging.info("Store retrieved: ID %s", store_id)
    return {
        "success": True,
        "store": store
    }

@tool_error_handler()
@mcp.tool()
def add_store(name: str, city: str, country: str, address: str) -> Dict[str, Any]:
    """
    Add a new store.

    :param name: The name of the store (required).
    :param city: The city where the store is located (required).
    :param country: The country where the store is located (required).
    :param address: The address of the store (required).
    :return: A dictionary with the result and the new store details.
    """
    stores = load_json_data("stores.json")
    if is_duplicate_store(stores, name, address):
        logging.warning("Duplicate store detected: name='%s', address='%s'", name, address)
        return {"success": False, "error": f"A store with the name '{name}' and address '{address}' already exists."}
    if not name or not isinstance(name, str):
        logging.warning("Failed to add store: Invalid name '%s'", name)
        return {"success": False, "error": "Store name is required and must be a string."}
    if not city or not isinstance(city, str):
        logging.warning("Failed to add store: Invalid city '%s'", city)
        return {"success": False, "error": "Store city is required and must be a string."}
    if not country or not isinstance(country, str):
        logging.warning("Failed to add store: Invalid country '%s'", country)
        return {"success": False, "error": "Store country is required and must be a string."}
    if not address or not isinstance(address, str):
        logging.warning("Failed to add store: Invalid address '%s'", address)
        return {"success": False, "error": "Store address is required and must be a string."}
    next_id = get_next_id(stores)
    new_store = {
        "id": next_id,
        "name": name,
        "city": city,
        "country": country,
        "address": address
    }
    stores.append(new_store)
    save_json_data("stores.json", stores)
    logging.info(f"Store added: {new_store}")
    return {
        "success": True,
        "message": f"Store '{name}' added successfully",
        "store": new_store
    }

# Proper update_store function
@tool_error_handler()
@mcp.tool()
def update_store(store_id: int, name: str = None, city: str = None, country: str = None, address: str = None) -> Dict[str, Any]:
    """
    Update an existing store's details by ID.

    :param store_id: The unique integer ID of the store to update.
    :param name: The new name for the store (optional).
    :param city: The new city for the store (optional).
    :param country: The new country for the store (optional).
    :param address: The new address for the store (optional).
    :return: A dictionary with the result and the updated store details.
    """
    stores = load_json_data("stores.json")
    store = next((store for store in stores if store['id'] == store_id), None)
    if store is None:
        logging.warning("Failed to update store: Store ID %s not found", store_id)
        return {
            "success": False,
            "error": f"Store with ID {store_id} not found"
        }
    # Duplicate detection: if name or address is being updated, check for another store with the same name and address (excluding this store)
    check_name = name if name is not None else None
    check_address = address if address is not None else None
    if check_name is not None or check_address is not None:
        name_to_check = check_name if check_name is not None else store['name']
        address_to_check = check_address if check_address is not None else store['address']
        if is_duplicate_store(stores, name_to_check, address_to_check, exclude_id=store_id):
            logging.warning("Duplicate store detected on update: name='%s', address='%s'", name_to_check, address_to_check)
            return {"success": False, "error": f"A store with the name '{name_to_check}' and address '{address_to_check}' already exists."}
    updated_fields = []
    if name is not None:
        if not name or not isinstance(name, str):
            logging.warning("Failed to update store: Invalid name '%s' for store ID %s", name, store_id)
            return {"success": False, "error": "Store name must be a non-empty string."}
        store['name'] = name
        updated_fields.append('name')
    if city is not None:
        if not city or not isinstance(city, str):
            logging.warning("Failed to update store: Invalid city '%s' for store ID %s", city, store_id)
            return {"success": False, "error": "Store city must be a non-empty string."}
        store['city'] = city
        updated_fields.append('city')
    if country is not None:
        if not country or not isinstance(country, str):
            logging.warning("Failed to update store: Invalid country '%s' for store ID %s", country, store_id)
            return {"success": False, "error": "Store country must be a non-empty string."}
        store['country'] = country
        updated_fields.append('country')
    if address is not None:
        if not address or not isinstance(address, str):
            logging.warning("Failed to update store: Invalid address '%s' for store ID %s", address, store_id)
            return {"success": False, "error": "Store address must be a non-empty string."}
        store['address'] = address
        updated_fields.append('address')
    if not updated_fields:
        logging.warning("Failed to update store: No fields provided for store ID %s", store_id)
        return {
            "success": False,
            "error": "No fields provided to update"
        }
    save_json_data("stores.json", stores)
    logging.info(f"Store updated (ID {store_id}): fields {updated_fields}")
    return {
        "success": True,
        "message": f"Store ID {store_id} updated successfully. Updated fields: {', '.join(updated_fields)}",
        "store": store,
        "updated_fields": updated_fields
    }

@tool_error_handler()
@mcp.tool()
def remove_store(store_id: int) -> Dict[str, Any]:
    """
    Remove a store by its ID.

    :param store_id: The unique integer ID of the store to remove.
    :return: A dictionary with the result and the removed store details.
    """
    stores = load_json_data("stores.json")
    if not stores:
        logging.warning("Failed to remove store: stores.json missing or empty")
        return {
            "success": False,
            "error": "No stores data available (stores.json missing or empty)"
        }
    store_to_remove = None
    for store in stores:
        if store['id'] == store_id:
            store_to_remove = store
            break
    if store_to_remove is None:
        logging.warning("Failed to remove store: Store ID %s not found", store_id)
        return {
            "success": False,
            "error": f"No store found with ID {store_id}"
        }
    stores.remove(store_to_remove)
    save_json_data("stores.json", stores)
    logging.info(f"Store removed: {store_to_remove}")
    return {
        "success": True,
        "message": f"Store '{store_to_remove['name']}' (ID: {store_id}) removed successfully",
        "removed_store": store_to_remove
    }


# endregion

# region MCP Tool Functions - Inventory

@tool_error_handler(default_return={"inventory": []})
@mcp.tool()
def list_inventory_by_store(store_id: int) -> Dict[str, Any]:
    """
    List all inventory records for a given store.

    :param store_id: The unique integer ID of the store to list inventory for.
    :return: A dictionary with the result and the inventory records for the store.
    """
    inventory = load_json_data("inventory.json")
    products = load_json_data("products.json")
    products_lookup = {product['id']: product for product in products}
    store_inventory = [item for item in inventory if item['storeId'] == store_id]
    if not store_inventory:
        logging.warning("No inventory found for store ID %s", store_id)
        return {
            "success": True,
            "message": f"No inventory found for store ID {store_id}",
            "count": 0,
            "inventory": []
        }
    total_quantity = sum(item['quantity'] for item in store_inventory)
    if total_quantity == 0:
        logging.warning("Inventory records exist but total quantity is 0 for store ID %s", store_id)
        return {
            "success": True,
            "message": f"No inventory found for store ID {store_id}",
            "count": 0,
            "inventory": []
        }
    logging.info("Inventory retrieved for store ID %s: %d items", store_id, len(store_inventory))
    enhanced_inventory = []
    for item in store_inventory:
        product_id = item['productId']
        product_details = products_lookup.get(product_id)
        enhanced_item = {
            "id": item['id'],
            "storeId": item['storeId'],
            "productId": product_id,
            "quantity": item['quantity']
        }
        if product_details:
            enhanced_item.update({
                "productName": product_details['name'],
                "productCategory": product_details['category'],
                "productPrice": product_details['price'],
                "productSku": product_details['sku'],
                "productDescription": product_details['description']
            })
        else:
            enhanced_item.update({
                "productName": f"Unknown Product (ID: {product_id})",
                "productCategory": "Unknown",
                "productPrice": 0.0,
                "productSku": "N/A",
                "productDescription": "Product not found in products.json"
            })
        enhanced_inventory.append(enhanced_item)
    return {
        "success": True,
        "count": len(enhanced_inventory),
        "inventory": enhanced_inventory
    }

@tool_error_handler(default_return={"inventory": []})
@mcp.tool()
def list_inventory_by_product(product_id: int) -> Dict[str, Any]:
    """
    List all inventory records for a given product.

    :param product_id: The unique integer ID of the product to list inventory for.
    :return: A dictionary with the result and the inventory records for the product.
    """
    inventory = load_json_data("inventory.json")
    stores = load_json_data("stores.json")
    if not inventory:
        logging.warning("No inventory data available (inventory.json missing or empty)")
        return {
            "success": False,
            "error": "No inventory data available (inventory.json missing or empty)",
            "inventory": []
        }
    if not stores:
        logging.warning("No stores data available (stores.json missing or empty)")
        return {
            "success": False,
            "error": "No stores data available (stores.json missing or empty)",
            "inventory": []
        }
    stores_lookup = {store['id']: store for store in stores}
    product_inventory = [item for item in inventory if item['productId'] == product_id]
    if not product_inventory:
        logging.warning("No inventory records found for product ID %s", product_id)
        return {
            "success": True,
            "message": f"No inventory records found for product ID {product_id}",
            "count": 0,
            "inventory": []
        }
    total_quantity = sum(item['quantity'] for item in product_inventory)
    logging.info("Inventory retrieved for product ID %s: %d records, total quantity: %d", product_id, len(product_inventory), total_quantity)
    enhanced_inventory = []
    for item in product_inventory:
        store_id = item['storeId']
        store_details = stores_lookup.get(store_id)
        enhanced_item = {
            "id": item['id'],
            "storeId": store_id,
            "productId": item['productId'],
            "quantity": item['quantity']
        }
        if store_details:
            enhanced_item.update({
                "storeName": store_details['name'],
                "storeCity": store_details['city'],
                "storeCountry": store_details['country'],
                "storeAddress": store_details['address']
            })
        else:
            enhanced_item.update({
                "storeName": f"Unknown Store (ID: {store_id})",
                "storeCity": "Unknown",
                "storeCountry": "Unknown",
                "storeAddress": "Store not found in stores.json"
            })
        enhanced_inventory.append(enhanced_item)
    return {
        "success": True,
        "count": len(enhanced_inventory),
        "totalQuantity": total_quantity,
        "inventory": enhanced_inventory
    }

@tool_error_handler()
@mcp.tool()
def get_inventory_by_product_and_store(product_id: int, store_id: int) -> Dict[str, Any]:
    """
    Get the inventory record for a specific product at a specific store.

    :param product_id: The unique integer ID of the product.
    :param store_id: The unique integer ID of the store.
    :return: A dictionary with the result and the inventory record if found.
    """
    inventory = load_json_data("inventory.json")
    products = load_json_data("products.json")
    stores = load_json_data("stores.json")
    if not inventory:
        logging.warning("No inventory data available (inventory.json missing or empty)")
        return {
            "success": False,
            "error": "No inventory data available (inventory.json missing or empty)"
        }
    if not products:
        logging.warning("No products data available (products.json missing or empty)")
        return {
            "success": False,
            "error": "No products data available (products.json missing or empty)"
        }
    if not stores:
        logging.warning("No stores data available (stores.json missing or empty)")
        return {
            "success": False,
            "error": "No stores data available (stores.json missing or empty)"
        }
    products_lookup = {product['id']: product for product in products}
    stores_lookup = {store['id']: store for store in stores}
    inventory_item = next((item for item in inventory if item['productId'] == product_id and item['storeId'] == store_id), None)
    if inventory_item is None:
        logging.warning("No inventory record found for product ID %s at store ID %s", product_id, store_id)
        return {
            "success": False,
            "error": f"No inventory record found for product ID {product_id} at store ID {store_id}"
        }
    logging.info("Inventory record retrieved for product ID %s at store ID %s: quantity %d", product_id, store_id, inventory_item['quantity'])
    product_details = products_lookup.get(product_id)
    store_details = stores_lookup.get(store_id)
    response = {
        "success": True,
        "inventory": inventory_item
    }
    if product_details:
        response["product"] = product_details
    else:
        response["product"] = {
            "id": product_id,
            "name": f"Unknown Product (ID: {product_id})",
            "category": "Unknown",
            "price": 0.0,
            "sku": "N/A",
            "description": "Product not found in products.json"
        }
    if store_details:
        response["store"] = store_details
    else:
        response["store"] = {
            "id": store_id,
            "name": f"Unknown Store (ID: {store_id})",
            "city": "Unknown",
            "country": "Unknown",
            "address": "Store not found in stores.json"
        }
    return response

@tool_error_handler(default_return={"inventory": []})
@mcp.tool()
def update_inventory_by_product_and_store(product_id: int, store_id: int, quantity: int) -> Dict[str, Any]:
    """
    Update the quantity for an existing inventory record for a product at a store.

    :param product_id: The unique integer ID of the product.
    :param store_id: The unique integer ID of the store.
    :param quantity: The new quantity to set (must be a non-negative integer).
    :return: A dictionary with the result and the updated inventory record.
    """
    inventory = load_json_data("inventory.json")
    if quantity is None or not isinstance(quantity, int) or quantity < 0:
        logging.warning("Failed to update inventory: Invalid quantity '%s' for product ID %s at store ID %s", quantity, product_id, store_id)
        return {
            "success": False,
            "error": "Quantity is required and must be a non-negative integer.",
            "inventory": []
        }
    if not inventory:
        logging.warning("No inventory data available (inventory.json missing or empty)")
        return {
            "success": False,
            "error": "No inventory data available (inventory.json missing or empty)",
            "inventory": []
        }
    inventory_item = next((item for item in inventory if item['productId'] == product_id and item['storeId'] == store_id), None)
    if inventory_item is None:
        logging.warning("No inventory record found for product ID %s at store ID %s", product_id, store_id)
        return {
            "success": False,
            "error": f"No inventory record found for product ID {product_id} at store ID {store_id}",
            "inventory": []
        }
    inventory_item['quantity'] = quantity
    save_json_data("inventory.json", inventory)
    logging.info("Inventory updated for product ID %s at store ID %s: new quantity %d", product_id, store_id, quantity)
    return {
        "success": True,
        "inventory": inventory_item
    }

@tool_error_handler(default_return={"inventory": []})
@mcp.tool()
def create_inventory_record(product_id: int, store_id: int, quantity: int) -> Dict[str, Any]:
    """
    Create a new inventory record for a product at a store.

    :param product_id: The unique integer ID of the product.
    :param store_id: The unique integer ID of the store.
    :param quantity: The quantity to set for the new inventory record (must be a non-negative integer).
    :return: A dictionary with the result and the new inventory record.
    """
    inventory = load_json_data("inventory.json")
    if quantity is None or not isinstance(quantity, int) or quantity < 0:
        logging.warning("Failed to create inventory: Invalid quantity '%s' for product ID %s at store ID %s", quantity, product_id, store_id)
        return {
            "success": False,
            "error": "Quantity is required and must be a non-negative integer.",
            "inventory": []
        }
    if not isinstance(product_id, int) or not isinstance(store_id, int):
        logging.warning("Failed to create inventory: Invalid product_id or store_id")
        return {
            "success": False,
            "error": "Product ID and Store ID must be integers.",
            "inventory": []
        }
    # Check for duplicate
    existing = next((item for item in inventory if item['productId'] == product_id and item['storeId'] == store_id), None)
    if existing:
        logging.warning("Inventory record already exists for product ID %s at store ID %s", product_id, store_id)
        return {
            "success": False,
            "error": f"Inventory record already exists for product ID {product_id} at store ID {store_id}",
            "inventory": []
        }
    # Generate new ID
    new_id = 1
    if inventory:
        new_id = max(item['id'] for item in inventory) + 1
    new_record = {
        "id": new_id,
        "productId": product_id,
        "storeId": store_id,
        "quantity": quantity
    }
    inventory.append(new_record)
    save_json_data("inventory.json", inventory)
    logging.info("Created new inventory record: %s", new_record)
    return {
        "success": True,
        "message": f"Inventory record created for product ID {product_id} at store ID {store_id}",
        "inventory": new_record
    }
# endregion

# region Custom routes

@app.route("/")
async def root(request) -> PlainTextResponse:
    """Root endpoint with custom message"""
    return PlainTextResponse("The Zava Inventory 📦 MCP Server 🧠 is running")

# endregion

# region MCP Server Startup

if __name__ == "__main__":
    logging.info("\u2139\ufe0f  Visit http://localhost:3000 to access the Zava Inventory 📦 MCP Server 🧠.")
    if os.getenv("RUNNING_IN_PRODUCTION") == "1":
        # Production mode with multiple workers for better performance
        uvicorn.run(
            "server:app",  # Pass as import string
            host="0.0.0.0",
            port=3000,
            workers=(multiprocessing.cpu_count() * 2) + 1,
            timeout_keep_alive=300  # Increased for SSE connections
        )
    else:
        # Development mode with a single worker for easier debugging
        uvicorn.run("server:app", host="0.0.0.0", port=3000, reload=True)

# endregion
