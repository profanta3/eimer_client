from eimer_client.base import BaseClient
from eimer_client.config import ClientConfig
from eimer_client.log import log
from eimer_client.move import Move

if __name__ == "__main__":
    clients: list[BaseClient] = []

    for i in range(3):
        client = BaseClient(
            team_name=f"EimerClient{i}",
            image_path="../cat.jpeg",
            config=ClientConfig(),
        )
        clients.append(client)
    # client.register()
    while True:
        prompt = input("Enter command: ")
        if prompt in ["exit", "quit", "q"]:
            break
        elif prompt.startswith("send_move"):
            _, player, first, second = prompt.split()
            client.send_move(
                Move(player=int(player), first=int(first), second=int(second))
            )
        else:
            print("Unknown command")

    log.info("Exiting ...")
    for client in clients:
        client.close()
