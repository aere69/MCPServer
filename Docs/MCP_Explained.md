# MCP Explained

## Introduction

Model Context Protocol (MCP) standardizes how large language models (LLMs) and other AI models interact with external systems. FastMCP is a framework that makes building MCP servers simple.

## The Model Context Protocol

Model Context Protocol (MCP) is an open protocol that defines how AI applications communicate with external systems.

### How MCP Works

MCP has three components:

- **Hosts** are the AI-powered applications users actually interact with. The host can be Claude Desktop, an IDE with AI features, or a custom app you’ve built. The host contains (or interfaces with) the language model and initiates connections to MCP servers.

- **Clients** connect to servers. When a host needs to talk to an MCP server, it creates a client instance to manage that specific connection. One host can run multiple clients simultaneously, each connected to a different server. The client handles all protocol-level communication.

- **Servers** are what you build. They expose specific capabilities — database access, file operations, API integrations — and respond to client requests by providing tools, resources, and prompts.

The user interacts with the host, the host uses a client to talk to your server, and the server returns structured results back up the chain.

### The Three Core Primitives

MCP servers expose three types of functionality:

- **Tools** are functions that perform actions. They’re like executable commands the LLM can invoke. add_task, send_an_email, and query_a_database are some examples of tools.

- **Resources** provide read-only access to data. They allow viewing information without changing it. Examples include lists of tasks, configuration files, and user profiles.

- **Prompts** are templates that guide AI interactions. They structure how the model approaches specific tasks. Examples include “Analyze these tasks and suggest priorities” and “Review this code for security issues.”

In practice, you’ll combine these primitives. An AI model might use a resource to view tasks, then a tool to update one, guided by a prompt that defines the workflow.