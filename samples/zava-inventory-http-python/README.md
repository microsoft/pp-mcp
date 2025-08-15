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
- Global coverage across 19 cities

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

## 🚀 Quick Start

### 1. Prerequisites

Before getting started, ensure you have the following installed on your system:

- **Python 3.8+**: The MCP server requires Python 3.8 or higher
  - Download from [python.org](https://www.python.org/downloads/)
  - Verify installation: `python --version`

- **Git**: For cloning the repository
  - Download from [git-scm.com](https://git-scm.com/)
  - Verify installation: `git --version`

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

### 3. API Key Authentication

To enable API key authentication, set the `MCP_API_KEY` environment variable before running the server.

**Important:** Be sure to replace `replace-with-api-key` with your actual API key value. You will use this same API key in Microsoft Copilot Studio to authenticate requests to your MCP server.

**On Windows (PowerShell):**
```
$env:MCP_API_KEY = "replace-with-api-key"
python src/server.py
```

**On Windows (Command Prompt):**
```
set MCP_API_KEY=replace-with-api-key
python src/server.py
```

### 4. Start the Server

To start the server, run the following command in your terminal:

```bash
python src/server.py
```

### 5. Setup a dev tunnel in Visual Studio Code by adding a port forward in the ports section

To expose your MCP server to the internet for Copilot Studio integration, you need to set up a dev tunnel in Visual Studio Code. This allows external services to access your local server securely.

**Steps to set up a dev tunnel and port forward:**

1. Open the Ports view (usually found in the bottom panel or via the Command Palette: `View: Open Ports View`).
1. Find the port your MCP server is running on (default is usually 8000 or 5000).
1. Right-click the port and select "Forward Port".
1. Choose "Dev Tunnel" as the forwarding option.
1. When prompted, set the tunnel visibility to **public** so Copilot Studio can access your server.
1. Copy the generated dev tunnel URL and paste this in the [schema.yaml](./schema.yaml) on the place of `{ replace-with-dev-tunnel-URL }`.

**Note:** Dev tunnels require you to be signed in with a Microsoft account in Visual Studio Code. Make sure you are signed in and have the Dev Tunnels extension installed if prompted.

### 6. Create a custom MCP connector in Microsoft Copilot Studio

To add your MCP server to a Copilot Studio agent, follow these steps:

1. Go to Microsoft Copilot Studio and select your agent.
1. Navigate to the Tools page for your agent.
1. Select "Add a tool" and then "New tool".
1. Choose "Custom connector" (this will open Power Apps).
1. Select "New custom connector" and then "Import OpenAPI file".
1. Select the [schema.yaml](./schema.yaml) file.
1. Complete the import and setup in Power Apps.

For more details, see the official documentation: [Add an existing MCP server to your agent](https://learn.microsoft.com/microsoft-copilot-studio/mcp-add-existing-server-to-agent)

### 7. Add Model Context Protocol (MCP) tools to your agent

To add an existing MCP connector to your agent in Microsoft Copilot Studio, follow these steps:

1. Select Agents in the left navigation.
1. Select your agent from the list.
1. Go to the Tools page for your agent.
1. Select Add a tool.
1. Select Model Context Protocol. A list of MCP connectors is displayed.
1. Select the Zava Inventory MCP from the list.
1. Authorize the connection, entering any information that is needed.
1. When you're done, select Add to agent to proceed.

Once added, the MCP server tools will appear under Tools for your agent.

### 8. Test the MCP server in your agent

After you have added the Zava Inventory MCP connector to your agent, you can publish and test the integration and authenticate as an end user in Copilot Studio.

**How to test and authenticate as an end user in Copilot Studio:**

1. Publish your agent by selecting **Publish** in the top right corner of Copilot Studio.
1. Open the integrated **Test** panel and start a conversation with your agent. For example, enter:
   
      `Get Stores`
1. If your agent needs to access the MCP connector, Copilot Studio will prompt you to open the connection manager.
1. In the connection manager, connect to the Zava Inventory MCP server by providing the required authentication (such as the API key you used [here](#3-api-key-authentication)).
1. After connecting, return to the Test panel and retry your request.
1. Once authenticated, you will receive the actual list of stores from the Zava Inventory MCP server.

For more details, see the official documentation: [Configure user authentication for actions](https://learn.microsoft.com/microsoft-copilot-studio/configure-enduser-authentication).

## 📁 Project Structure

```
zava-inventory-mcp/
├── src/
│   ├── server.py          # Main MCP server implementation
│   ├── helpers.py         # Shared business logic, duplicate detection, and data handling utilities
│   ├── middleware.py      # Custom authentication middleware
│   ├── requirements.txt   # Python dependencies
├── data/
│   ├── products.json      # Product catalog with sample data
│   ├── stores.json        # Store locations sample data
│   └── inventory.json     # Inventory tracking across all stores
├── schema.yaml            # Schema definition for the custom connector for the Zava Inventory MCP Server
└── README.md              # Project documentation (this file)
```

## 🌍 Sample Data

The system comes pre-loaded with sample data:

| Data Type           | Count | File Path              | Fields                                         | Notes |
|---------------------|-------|------------------------|------------------------------------------------|-------|
| Products            | 11    | `data/products.json`   | `id`, `name`, `category`, `price`, `sku`, `description` | Categories: electronics, furniture, sports equipment, kitchenware, and more |
| Stores              | 19    | `data/stores.json`     | `id`, `name`, `city`, `country`, `address`     | Located in major cities worldwide |
| Inventory Records   | 84    | `data/inventory.json`  | `id`, `productId`, `storeId`, `quantity`       | Realistic distribution of products across stores |

## 📈 Use Cases

- **Retail Management**: Complete inventory management for retail chains
- **E-commerce**: Product and inventory tracking for online stores
- **Supply Chain**: Monitor product distribution across locations
- **Analytics**: Generate reports on product performance by location
- **Customer Service**: Check product availability for customers

---

**Zava Inventory MCP Server** - Powering global retail inventory management 🌟
