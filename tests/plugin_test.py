import os

import tempfile

from certbot_vault.plugin import VaultInstaller
import unittest
from unittest.mock import patch, MagicMock
import hvac

from certbot._internal import configuration
from certbot._internal import constants


class TestAuthPlugin(unittest.TestCase):
    def setUp(self):
        self.redis_client_mock = patch("hvac.Client").start().return_value
        self.name = "certbot-vault-installer"
        self.name_cfg = self.name.replace("-", "_") + "_"
        self.tempdir = tempfile.mkdtemp(dir=tempfile.gettempdir())
        self.config = configuration.NamespaceConfig(MagicMock(**constants.CLI_DEFAULTS))
        self.config.verb = "certonly"
        self.config.config_dir = os.path.join(self.tempdir, "config")
        self.config.work_dir = os.path.join(self.tempdir, "work")
        self.config.logs_dir = os.path.join(self.tempdir, "logs")
        self.config.cert_path = constants.CLI_DEFAULTS["auth_cert_path"]
        self.config.fullchain_path = constants.CLI_DEFAULTS["auth_chain_path"]
        self.config.chain_path = constants.CLI_DEFAULTS["auth_chain_path"]
        self.config.server = "example.com"
        self.config.certbot_vault_installer_vault_engine_name = "certificates"

        self.config.__setattr__(self.name_cfg + "vault-url", "http://localhost:8200")
        self.config.__setattr__(self.name_cfg + "vault-url", "testike")
        self.subject = VaultInstaller(self.config, self.name)

    def test_http_challenge_gets_saved_to_redis(self):
        sub = tempfile.mkdtemp(dir=tempfile.gettempdir())
        open(os.path.join(sub, "test.crt"), "w+").write("testcrt")
        open(os.path.join(sub, "test.key"), "w+").write("testkey")
        open(os.path.join(sub, "test.chain"), "w+").write("testchain")
        open(os.path.join(sub, "test.fchain"), "w+").write("fullchain")

        self.subject.deploy_cert(
            "test",
            os.path.join(sub, "test.crt"),
            os.path.join(sub, "test.key"),
            os.path.join(sub, "test.chain"),
            os.path.join(sub, "test.fchain"),
        )

        self.redis_client_mock.write.assert_called_with(
            body="testcrt",
            chain="testchain",
            key="testkey",
            path="certificates/le-test",
        )
