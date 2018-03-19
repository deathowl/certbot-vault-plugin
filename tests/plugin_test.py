import os
import sys
import tempfile

import pytest
import tempfile
SETTINGS_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))
sys.path.insert(0, SETTINGS_DIRECTORY)
from certbot_vault.plugin import Installer
import mock
import hvac

from certbot import achallenges, configuration

from certbot import constants

from certbot.tests import acme_util




class TestAuthPlugin(object):
    @mock.patch('hvac.Client', mock.MagicMock(hvac.Client))
    def setup_method(self, method):
        self.name = 'certbot-vault-installer'
        self.name_cfg = self.name.replace('-', '_') + '_'
        self.tempdir = tempfile.mkdtemp(dir=tempfile.gettempdir())
        self.config = configuration.NamespaceConfig(
            mock.MagicMock(**constants.CLI_DEFAULTS)
        )
        self.config.verb = "certonly"
        self.config.config_dir = os.path.join(self.tempdir, 'config')
        self.config.work_dir = os.path.join(self.tempdir, 'work')
        self.config.logs_dir = os.path.join(self.tempdir, 'logs')
        self.config.cert_path = constants.CLI_DEFAULTS['auth_cert_path']
        self.config.fullchain_path = constants.CLI_DEFAULTS['auth_chain_path']
        self.config.chain_path = constants.CLI_DEFAULTS['auth_chain_path']
        self.config.server = "example.com"
        self.config.__setattr__(self.name_cfg + 'vault-url', "http://localhost:8200")
        self.config.__setattr__(self.name_cfg + 'vault-url', "testike")
        self.subject = Installer(self.config, self.name)
        self.subject.hvac_client.write = mock.MagicMock(hvac.Client)




    def test_http_challenge_gets_saved_to_redis(self):
        sub = tempfile.mkdtemp(dir=tempfile.gettempdir())
        open(os.path.join(sub, "test.crt"), "w+").write("testcrt")
        open(os.path.join(sub, "test.key"), "w+").write("testkey")
        open(os.path.join(sub, "test.chain"), "w+").write("testchain")

        self.subject.deploy_cert("test", os.path.join(sub, "test.crt"),  os.path.join(sub, "test.key"),
                                 os.path.join(sub, "test.chain"), "")
        self.subject.hvac_client.write.assert_called_with(body='testcrt', chain='testchain', key='testkey',
                                                          path='certificates/le-test')
