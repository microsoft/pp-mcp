import os
import json
import multiprocessing
import uvicorn
from mcp.server.fastmcp import FastMCP
from starlette.responses import PlainTextResponse
from typing import Optional

# Initialize FastMCP
mcp = FastMCP("docker-mcp", stateless_http=True)
app = mcp.streamable_http_app()

# Helper functions
def get_data_file_path(filename: str) -> str:
    """Get the absolute path to a data file"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(os.path.dirname(current_dir), "data", filename)

def load_json_data(filename: str) -> list:
    """Load data from a JSON file, return empty list if file not found"""
    try:
        with open(get_data_file_path(filename), 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_json_data(filename: str, data: list) -> None:
    """Save data to a JSON file"""
    with open(get_data_file_path(filename), 'w') as file:
        json.dump(data, file, indent=2)

def generate_sku(product_name: str, product_id: int) -> str:
    """Generate SKU based on product name and ID"""
    # Extract first letters of important words (excluding common words)
    common_words = {'and', 'the', 'a', 'an', 'with', 'for', 'of', 'in', 'on', 'at', 'to', 'from'}
    words = [word for word in product_name.lower().split() if word not in common_words]
    
    # Take first letter of each word, up to 3 letters
    abbreviation = ''.join([word[0].upper() for word in words[:3]])
    
    # If we have less than 2 letters, use first 2-3 chars of first word
    if len(abbreviation) < 2:
        abbreviation = product_name.replace(' ', '')[:3].upper()
    
    # Format: ABC-XXX where XXX is zero-padded ID
    return f"{abbreviation}-{product_id:03d}"

# Add custom root route
@app.route("/")
async def root(request):
    """Root endpoint with custom message"""
    return PlainTextResponse("The Zava Inventory MCP Server is running")

# ======================
# MCP Tools - Products Management  
# ======================

@mcp.tool()
def get_products():
    """Get all products"""
    try:
        products = load_json_data("products.json")
        return {
            "success": True,
            "count": len(products),
            "products": products
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"An error occurred: {str(e)}",
            "products": []
        }

@mcp.tool()
def get_product_by_id(product_id: int):
    """Get a product by ID"""
    try:
        products = load_json_data("products.json")
        
        # Find the product by ID
        product = next((product for product in products if product['id'] == product_id), None)

        if product is None:
            return {
                "success": False,
                "error": f"Product with ID {product_id} not found"
            }

        return {
            "success": True,
            "product": product
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"An error occurred: {str(e)}"
        }

@mcp.tool()
def add_product(name: str, category: str, price: float, description: str = ""):
    """Add a new product with auto-generated SKU"""
    try:
        products = load_json_data("products.json")
        
        # Find the next available ID
        next_id = max([product.get('id', 0) for product in products], default=0) + 1
        
        # Generate SKU using helper function
        sku = generate_sku(name, next_id)
        
        # Create new product
        new_product = {
            "id": next_id,
            "name": name,
            "category": category,
            "price": price,
            "sku": sku,
            "description": description
        }
        
        # Add to products list and save
        products.append(new_product)
        save_json_data("products.json", products)
        
        return {
            "success": True,
            "message": f"Product '{name}' added successfully with SKU {sku}",
            "product": new_product
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"An error occurred: {str(e)}"
        }

@mcp.tool()
def update_product(product_id: int, name: str = None, category: str = None, price: float = None, description: str = None):
    """Update an existing product"""
    try:
        products = load_json_data("products.json")
        
        # Find the product by ID
        product = next((product for product in products if product['id'] == product_id), None)

        if product is None:
            return {
                "success": False,
                "error": f"Product with ID {product_id} not found"
            }

        # Track what fields were updated
        updated_fields = []

        # Update only the fields that were provided (not None)
        if name is not None:
            product['name'] = name
            updated_fields.append('name')
        
        if category is not None:
            product['category'] = category
            updated_fields.append('category')
            
        if price is not None:
            product['price'] = price
            updated_fields.append('price')
            
        if description is not None:
            product['description'] = description
            updated_fields.append('description')

        # Check if any fields were actually updated
        if not updated_fields:
            return {
                "success": False,
                "error": "No fields provided to update"
            }

        # Save updated products
        save_json_data("products.json", products)

        return {
            "success": True,
            "message": f"Product ID {product_id} updated successfully. Updated fields: {', '.join(updated_fields)}",
            "product": product,
            "updated_fields": updated_fields
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"An error occurred: {str(e)}"
        }

@mcp.tool()
def remove_product(product_id: int):
    """Remove a product by ID"""
    try:
        products = load_json_data("products.json")
        
        # Find the product to remove
        product_to_remove = None
        for product in products:
            if product['id'] == product_id:
                product_to_remove = product
                break
        
        if product_to_remove is None:
            return {
                "success": False,
                "error": f"Product with ID {product_id} not found"
            }
        
        # Remove the product
        products.remove(product_to_remove)
        
        # Save updated products
        save_json_data("products.json", products)
        
        return {
            "success": True,
            "message": f"Product '{product_to_remove['name']}' (ID: {product_id}) removed successfully",
            "removed_product": product_to_remove
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"An error occurred: {str(e)}"
        }

# ======================
# MCP Tools - Stores Management
# ======================

@mcp.tool()
def get_stores():
    """Get a list of all stores"""
    try:
        stores = load_json_data("stores.json")
        return {
            "success": True,
            "stores": stores
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"An error occurred: {str(e)}"
        }
    
@mcp.tool()
def get_store_by_id(store_id: int):
    """Get a store by ID"""
    try:
        stores = load_json_data("stores.json")
        
        # Find the store by ID
        store = next((store for store in stores if store['id'] == store_id), None)

        if store is None:
            return {
                "success": False,
                "error": f"Store with ID {store_id} not found"
            }

        return {
            "success": True,
            "store": store
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"An error occurred: {str(e)}"
        }

@mcp.tool()
def add_store(name: str, city: str, country: str, address: str):
    """Add a new store"""
    try:
        # Get the path to the stores.json file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        stores_file = os.path.join(os.path.dirname(current_dir), "data", "stores.json")

        # Read existing stores
        try:
            with open(stores_file, 'r') as file:
                stores = json.load(file)
        except FileNotFoundError:
            stores = []

        # Find the next available ID
        if stores:
            next_id = max(store['id'] for store in stores) + 1
        else:
            next_id = 1

        # Create new store
        new_store = {
            "id": next_id,
            "name": name,
            "city": city,
            "country": country,
            "address": address
        }

        # Add to stores list
        stores.append(new_store)

        # Write back to file
        with open(stores_file, 'w') as file:
            json.dump(stores, file, indent=2)

        return {
            "success": True,
            "message": f"Store '{name}' added successfully",
            "store": new_store
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"An error occurred: {str(e)}"
        }

@mcp.tool()
def remove_store(store_id: int):
    """Remove a store by ID"""
    try:
        # Get the path to the stores.json file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        stores_file = os.path.join(os.path.dirname(current_dir), "data", "stores.json")

        # Read existing stores
        try:
            with open(stores_file, 'r') as file:
                stores = json.load(file)
        except FileNotFoundError:
            return {
                "success": False,
                "error": "Stores file not found"
            }

        # Find the store to remove
        store_to_remove = None
        for store in stores:
            if store['id'] == store_id:
                store_to_remove = store
                break

        if store_to_remove is None:
            return {
                "success": False,
                "error": f"Store with ID {store_id} not found"
            }

        # Remove the store
        stores.remove(store_to_remove)

        # Write back to file
        with open(stores_file, 'w') as file:
            json.dump(stores, file, indent=2)

        return {
            "success": True,
            "message": f"Store '{store_to_remove['name']}' (ID: {store_id}) removed successfully",
            "removed_store": store_to_remove
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"An error occurred: {str(e)}"
        }

# ======================
# MCP Tools - Inventory Management
# ======================

@mcp.tool()
def list_inventory_by_store(store_id: int):
    """Get inventory for a specific store by store ID"""
    try:
        inventory = load_json_data("inventory.json")
        products = load_json_data("products.json")
        
        # Create a lookup dictionary for products
        products_lookup = {product['id']: product for product in products}
        
        # Filter inventory by store ID
        store_inventory = [item for item in inventory if item['storeId'] == store_id]
        
        if not store_inventory:
            return {
                "success": True,
                "message": f"No inventory found for store ID {store_id}",
                "count": 0,
                "inventory": []
            }
        
        # Enhance inventory items with product details
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
    except Exception as e:
        return {
            "success": False,
            "error": f"An error occurred: {str(e)}",
            "inventory": []
        }

@mcp.tool()
def list_inventory_by_product(product_id: int):
    """Get inventory for a specific product by product ID across all stores"""
    try:
        # Get the path to the inventory.json and stores.json files
        current_dir = os.path.dirname(os.path.abspath(__file__))
        inventory_file = os.path.join(os.path.dirname(current_dir), "data", "inventory.json")
        stores_file = os.path.join(os.path.dirname(current_dir), "data", "stores.json")
        
        # Read inventory data
        try:
            with open(inventory_file, 'r') as file:
                inventory = json.load(file)
        except FileNotFoundError:
            return {
                "success": False,
                "error": "Inventory file not found",
                "inventory": []
            }
        
        # Read stores data
        try:
            with open(stores_file, 'r') as file:
                stores = json.load(file)
        except FileNotFoundError:
            return {
                "success": False,
                "error": "Stores file not found",
                "inventory": []
            }
        
        # Create a lookup dictionary for stores
        stores_lookup = {store['id']: store for store in stores}
        
        # Filter inventory by product ID
        product_inventory = [item for item in inventory if item['productId'] == product_id]
        
        if not product_inventory:
            return {
                "success": True,
                "message": f"No inventory found for product ID {product_id}",
                "count": 0,
                "inventory": []
            }
        
        # Enhance inventory items with store details
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
        
        # Calculate total quantity across all stores
        total_quantity = sum(item['quantity'] for item in enhanced_inventory)
        
        return {
            "success": True,
            "count": len(enhanced_inventory),
            "totalQuantity": total_quantity,
            "inventory": enhanced_inventory
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"An error occurred: {str(e)}",
            "inventory": []
        }

@mcp.tool()
def get_inventory_by_product_and_store(product_id: int, store_id: int):
    """Get inventory for a specific product and store"""
    try:
        # Get the path to all required files
        current_dir = os.path.dirname(os.path.abspath(__file__))
        inventory_file = os.path.join(os.path.dirname(current_dir), "data", "inventory.json")
        products_file = os.path.join(os.path.dirname(current_dir), "data", "products.json")
        stores_file = os.path.join(os.path.dirname(current_dir), "data", "stores.json")

        # Read inventory data
        try:
            with open(inventory_file, 'r') as file:
                inventory = json.load(file)
        except FileNotFoundError:
            return {
                "success": False,
                "error": "Inventory file not found"
            }

        # Read products data
        try:
            with open(products_file, 'r') as file:
                products = json.load(file)
        except FileNotFoundError:
            return {
                "success": False,
                "error": "Products file not found"
            }

        # Read stores data
        try:
            with open(stores_file, 'r') as file:
                stores = json.load(file)
        except FileNotFoundError:
            return {
                "success": False,
                "error": "Stores file not found"
            }

        # Create lookup dictionaries
        products_lookup = {product['id']: product for product in products}
        stores_lookup = {store['id']: store for store in stores}

        # Find the inventory item by product ID and store ID
        inventory_item = next((item for item in inventory if item['productId'] == product_id and item['storeId'] == store_id), None)

        if inventory_item is None:
            return {
                "success": False,
                "error": f"No inventory found for product ID {product_id} and store ID {store_id}"
            }

        # Get product and store details
        product_details = products_lookup.get(product_id)
        store_details = stores_lookup.get(store_id)

        # Build comprehensive response
        response = {
            "success": True,
            "inventory": {
                "id": inventory_item['id'],
                "quantity": inventory_item['quantity']
            }
        }

        # Add product details
        if product_details:
            response["product"] = {
                "id": product_details['id'],
                "name": product_details['name'],
                "category": product_details['category'],
                "price": product_details['price'],
                "sku": product_details['sku'],
                "description": product_details['description']
            }
        else:
            response["product"] = {
                "id": product_id,
                "name": f"Unknown Product (ID: {product_id})",
                "category": "Unknown",
                "price": 0.0,
                "sku": "N/A",
                "description": "Product not found in products.json"
            }

        # Add store details
        if store_details:
            response["store"] = {
                "id": store_details['id'],
                "name": store_details['name'],
                "city": store_details['city'],
                "country": store_details['country'],
                "address": store_details['address']
            }
        else:
            response["store"] = {
                "id": store_id,
                "name": f"Unknown Store (ID: {store_id})",
                "city": "Unknown",
                "country": "Unknown",
                "address": "Store not found in stores.json"
            }

        return response

    except Exception as e:
        return {
            "success": False,
            "error": f"An error occurred: {str(e)}"
        }

@mcp.tool()
def update_inventory_by_product_and_store(product_id: int, store_id: int, quantity: int):
    """Update inventory for a specific product and store"""
    try:
        # Get the path to the inventory.json file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        inventory_file = os.path.join(os.path.dirname(current_dir), "data", "inventory.json")

        # Read inventory data
        try:
            with open(inventory_file, 'r') as file:
                inventory = json.load(file)
        except FileNotFoundError:
            return {
                "success": False,
                "error": "Inventory file not found",
                "inventory": []
            }

        # Find the inventory item by product ID and store ID
        inventory_item = next((item for item in inventory if item['productId'] == product_id and item['storeId'] == store_id), None)

        if inventory_item is None:
            return {
                "success": False,
                "error": f"No inventory found for product ID {product_id} and store ID {store_id}",
                "inventory": []
            }

        # Update the inventory quantity
        inventory_item['quantity'] = quantity

        # Write the updated inventory back to the file
        with open(inventory_file, 'w') as file:
            json.dump(inventory, file)

        return {
            "success": True,
            "inventory": inventory_item
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"An error occurred: {str(e)}",
            "inventory": []
        }

if __name__ == "__main__":
    if os.getenv("RUNNING_IN_PRODUCTION"):
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
