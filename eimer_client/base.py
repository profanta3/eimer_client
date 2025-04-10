import socket
from abc import ABC
from pathlib import Path

from eimer_client.api import MoveCode
from eimer_client.config import ClientConfig
from eimer_client.log import log
from eimer_client.move import Move
from eimer_client.utils import encode_image


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

        self.time_limit: float | None = None
        self.player_number: int | None = None

        self.socket: socket.SocketIO | None = None

        # Register the client to the server
        self._register()

    def send_move(self, move: Move) -> bool:
        """Sends a move as a sequence of bytes over a socket, preserving leading zeros."""

        MoveLUT = [
            [None, 8, None, None],  # From 0
            [7, None, 9, None],  # From 1
            [None, 6, None, 10],  # From 2
            [None, None, None, None],  # From 3
        ]

        move = MoveLUT[move.first][move.second]

        if move is not None:
            move_bytes = bytes([MoveLUT[move.first][move.second]])
            self.socket.sendall(move_bytes)
            return True
        else:
            return False

    def get_time_limit(self) -> float:
        """
        Get time limit for the server.
        """
        if not self.time_limit:
            raise ValueError(
                "Time limit not set. There most likely was an error in the registration."
            )
        return self.time_limit

    def get_player_number(self) -> int:
        """
        Get player number for the server.
        """
        if not self.player_number:
            raise ValueError(
                "Player number not set. There most likely was an error in the registration."
            )
        return self.player_number

    def get_expected_network_latency(self) -> float:
        """
        Get expected network latency for the server.
        """
        return 0.1

    def receive_move(self) -> Move:
        """
        Receive move from the server.

        - #201 --> your turn
        - #207 --> invalid
        - #208 --> to late
        - #else ... might follow example in send moves
        """
        recieved = self.socker.recv(1)[0]

        if recieved == MoveCode.YOUR_TURN:
            # Your Turn
            return True
        elif recieved == MoveCode.INVALID:
            # Invalid Turn
            return False
        elif recieved == MoveCode.TO_LATE:
            # Timed Out
            return False
        else:
            return "Fallback"
            # TODO

    def _register(self) -> socket.SocketIO:
        """
        Register the client to the server and return the socket connection.
        """

        log.info(f"Registering to client {self.team_name} with logo {self.image_path}")

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.config.host, self.config.port))

        # Send version byte
        s.sendall(bytes([1]))

        encoded_image = encode_image(self.image_path)
        s.sendall((self.team_name + "\n" + encoded_image + "\n").encode("utf-8"))

        info = s.recv(1)[0]
        player_number = info & 3
        time_limit = info // 4

        self.time_limit = time_limit
        self.player_number = player_number

        log.info(
            f"Client {self.team_name} connected and logo sent.",
            player_number=player_number,
            time_limit=time_limit,
        )
        return s

    def close(self):
        """
        Close the client.
        """
        log.info(f"Closing client {self.team_name}")
        self.socket.close()
