import sys
import time
import os

def execute_code_safely(code: str, language: str = "python") -> dict:
    if language != "python":
        return {
            "stdout": "",
            "stderr": f"Language {language} is not supported. Only Python is allowed.",
            "exit_code": 1,
            "execution_time_ms": 0
        }
        
    try:
        import docker
        client = docker.from_env()
    except Exception as e:
        return {
            "stdout": "",
            "stderr": f"Sandbox Error: Docker is not available or not running on the host system. Execution blocked for security. Details: {e}",
            "exit_code": -1,
            "execution_time_ms": 0
        }
        
    container = None
    try:
        container = client.containers.create(
            image="python:3.11-slim",
            command=["python3", "-c", code],
            network_disabled=True,
            mem_limit="128m",
            cpu_quota=50000, # 50% of CPU
            read_only=True,
            user="nobody",
            stdin_open=False,
            detach=True
        )
        
        start_time = time.time()
        container.start()
        
        # Wait with timeout
        result = container.wait(timeout=10)
        end_time = time.time()
        
        stdout = container.logs(stdout=True, stderr=False).decode("utf-8", errors='replace')
        stderr = container.logs(stdout=False, stderr=True).decode("utf-8", errors='replace')
        container.remove(force=True)
        
        return {
            "stdout": stdout,
            "stderr": stderr,
            "exit_code": result.get("StatusCode", 0),
            "execution_time_ms": int((end_time - start_time) * 1000)
        }
        
    except Exception as ex:
        # Ensure we always clean up
        if container:
            try:
                container.remove(force=True)
            except Exception:
                pass
            
        err_msg = str(ex)
        if "timeout" in err_msg.lower() or "timed out" in err_msg.lower():
            return {
                "stdout": "",
                "stderr": "Execution timed out (Max 10 seconds allowed).",
                "exit_code": -1,
                "execution_time_ms": 10000
            }
            
        return {
            "stdout": "",
            "stderr": f"Sandbox execution error: {str(ex)}",
            "exit_code": -1,
            "execution_time_ms": 0
        }
