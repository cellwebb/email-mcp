import json
import sys
import email_fetcher

class EmailMCPServer:
    """A simple MCP server for email operations using STDIO transport."""
    
    def __init__(self):
        self.tools = [
            {
                "name": "get_emails",
                "description": "Retrieve recent emails from inbox",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "integer",
                            "description": "Number of emails to retrieve"
                        }
                    },
                    "required": []
                }
            },
            {
                "name": "delete_email",
                "description": "Delete an email by ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email_id": {
                            "type": "string",
                            "description": "Email ID to delete"
                        }
                    },
                    "required": ["email_id"]
                }
            }
        ]
    
    def process_request(self, request):
        """Process incoming JSON-RPC request."""
        if request.get("method") == "list_tools":
            return {"jsonrpc": "2.0", "result": self.tools, "id": request.get("id")}
        
        elif request.get("method") == "call_tool":
            tool_name = request.get("params", {}).get("name")
            tool_params = request.get("params", {}).get("parameters", {})
            
            if tool_name == "get_emails":
                limit = tool_params.get("limit", 5)
                emails = email_fetcher.fetch_emails(limit)
                return {"jsonrpc": "2.0", "result": emails, "id": request.get("id")}
            
            elif tool_name == "delete_email":
                email_id = tool_params.get("email_id")
                result = email_fetcher.delete_email(email_id)
                return {
                    "jsonrpc": "2.0", 
                    "result": result, 
                    "id": request.get("id")
                }
            
            return {
                "jsonrpc": "2.0", 
                "error": {"code": -32601, "message": "Method not found"}, 
                "id": request.get("id")
            }
        
        return {
            "jsonrpc": "2.0", 
            "error": {"code": -32600, "message": "Invalid request"}, 
            "id": request.get("id")
        }

    def start(self):
        """Start the MCP server using STDIO transport."""
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break
                    
                request = json.loads(line)
                response = self.process_request(request)
                
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
                
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "error": {"code": -32603, "message": f"Internal error: {str(e)}"},
                    "id": None
                }
                sys.stdout.write(json.dumps(error_response) + "\n")
                sys.stdout.flush()

if __name__ == "__main__":
    server = EmailMCPServer()
    server.start()
