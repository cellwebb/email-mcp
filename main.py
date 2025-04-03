import subprocess
import os
import time
import json

def setup_mcp_config():
    """Create MCP configuration file."""
    config = {
        "mcpServers": {
            "email": {
                "command": "python",
                "args": ["mcp_email_server.py"]
            }
        }
    }
    
    with open("mcp_config.json", "w") as f:
        json.dump(config, f, indent=2)

def main():
    print("Setting up MCP configuration...")
    setup_mcp_config()
    
    print("\nStarting MCP host with Ollama integration...")
    print("Enter 'exit' to quit.")
    
    # Check if mcphost is installed
    try:
        subprocess.run(["mcphost", "--version"], 
                       stdout=subprocess.PIPE, 
                       stderr=subprocess.PIPE, 
                       check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("mcphost not found. Installing...")
        subprocess.run(["pip", "install", "mcphost"], check=True)
    
    # Uses mcphost to connect Ollama with our MCP server
    process = subprocess.Popen(
        ["mcphost", "--config", "mcp_config.json", "--model", "ollama:qwen2.5:3b"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    # Simple interactive prompt
    print("\n=== Email Management Session Started ===")
    print("Tip: Ask the AI to 'analyze my recent emails and suggest which ones to delete'")
    
    try:
        while True:
            try:
                user_input = input("\nYou: ")
                if user_input.lower() == "exit":
                    break
                    
                # Send to mcphost
                process.stdin.write(user_input + "\n")
                process.stdin.flush()
                
                # Get response (this is simplified - real implementation would be more robust)
                time.sleep(2)  # Give the model time to respond
                
                # Read available output
                response = ""
                while True:
                    if process.stdout.readable() and not process.stdout.closed:
                        line = process.stdout.readline()
                        if not line:
                            break
                        response += line
                    else:
                        break
                
                print("\nAI:", response)
                
            except KeyboardInterrupt:
                break
    finally:
        print("\nShutting down...")
        process.terminate()

if __name__ == "__main__":
    main()
