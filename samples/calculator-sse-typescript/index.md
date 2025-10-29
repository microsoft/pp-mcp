# 🧮 Calculator (SSE Version) - TypeScript

This is a demo Node.js + TypeScript MCP SDK using [Model Context Protocol SDK](https://www.npmjs.com/package/@modelcontextprotocol/sdk). It exposes simple calculation tools like BMI and addition through MCP, and supports real-time responses via Server-Sent Events (SSE).
Explore the MCP architecture and best practices using the [MCP Architecture](https://modelcontextprotocol.io/docs/concepts/architecture) and SSE transport.

This MCP Server has multiple tools available:

- `calculate-bmi` | Calculates your BMI based on weight in kg and height in m
- `calculate-sum` | Calculated the sum of two input numbers (a an b)

## ⚙️ Prerequisites

- Visual Studio Code ([link](https://code.visualstudio.com/download))
- Node v22 (ideally installed via [nvm for Windows](https://github.com/coreybutler/nvm-windows))

## 🚀 Minimal path to awesome

1. Clone this repository by running `git clone https://github.com/microsoft/copilot-studio-mcp/` in your terminal
1. Open Visual Studio Code on the subfolder `samples/calculator-sse-typescript`
1. Open the terminal and navigate to the same folder
1. Run `npm install`
1. Run `npm run build && npm run start`

The app will run at <http://localhost:3001> (unless configured otherwise).

## 👨‍💻 Use the Employee Vacations MCP Server in Visual Studio Code / GitHub Copilot

1. Open the **Command Palette** (`Ctrl+Shift+P` or `Cmd+Shift+P`).
2. Type **"Add MCP Server"** and select it.
3. Update `.vscode/mcp.json` with the following:

```json
{
    "servers": {
        "my-mcp-server": {
            "type": "sse",
            "url": "http://localhost:3001/sse"
        }
    }
}
```

<p align="left"> <img src="https://github.com/user-attachments/assets/5109619f-071e-41f9-aa92-f37a767306ac" width="400"/> </p>

**Result in Github Copilot Agent**
<p align="left"> <img src="https://github.com/user-attachments/assets/e4c0977c-a388-42cb-8f98-9f6cb84d3978" width="400"/> </p>
The server appears and is connected successfully.

## 👨‍💻 Use the Employee Vacations MCP Server in Microsoft Copilot Studio

For details on integrating Model Context Protocol (MCP) tools into Microsoft Copilot Studio using custom connectors, check out the official Microsoft documentation: 🔗 [Extend Copilot actions using MCP in Copilot Studio](https://learn.microsoft.com/microsoft-copilot-studio/agent-extend-action-mcp)

### MCP Custom connector Copilot Studio Integration

It shows how to set up the MCP Tools for actions to work with custom connectors in **Copilot Studio**.

---

### Swagger Specification

```yaml
swagger: '2.0'
info:
  title: MCPCalculatorDemo
  description: Calculate BMI and Calculate sum using MCP SSE server
  version: '1.0'
host: calculatormcp-dummyurl.azurewebsites.net
basePath: /
schemes:
  - https
definitions:
  QueryResponse:
    type: object
    properties:
      jsonrpc:
        type: string
      id:
        type: string
      method:
        type: string
      params:
        type: object
      result:
        type: object
      error:
        type: object
paths:
  /sse:
    get:
      summary: MCP Server Actions for calculating BMI and sum
      parameters:
        - in: query
          name: sessionId
          type: string
          required: false
      produces:
        - application/json
      responses:
        '200':
          description: Immediate Response
          schema:
            $ref: '#/definitions/QueryResponse'
        '201':
          description: Created and will follow callback
      operationId: CalculatorDemo
      tags:
        - Agentic
        - McpSse
securityDefinitions: {}
security: []

```
![image](https://github.com/user-attachments/assets/7727d5b9-f4c8-44bd-8293-aa4bd7957133)

### Using MCP Server Action in Copilot Studio

#### Steps to Access the MCP Server Action

1. **Open Copilot Studio**  
   Navigate to your [Copilot Studio](https://copilotstudio.microsoft.com) workspace.

2. **Go to Actions**  
   Click on the **Action** menu in the left sidebar.

3. **Select "Custom connector"**  
   Under the Action menu, choose **Custom connector**.

4. **Locate the MCP Server Action**  
   The system will automatically display available tools. Select the **MCP Server Action** from the list.

   ![Custom Connector Selection](https://github.com/user-attachments/assets/ee74ce02-a1f1-4835-a0a9-9b26ab0f7367)

5. **MCP Server Action Preview**  
   You will be able to view the details of the selected MCP Server Action as shown below:

   ![MCP Server Action](https://github.com/user-attachments/assets/2992d2b3-af6e-4d61-a0d5-96ae3ba60fe1)

## 📌 Considerations

- ✅ The `/sse` endpoint should **return the full URI** (including protocol and host) when initializing the **MCP transport**. This ensures compatibility when deploying across environments (e.g., localhost vs Azure). It establishes a live connection for streaming MCP interactions.

  **Example:**

  ```ts
  const protocol = req.protocol;
  const host = req.get('host');
  const fullUri = `${protocol}://${host}/mcp`;

### 🔄 Return / Server-Sent Events (SSE) with Full URI

Ensure your custom connector supports **SSE (Server-Sent Events)** and returns the **full URI** as shown:
![Return SSE with Full URI](https://github.com/user-attachments/assets/1da61513-ea89-4c48-8bf8-096a26ed3e69)

### 🏷️ Add Tags to Your Custom Connector
```yaml
tags:
  - Agentic
  - McpSse
```
### ⚠️ Naming Guidance
Do **not** use `"InvokeMCP"` as your `operationId`.  
Choose a more specific and descriptive name to reflect the purpose of the action and avoid conflicts.

## ☁️ Deploy to Azure (Optional)

Create an Azure App Service (Node.js 18+)
Set the startup command (if needed):

```bash
npm run build && npm run start
```

### SSE Deployment Update

The SSE deployment to Azure with the **West US 2** region using the **Basic plan** was successful and tested without issues.  


## 🛠️ Troubleshooting

### ✅ How to Check if Your SSE Server is Running Properly

Follow these steps to verify that your SSE (Server-Sent Events) server is functioning correctly:

---

### 🔍 Step 1: Browse the SSE Endpoint

- Open your browser and navigate to:  
  - `http://localhost:3000/sse` (if running locally), or  
  - Your deployed **Azure URL**.

- Open **Developer Tools** → **Network** tab.

- Look for an **EventStream** connection.

- Under the `Event` section, you should see:
  - **Endpoint**: SSE endpoint
  - **Data**: Your Full URI endpoint

![SSE Browser Network Trace](https://github.com/user-attachments/assets/680c6f25-ebba-4494-83d2-2244ad3fb98e)

---

### 🧪 Step 2: Test SSE Endpoint via Postman

1. Copy the **Full URI** (from the EventStream `data`).
2. Use Postman to send a `POST` request to that URI.

**Example URL**:
```
http://calculatormcp-dummyurl.azurewebsites.net/mcpfy/v1/calculatordemo?sessionId=620c84e1-81e2-484d-8737-a7fbc93165b1
```

**Example Request Payload**:
```json
{
  "jsonrpc": "2.0",
  "id": "2",
  "method": "tools/call",
  "params": {
    "name": "calculate-bmi",
    "arguments": {
      "weightKg": 180,
      "heightM": 1.8
    }
  }
}
```

If successful, you'll receive a response with a `"message"` confirming that the server is working correctly.

---

### 🖼️ Sample Screenshots

#### Browser Network Event Trace:
![Event Trace](https://github.com/user-attachments/assets/13ee9c86-093d-41f9-8096-782f0bc192e3)

#### Postman Response:
![Postman Output](https://github.com/user-attachments/assets/efc412ed-28f7-44cd-ba89-d92d3bae8418)

Alternatively, you can use MCP Inspector to test, https://github.com/modelcontextprotocol/inspector

## Disclaimer

This is an **unsupported**, **experimental**, and **not an official Microsoft product**. It is provided **"as is"**, without support and without any warranties, whether express or implied. This includes, but is not limited to, warranties of **merchantability**, **fitness for a particular purpose**, and **non-infringement**.

In no event shall the authors or copyright holders be liable for any **claims**, **damages**, or other **liabilities**, whether in contract, tort, or otherwise, arising from, out of, or in connection with the Software or the use or other dealings in the Software.

> ⚠️ **Important Note:**  
> This is a sample demo **custom MCP server** created for **demonstration purposes**. It is deployed into **Microsoft Azure** and intended solely for **integration with Copilot Studio** during prototyping or sample scenarios.  
> This component is **not part of any official Microsoft product** and is **not available for production use**.

![🧮 Calculator (SSE Version) - TypeScript](https://m365-visitor-stats.azurewebsites.net/?resource=https://github.com/microsoft/copilot-studio-mcp/tree/main/samples/calculator-sse-typescript&dot=)


