# Using FastMCP CLI

To run this server with the default stdio transport (no matter how you called mcp.run()), you can use the following command:

```sh
fastmcp run task_server.py
```

To run this server with the HTTP transport, you can use the following command:

```sh
fastmcp run my_server.py:mcp --transport http --port 8000
```
