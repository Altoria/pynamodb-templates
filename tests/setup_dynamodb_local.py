import logging
import time
import unittest
from typing import Optional, Union, Iterable
from uuid import uuid4

import docker
import requests
from docker.errors import NotFound
from pynamodb.models import Model

"""
Wrapper script to run container using

docker run -p 8000:8000 amazon/dynamodb-local -jar DynamoDBLocal.jar -inMemory -sharedDb
"""

__all__ = ["run_local_dynamodb", "stop_local_dynamodb", "DynamodbLocalTest"]

IMAGE = "amazon/dynamodb-local"

client = docker.DockerClient()


def run_local_dynamodb(name=None, port=None):
    if name is None:
        name = str(uuid4())

    port_key = "8000/tcp"

    try:
        container = client.containers.run(
            name=name,
            image=IMAGE,
            command="-jar DynamoDBLocal.jar -inMemory -sharedDb",
            remove=True,
            auto_remove=True,
            detach=True,
            ports={port_key: port},
        )
        while True:
            try:
                container.reload()
                port = int(container.ports.get(port_key, [])[0].get("HostPort"))
                time.sleep(0.5)
                response = requests.get(f"http://localhost:{port}")
                if response.status_code in (200, 400):
                    break
            except Exception as e:
                logging.debug(e, exc_info=True)
    except Exception as e:
        try:
            container = client.containers.get(name)
            container.remove(force=True)
        except NotFound:
            pass
        raise e
    return f"http://localhost:{port}"


def stop_local_dynamodb(name: Optional[str]):
    try:
        container = client.containers.get(container_id=name)
        container.stop()
    except Exception as e:
        logging.error(e, exc_info=True)


class DynamodbLocalTest(unittest.TestCase):
    container_name = str(uuid4())

    PYNAMODB_MODEL: Union[Model, Iterable[Model]] = None

    host: Optional[str] = None

    def setUp(self) -> None:
        self.host = run_local_dynamodb(name=self.container_name)

        if isinstance(self.PYNAMODB_MODEL, Model):
            if self.host:
                self.PYNAMODB_MODEL.Meta.host = self.host
            self.PYNAMODB_MODEL.create_table()
        elif isinstance(self.PYNAMODB_MODEL, Iterable):
            for m in self.PYNAMODB_MODEL:  # type: Model
                if self.host:
                    m.Meta.host = self.host
                m.create_table()

    def doCleanups(self) -> None:
        stop_local_dynamodb(name=self.container_name)
