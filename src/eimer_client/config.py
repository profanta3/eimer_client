from pydantic_settings import BaseSettings


class ClientConfig(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 22135
