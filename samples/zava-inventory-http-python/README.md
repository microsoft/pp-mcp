# Zava Inventory MCP Server

A comprehensive Model Context Protocol (MCP) server for managing inventory across multiple store locations. This server provides a complete suite of tools for managing products, stores, and inventory data for the fictional retail company "Zava".

## 🚀 Features

- **Product Management**: Add, remove, and retrieve product information
- **Store Management**: Manage store locations worldwide
- **Inventory Tracking**: Track product quantities across all store locations
- **Real-time Data**: JSON-based data storage with immediate updates
- **Global Coverage**: Support for international store locations

## 📊 Data Structure

The system manages three main data entities:

### Products (`data/products.json`)
- Product information including name, category, price, SKU, and description
- No stock quantities (handled separately in inventory)

### Stores (`data/stores.json`)
- Store locations with name, city, country, and address
- Global coverage across 10 major cities

### Inventory (`data/inventory.json`)
- Links products to stores with current quantities
- Tracks last updated timestamps
- Supports detailed inventory management

## 🛠️ Available Tools

### Product Management Tools

#### `get_products()`
Retrieves all products from the products.json file.
- **Returns**: List of all products with details
- **Use case**: Browse product catalog

#### `get_product_by_id(product_id: int)`
Retrieves a specific product by its ID.
- **Parameters**: `product_id` - The ID of the product to retrieve
- **Returns**: Product details or error if not found
- **Use case**: Get detailed information about a specific product

#### `add_product(name: str, category: str, price: float, description: str)`
Adds a new product to the inventory system with auto-generated SKU.
- **Parameters**:
  - `name` - Product name
  - `category` - Product category
  - `price` - Product price
  - `description` - Product description (optional)
- **Returns**: Success confirmation with new product details including auto-generated SKU
- **Use case**: Add new products to the catalog

#### `remove_product(product_id: int)`
Removes a product from the system.
- **Parameters**: `product_id` - The ID of the product to remove
- **Returns**: Success confirmation with removed product details
- **Use case**: Discontinue products

### Store Management Tools

#### `get_stores()`
Retrieves all store locations.
- **Returns**: List of all stores with location details
- **Use case**: View all store locations

#### `get_store_by_id(store_id: int)`
Retrieves a specific store by its ID.
- **Parameters**: `store_id` - The ID of the store to retrieve
- **Returns**: Store details or error if not found
- **Use case**: Get information about a specific store

#### `add_store(name: str, city: str, country: str, address: str)`
Adds a new store location.
- **Parameters**:
  - `name` - Store name (e.g., "Zava Tokyo")
  - `city` - City name
  - `country` - Country name
  - `address` - Full address
- **Returns**: Success confirmation with new store details
- **Use case**: Open new store locations

#### `remove_store(store_id: int)`
Removes a store from the system.
- **Parameters**: `store_id` - The ID of the store to remove
- **Returns**: Success confirmation with removed store details
- **Use case**: Close store locations

### Inventory Management Tools

#### `list_inventory_by_store(store_id: int)`
Gets inventory for a specific store with resolved product names and details.
- **Parameters**: `store_id` - The ID of the store
- **Returns**: List of inventory items with complete product information
- **Use case**: Check what products are available at a specific store

#### `list_inventory_by_product(product_id: int)`
Gets inventory for a specific product across all stores with resolved store names and details.
- **Parameters**: `product_id` - The ID of the product
- **Returns**: List of inventory items with complete store information and total quantity
- **Use case**: Check which stores have a specific product in stock

#### `get_inventory_by_product_and_store(product_id: int, store_id: int)`
Gets inventory for a specific product at a specific store with complete details.
- **Parameters**:
  - `product_id` - The ID of the product
  - `store_id` - The ID of the store
- **Returns**: Complete inventory, product, and store information
- **Use case**: Check exact quantity of a product at a specific store

#### `update_inventory_by_product_and_store(product_id: int, store_id: int, quantity: int)`
Updates inventory quantity for a specific product at a specific store.
- **Parameters**:
  - `product_id` - The ID of the product
  - `store_id` - The ID of the store
  - `quantity` - New quantity value
- **Returns**: Success confirmation with updated inventory
- **Use case**: Update stock levels after sales or restocking

##  Quick Start

### 1. Prerequisites

Before getting started, ensure you have the following installed on your system:

- **Python 3.8+**: The MCP server requires Python 3.8 or higher
  - Download from [python.org](https://www.python.org/downloads/)
  - Verify installation: `python --version`

- **Git**: For cloning the repository
  - Download from [git-scm.com](https://git-scm.com/)
  - Verify installation: `git --version`

- **Optional - Docker**: For containerized deployment
  - Download from [docker.com](https://www.docker.com/get-started)
  - Verify installation: `docker --version`

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/microsoft/aitour26-WRK532-building-agents-with-copilot-studio.git
cd aitour26-WRK532-building-agents-with-copilot-studio/src/zava-inventory-mcp

# Create virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r src/requirements.txt
```

### 3. Start the Server
```bash
python src/server.py
```

## 📁 Project Structure

```
zava-inventory-mcp/
├── src/
│   ├── server.py          # Main MCP server implementation
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile         # Docker configuration for containerization
├── data/
│   ├── products.json      # Product catalog with sample data
│   ├── stores.json        # Store locations worldwide
│   └── inventory.json     # Inventory tracking across all stores
├── .dockerignore          # Docker ignore patterns
├── azure.yaml             # Azure Developer CLI configuration
├── docker-compose.yml     # Docker Compose for local development
└── README.md              # Project documentation (this file)
```

## 🌍 Sample Data

The system comes pre-loaded with:
- **10 Products**: Electronics, furniture, sports equipment, etc.
- **10 Stores**: Located in major cities worldwide (New York, London, Tokyo, Paris, Sydney, Rio de Janeiro, Singapore, Berlin, Toronto, Seoul)
- **34 Inventory Records**: Realistic distribution of products across stores

##  Docker Support

Build and run with Docker Compose. The server will be available at http://localhost:3000.

```bash
docker-compose up --build
```

## 📈 Use Cases

- **Retail Management**: Complete inventory management for retail chains
- **E-commerce**: Product and inventory tracking for online stores
- **Supply Chain**: Monitor product distribution across locations
- **Analytics**: Generate reports on product performance by location
- **Customer Service**: Check product availability for customers

---

**Zava Inventory MCP Server** - Powering global retail inventory management 🌟
