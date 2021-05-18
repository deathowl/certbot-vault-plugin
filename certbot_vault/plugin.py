"""Vault Let's Encrypt installer plugin."""

import os
import logging

import zope.interface

import hvac

from certbot import interfaces
from certbot.plugins import common


logger = logging.getLogger(__name__)


@zope.interface.implementer(interfaces.IInstaller)
@zope.interface.provider(interfaces.IPluginFactory)
class VaultInstaller(common.Plugin):
    description = "Vault Cert Installer"

    @classmethod
    def add_parser_arguments(cls, add):
        add("vault-token", default=os.getenv("VAULT_TOKEN"), help="Token for accessing vault")
        add("vault-url", default=os.getenv("VAULT_URL"))
        add(
            "vault-engine-name",
            default=os.getenv("VAULT_ENGINE_NAME", "certificates"),
            help="Secrets engine path",
        )

    def __init__(self, *args, **kwargs):
        super(VaultInstaller, self).__init__(*args, **kwargs)
        self.hvac_client = hvac.Client(self.conf("vault-url"), token=self.conf("vault-token"))

    def prepare(self):
        pass

    def more_info(self):
        return ""

    def get_all_names(self):
        return []

    def deploy_cert(self, domain, cert_path, key_path, chain_path, fullchain_path):
        self.hvac_client.renew_token()
        name = "{engine_name}/le-{domain}".format(
            engine_name=self.conf("vault-engine-name"),
            domain=domain,
        )
        body = open(cert_path).read()
        key = open(key_path).read()
        chain = open(chain_path).read()
        self.hvac_client.write(path=name, body=body, key=key, chain=chain)

    def enhance(self, domain, enhancement, options=None):
        pass

    def supported_enhancements(self):
        return []

    def get_all_certs_keys(self):
        pass

    def save(self, title=None, temporary=False):
        pass

    def rollback_checkpoints(self, rollback=1):
        pass

    def recovery_routine(self):
        pass

    def view_config_changes(self):
        pass

    def config_test(self):
        pass

    def restart(self):
        pass
