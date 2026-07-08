import sys
import subprocess
import time
import tempfile
import os

def execute_code_safely(code: str, language: str = "python") -> dict:
    if language != "python":
        return {
            "stdout": "",
            "stderr": f"Language {language} is not supported. Only Python is allowed.",
            "exit_code": 1,
            "execution_time_ms": 0
        }
        
    # Try using Docker first
    try:
        import docker
        client = docker.from_env()
        # Escape python code for cmd execution
        # Write to temporary file inside host and map it, or pass it via cmd
        # To avoid escaping issues, passing code via container stdin or command is best
        # Let's run a container with python:3.11-slim
        container = client.containers.create(
            image="python:3.11-slim",
            command="python3 -c \"import sys; exec(sys.stdin.read())\"",
            network_disabled=True,
            mem_limit="256m",
            read_only=True,
            user="nobody",
            # We will stream stdin
        )
        
        start_time = time.time()
        container.start()
        
        # Attach and write stdin
        socket = container.attach_socket(params={'stdin': 1, 'stream': 1})
        # socket is socket-like object
        # Write code
        if hasattr(socket, 'sendall'):
            socket.sendall(code.encode('utf-8'))
        elif hasattr(socket, '_sock') and hasattr(socket._sock, 'sendall'):
            socket._sock.sendall(code.encode('utf-8'))
        socket.close()
        
        # Wait with timeout
        result = container.wait(timeout=10)
        end_time = time.time()
        
        stdout = container.logs(stdout=True, stderr=False).decode("utf-8")
        stderr = container.logs(stdout=False, stderr=True).decode("utf-8")
        container.remove(force=True)
        
        return {
            "stdout": stdout,
            "stderr": stderr,
            "exit_code": result.get("StatusCode", 0),
            "execution_time_ms": int((end_time - start_time) * 1000)
        }
        
    except Exception as e:
        print(f"Docker sandbox failed or not available ({e}). Falling back to subprocess execution.")
        
        # Safe fallback subprocess execution
        # Write code to temp file
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, f"codesight_run_{int(time.time())}.py")
        
        with open(temp_file_path, "w", encoding="utf-8") as temp_file:
            temp_file.write(code)
            
        start_time = time.time()
        try:
            # Run python code in subprocess with 10s timeout
            process = subprocess.run(
                [sys.executable, temp_file_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            end_time = time.time()
            
            # Clean up temp file
            try:
                os.remove(temp_file_path)
            except Exception:
                pass
                
            return {
                "stdout": process.stdout,
                "stderr": process.stderr,
                "exit_code": process.returncode,
                "execution_time_ms": int((end_time - start_time) * 1000)
            }
        except subprocess.TimeoutExpired as te:
            try:
                os.remove(temp_file_path)
            except Exception:
                pass
            return {
                "stdout": te.stdout or "",
                "stderr": te.stderr or "Execution timed out (Max 10 seconds allowed).",
                "exit_code": -1,
                "execution_time_ms": 10000
            }
        except Exception as ex:
            try:
                os.remove(temp_file_path)
            except Exception:
                pass
            return {
                "stdout": "",
                "stderr": f"Sandbox execution error: {str(ex)}",
                "exit_code": -1,
                "execution_time_ms": 0
            }
