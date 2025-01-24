import yaml
from typing import Optional


class CredentialConfig:
    def __init__(self, secret_vault_type: str, secret_vault_name: Optional[str], **kwargs):
        self.secret_vault_type = secret_vault_type
        self.secret_vault_name = secret_vault_name
        self.additional_properties = kwargs

    def __repr__(self):
        return (
            f"Config(secret_vault_type={self.secret_vault_type}, "
            f"secret_vault_name={self.secret_vault_name}, "
            f"additional_properties={self.additional_properties})"
        )

    @classmethod
    def load_credentials(cls, file_path: str) -> list['CredentialConfig']:
        with open(file_path, 'r', encoding='utf-8') as file:
            credentials_data = yaml.safe_load(file)

        credential_configs = []
        for key, value in credentials_data.items():
            if isinstance(value, dict):
                config = cls(secret_vault_type=credentials_data.get('secret_vault_type', 'local'),
                             secret_vault_name=credentials_data.get('secret_vault_name', None),
                             **value)
                credential_configs.append(config)

        return credential_configs
