## **Introduction to Transport , Protocols , Rest , Json_RPC and MCP (Model Context Protocol) - Step-by-Step Guide**

### **Section 1: Introduction to Communication Between Machines**

**1.1 What is Communication in Computing?**

- When two machines talk to each other, they need a way to send and receive data.
- Think of it like sending a letter or making a phone call.

**1.2 Two Key Concepts:**

- **Transport**: How the message travels (car, airplane, network cable).
- **Protocol**: The rules for how the message is written and understood.

---

### **Section 2: Transports - The Data Delivery Mechanisms**

**2.1 What is a Transport?**

- It is the method by which data is transmitted between machines.
- Doesn’t care about the _content_, just ensures it gets from A to B.

**2.2 Common Transports:**

| Transport    | Description                                | Examples                      |
| ------------ | ------------------------------------------ | ----------------------------- |
| HTTP         | Standard web transport, reliable           | Web browsing, REST, APIs      |
| TCP          | Reliable, ordered communication            | Web, Email, File downloads    |
| UDP          | Fast but unreliable                        | Games, Video Calls, Streaming |
| WebSocket    | Real-time 2-way connection                 | Chat apps, live tools         |
| stdin/stdout | Local program communication                | Developer tools, AI tools     |
| Named Pipes  | OS-level local inter-process communication | System tools, plugins         |

**2.3 Analogy:**

- Transport is like the vehicle that delivers the message.

---

### **Section 3: Protocols - The Language and Rules of Communication**

**3.1 What is a Protocol?**

- The structure and rules for how machines communicate.
- Protocol defines the format, actions, and expectations for a message.

**3.2 Examples of Protocols:**

| Protocol | Description                                 | Transport Used               |
| -------- | ------------------------------------------- | ---------------------------- |
| REST     | Resource-based communication via HTTP verbs | HTTP                         |
| JSON-RPC | Function-style calls using JSON             | HTTP, WebSocket              |
| GraphQL  | Query-based API access                      | HTTP                         |
| SMTP     | Email sending protocol                      | TCP                          |
| MCP      | LLM-to-tool protocol using JSON-RPC         | Multiple (pipes, HTTP, etc.) |

**3.3 Analogy:**

- Protocol is like the agreed-upon language and message format (English letter, email, etc.).

---

### **Section 4: Understanding REST**

**4.1 What is REST?**

- REST = Representational State Transfer
- Uses HTTP methods to interact with resources.

**4.2 REST Structure:**

- **Resource**: A thing you want to access (user, product).
- **URI**: The path to a resource, e.g., `/users/123`

**4.3 Common HTTP Methods in REST:**

| Method | Meaning                     | Example           |
| ------ | --------------------------- | ----------------- |
| GET    | Retrieve data               | GET /users/123    |
| POST   | Create a new resource       | POST /users       |
| PUT    | Update an existing resource | PUT /users/123    |
| DELETE | Remove a resource           | DELETE /users/123 |

---

### **Section 5: Understanding JSON-RPC**

**5.1 What is JSON-RPC?**

- JSON-based Remote Procedure Call protocol.
- Defines how to call methods/functions remotely.

**5.2 How it Works:**

- Always uses HTTP POST or another transport.
- Uses a consistent message format:

```json
{
  "jsonrpc": "2.0",
  "method": "getUser",
  "params": { "userId": 123 },
  "id": 1
}
```

**5.3 Why POST?**

- Allows complex JSON body
- GET/DELETE have limitations (no body or semantic constraints)

**5.4 No Fixed Verbs Like REST:**

- The `method` field defines the action
- Can be any name: "getUser", "deletePost", etc.

### **Section 6: MCP - Model Context Protocol**

**6.1 What is MCP?**

- A protocol for connecting large language models (LLMs) to tools, data, and external services.
- Based on JSON-RPC

**6.2 Key Components:**

- **Host**: Where the user interacts (e.g., Claude Desktop)
- **Client**: Middle layer that speaks with the MCP server
- **Server**: The actual tools/data that LLMs can call

### Example:

- A Host (e.g., Claude or ChatGPT Agent) sends a JSON-RPC request like tools/list or tools/call via HTTP to the Client.

- The Client handles the routing and invokes the appropriate server/tool.

**6.3 Types of MCP Calls:**

- **Tools**: Functions with side effects (e.g., fetch GitHub issues)
- **Resources**: Structured, read-only data that the LLM can fetch but cannot modify.
- **Prompts**: Predefined templates to Standardize common workflows.

**6.4 Why MCP is Useful:**

- Standardizes tool access
- Decouples LLMs and APIs
- Makes integration modular and reusable
- Supports streaming, session, retries, discovery

**6.5 Example of MCP Workflow:**

    1. Host asks server what tools are available
    2. Server responds with tool schemas
    3. LLM selects and calls a tool
    4. Server executes it and sends response
    5. Client passes response to LLM context

---

### **Section 7: Final Summary**

- ✅ Transports move the data
- ✅ Protocols define what the data means
- ✅ REST uses HTTP and is resource-based
- ✅ JSON-RPC uses JSON to call functions remotely
- ✅ MCP is an advanced protocol built on JSON-RPC for LLMs to use tools

### Now ask yourself:

What are we sending? How are we sending it? Why this format? That leads to understanding the layers: Transport → Protocol → Payload.
