from fastmcp import FastMCP
from datetime import datetime

# Create the MCP server
mcp = FastMCP("TaskTracker")

# Simple in-memory task storage
tasks = []              # List of tasks
task_id_counter = 1     # Unique IDs for each task

# ------ Create Tools ------
# Tools are functions decorated with @mcp.tool()

# Give the model create, read, update, and delete (CRUD) operations 
# for task management.

# Add task to the list
# - Takes a task title (required) and an optional description.
# - Creates a task dictionary with a unique ID, status, and timestamp.
# - Adds it to our tasks list.
# - Returns the created task.
@mcp.tool()
def add_task(title: str, description: str="") -> dict:
    """Add a new task to the task list"""
    global task_id_counter

    task = {
        "id" : task_id_counter,
        "title" : title,
        "description" : description,
        "status" : "pending",
        "created_at" : datetime.now().isoformat()
    }

    tasks.append(task)
    task_id_counter += 1

    return task

# Complete a task
# - Search the task list for a matching ID.
# - Update its status to “completed”.
# - Stamps it with a completion timestamp.
# - Return the updated task or an error message if no match is found.
@mcp.tool()
def complete_task(task_id: int) -> dict:
    """Mark a task as completed"""
    for task in tasks :
        if task["id"] == task_id :
            task["status"] = "completed"
            task["completed_at"] = datetime.now().isoformat()
            return task
    
    return {"error": f"Task: {task_id} not found"}

# Delete a task
# - Search for a task
# - Remove it from the list
# - Return confirmation with the deleted task data.
@mcp.tool()
def delete_task(task_id: int) -> dict:
    """Delete a task from the list"""
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            deleted_task = tasks.pop(i)
            return {"Success": True, "deleted": deleted_task}
    
    return {"success": False, "error": f"Tasj {task_id} not found"}


# ------ Create Resources ------
# Resources let the AI application view data without modifying it.
# Resources are functions decorated with @mcp.resource()
# Resources work well for data the model needs to read frequently without making changes.

# View All Tasks
# Return the complete taks list.
# - The decorator @mcp.resource("tasks://all") creates a resource with a URI-like identifier.
# - Format all tasks into readable text with emojis for visual clarity.
# - Return a simple message if no tasks exist.
@mcp.resource("tasks://all")
def get_all_tasks() -> str:
    """Get all tasks as formatted text."""
    if not tasks:
        return "No tasks found"
    
    result = "Current Tasks:\n\n"
    for task in tasks:
        status_emoji = "✅" if task["status"] == "completed" else "⏳"
        result += f"{status_emoji} [{task['id']}] {task['title']}\n"
        if task["description"]:
            result += f"   Description: {task['description']}\n"
        result += f"   Status: {task['status']}\n"
        result += f"   Created: {task['created_at']}\n\n"
    
    return result

# View Pending Tasks
# Filters and return incomplete tasks
# - Filter the task list down to pending items only
# - Format pending items for easy reading
# - Returns a message if there’s nothing left to do.
@mcp.resource("tasks://pending")
def get_pending_tasks() -> str:
    """Get only pending tasks."""
    pending = [t for t in tasks if t["status"] == "pending"]
    
    if not pending:
        return "No pending tasks!"
    
    result = "Pending Tasks:\n\n"
    for task in pending:
        result += f"⏳ [{task['id']}] {task['title']}\n"
        if task["description"]:
            result += f"   {task['description']}\n"
        result += "\n"
    
    return result

# ------ Define Prompts ------
# Prompts guide how the AI application interacts with your server.
# Prompts are functions decorated with @mcp.resource()
# Prompts make AI interactions consistent and useful.

# Define a structured template for task analysis
# - Tell the AI what information to include
# - Reference the resource to use for data.

@mcp.prompt()
def task_summary_prompt() -> str:
    """Generate a prompt for summarizing tasks."""
    return """Please analyze the current task list and provide:

1. Total number of tasks (completed vs pending)
2. Any overdue or high-priority items
3. Suggested next actions
4. Overall progress assessment

Use the tasks://all resource to access the complete task list."""

# ------ Run the server ------

# Run on stdio for local servers
if __name__ == "__main__":
    mcp.run()             

# Run on http for remote access
#if __name__ == "__main__":
#    mcp.run(transport="http", port=8000)