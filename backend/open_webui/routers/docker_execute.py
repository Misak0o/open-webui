from datetime import datetime
from typing import Dict
import docker
from fastapi import HTTPException

class DockerService():
    def __init__(self):
        self.client = docker.from_env()
        self.image = "sandbox-cyber"
        self.timeout = 300

    async def execute_command(self, command: str):
        start_time = datetime.now()
        try:
            result = self.client.containers.run(self.image, command, auto_remove=True)
            duration = (datetime.now() - start_time).total_seconds()
            text = result.decode('utf-8', errors='replace')
            return text, duration
        except Exception as e:
            raise HTTPException(500, "Probleme docker_execute")


