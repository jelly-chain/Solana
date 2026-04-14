from __future__ import annotations
import base58
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.api import Client
from solana.rpc.async_api import AsyncClient
from .constants import SOLANA_MAINNET_RPC


class JellychainWallet:
    def __init__(self, keypair: Keypair) -> None:
        self._keypair = keypair

    @property
    def keypair(self) -> Keypair:
        return self._keypair

    @property
    def public_key(self) -> Pubkey:
        return self._keypair.pubkey()

    @classmethod
    def from_base58(cls, private_key_base58: str) -> "JellychainWallet":
        secret_bytes = base58.b58decode(private_key_base58)
        keypair = Keypair.from_bytes(secret_bytes)
        return cls(keypair)

    @classmethod
    def from_bytes(cls, secret_key: bytes) -> "JellychainWallet":
        return cls(Keypair.from_bytes(secret_key))

    @classmethod
    def generate(cls) -> "JellychainWallet":
        return cls(Keypair())

    def to_base58_private_key(self) -> str:
        return base58.b58encode(bytes(self._keypair)).decode("utf-8")

    def __repr__(self) -> str:
        return f"JellychainWallet(public_key={self.public_key})"


def create_client(rpc_url: str = SOLANA_MAINNET_RPC) -> Client:
    return Client(rpc_url, commitment="confirmed")


def create_async_client(rpc_url: str = SOLANA_MAINNET_RPC) -> AsyncClient:
    return AsyncClient(rpc_url, commitment="confirmed")
