import base64
import io
import socket
from abc import ABC
from pathlib import Path

from PIL import Image

from eimer_client.config import ClientConfig
from eimer_client.log import log
from eimer_client.move import Move


class BaseClient(ABC):
    """
    Base class for all clients.
    """

    def __init__(
        self,
        team_name: str,
        image_path: str,
        config: ClientConfig | None = None,
        *args,
        **kwargs,
    ):
        """
        Initialize the client.
        """
        self.team_name: str = team_name
        self.config: ClientConfig = config or ClientConfig()
        log.info("Started EimerClient", team_name=self.team_name, config=self.config)
        self.image_path: Path = Path(image_path)

        assert self.image_path.exists(), f"Image path {self.image_path} does not exist."

        # Register the client to the server
        self.socket: socket.SocketIO = self.register()

    def _send(self, data: str):
        """
        Send data to the server.
        """

        self.socket.sendall(f"{self.team_name}\n{data}\n".encode("utf-8"))
        # s.close()

    def send_move(self, move: Move) -> None:
        """
        Send move to the server.
        """
        log.info("Sending move for client", team_name=self.team_name, move=move)
        self._send(move.model_dump())

    def get_num_players(self) -> int:
        """
        Get number of players in the team.
        """
        return self._send(f"get_num_players {self.team_name}")

    def get_time_limit(self) -> float:
        """
        Get time limit for the server.
        """
        return 1.0

    def get_expected_network_latency(self) -> float:
        """
        Get expected network latency for the server.
        """
        return 0.1

    def receive_move(self) -> Move:
        """
        Receive move from the server.
        """
        log.info(f"Receiving move for client {self.team_name}")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.config.host, self.config.port))
        s.sendall(bytes([1]))
        data = s.recv(1024).decode("utf-8")
        log.info(f"Received move for client {self.team_name}: {data}")

    def register(self) -> socket.SocketIO:
        """
        Register the client to the server and return the socket connection.
        """

        log.info(f"Registering to client {self.team_name} with logo {self.image_path}")

        with open(self.image_path, "rb") as image_file:
            img = Image.open(image_file)
            img = img.resize((256, 256))
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format="PNG")
            img_byte_arr = img_byte_arr.getvalue()

        encoded_image = base64.b64encode(img_byte_arr).decode("utf-8")

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.config.host, self.config.port))
        # Send version byte
        s.sendall(bytes([1]))

        s.sendall((self.team_name + "\n" + encoded_image + "\n").encode("utf-8"))

        log.info(f"Client {self.team_name} connected and logo sent.")
        return s

    def close(self):
        """
        Close the client.
        """
        log.info(f"Closing client {self.team_name}")
        self.socket.close()
