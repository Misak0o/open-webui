from datetime import datetime
import docker

class DockerService:
    def __init__(self):
        self.client = docker.from_env()
        self.image = "sandbox-cyber"
        self.memory_limit = "512m"
    
    async def execute_command(self, command: str):
        start_time = datetime.now()
        try:
            result = self.client.containers.run(
                self.image,
                command,
                detach=True,
                stderr=True,
                mem_limit=self.memory_limit,
                security_opt=["no-new-privileges:true"]
            )
            result.wait()
            duration = (datetime.now() - start_time).total_seconds()
            output = result.logs().decode('utf-8', errors='replace')
            result.remove()
            return {
                "stdout": output,
                "stderr": "",
                "returncode": 0
            }, duration
            
        except docker.errors.ContainerError as e:
            duration = (datetime.now() - start_time).total_seconds()
            return {
                "stdout": e.stdout.decode('utf-8', errors='replace') if e.stdout else "",
                "stderr": e.stderr.decode('utf-8', errors='replace') if e.stderr else str(e),
                "returncode": e.exit_status
            }, duration
            
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            return {
                "stdout": "",
                "stderr": f"Docker error: {str(e)}",
                "returncode": -1
            }, duration

