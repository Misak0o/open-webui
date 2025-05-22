from datetime import datetime
from typing import Dict
import docker

class DockerService():
    def __init__(self):
        self.client = docker.from_env()
        self.image = "sandbox-cyber"

    def execute_command(self, command: str, timeout: int = 300):
        start_time = datetime.now()
        result = self.client.containers.run(self.image, command, auto_remove=True)
        # self.client.containers.get(self.image).stop()
        duration = (datetime.now() - start_time).total_seconds()

        text = result.decode('utf-8', errors='replace')
        return text, duration


