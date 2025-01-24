from dataclasses import dataclass, field
from typing import Optional

@dataclass
class SnowflakeConfig:
    account: Optional[str] = None
    connect_retries: Optional[int] = None
    connect_timeout: Optional[int] = None
    host: Optional[str] = None
    insecure_mode: Optional[bool] = None
    oauth_client_id: Optional[str] = None
    oauth_client_secret: Optional[str] = None
    password: Optional[str] = None
    port: Optional[int] = None
    private_key: Optional[str] = None
    private_key_passphrase: Optional[str] = None
    private_key_path: Optional[str] = None
    role: Optional[str] = None
    token: Optional[str] = None
    user: Optional[str] = None
    warehouse: Optional[str] = None

@dataclass
class MSSQLConfig:
    database: Optional[str] = None
    driver: Optional[str] = None
    server: Optional[str] = None
    port: Optional[int] = None
    user: Optional[str] = None
    password: Optional[str] = None

@dataclass
class CredentialsConfig:
    secret_vault_type: Optional[str] = None
    secret_vault_name: Optional[str] = None

