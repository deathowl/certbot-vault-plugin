"""Vault Let's Encrypt installer plugin."""

from __future__ import print_function

import os
import logging
import hvac

import zope.interface
import OpenSSL.crypto

from datetime import datetime
from certbot import interfaces
from certbot import errors
from certbot.plugins import common


logger = logging.getLogger(__name__)


@zope.interface.implementer(interfaces.IInstaller)
@zope.interface.provider(interfaces.IPluginFactory)
class VaultInstaller(common.Plugin):
    description = "Vault Cert Installer"

    @classmethod
    def add_parser_arguments(cls, add):
        add('auth-path',
            default=os.getenv('VAULT_AUTH_PATH'),
            help='Auth path'
        )
        add("token",
            default=os.getenv('VAULT_TOKEN'),
            help="Vault access token"
        )
        add("role-id",
            default=os.getenv('VAULT_ROLE_ID'),
            help='AppRole ID'
        )
        add("secret-id",
            default=os.getenv('VAULT_SECRET_ID'),
            help='AppRole Secret ID'
        )
        add("jwt-role",
            default=os.getenv('VAULT_JWT_ROLE'),
            help='JWT Role'
        )
        add("jwt-key",
            default=os.getenv('VAULT_JWT_KEY'),
            help='JWT Key'
        )
        add("addr",
            default=os.getenv('VAULT_ADDR'),
            help="Vault URL"
        )
        add("mount",
            default=os.getenv('VAULT_MOUNT'),
            help="Vault Mount Point"
        )
        add("path",
            default=os.getenv('VAULT_PATH'),
            help="Vault Mount Point"
        )

    def __init__(self, *args, **kwargs):
        super(VaultInstaller, self).__init__(*args, **kwargs)
        self.hvac_client = hvac.Client(self.conf('addr'))

        if self.conf('token'):
            self.hvac_client.token = self.conf('token')

        if self.conf('role-id') and self.conf('secret-id'):
            auth_mount_point = self.conf('auth-path') or 'approle'
            self.hvac_client.auth.approle.login(
                self.conf('role-id'),
                self.conf('secret-id'),
                mount_point=auth_mount_point
            )

        if self.conf('jwt-role') and self.conf('jwt-key'):
            self.hvac_client.auth.jwt.jwt_login(
                self.conf('jwt-role'),
                self.conf('jwt-key'),
                path=self.conf('auth-path')
            )

    def prepare(self):  # pylint: disable=missing-docstring,no-self-use
        """
        Prepare the plugin
        """

        if not self.hvac_client.is_authenticated():
            raise errors.PluginError('Not authenticated')

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        """
        Human-readable string to help understand the module
        """
        return (
            "Hashicorp Vault Plugin",
            "Vault: %s" % (
                self.conf('addr'),
            )
        )

    def get_all_names(self):  # pylint: disable=missing-docstring,no-self-use
        return []

    def deploy_cert(self, domain, cert_path, key_path, chain_path, fullchain_path):
        """
        Upload Certificate to Vault

        :param str domain: domain to deploy certificate file
        :param str cert_path: absolute path to the certificate file
        :param str key_path: absolute path to the private key file
        :param str chain_path: absolute path to the certificate chain file
        :param str fullchain_path: absolute path to the certificate fullchain file (cert plus chain)

        :raises .PluginError: when cert cannot be deployed
        """

        cert = open(cert_path).read()

        date_format = "%Y%m%d%H%M%SZ"

        openssl_cert = OpenSSL.crypto.load_certificate(
            OpenSSL.crypto.FILETYPE_PEM,
            cert
        )

        data = {
            'type': 'urn:scheme:type:certificate',
            'cert': cert,
            'key': open(key_path).read(),
            'chain': open(fullchain_path).read(),
            'serial': str(openssl_cert.get_serial_number()),
            'life': {
                'issued': int(datetime.strptime(openssl_cert.get_notBefore().decode(), date_format).timestamp()),
                'expires': int(datetime.strptime(openssl_cert.get_notAfter().decode(), date_format).timestamp()),
            }
        }

        domains = []
        ext_count = openssl_cert.get_extension_count()
        for i in range(0, ext_count):
            ext = openssl_cert.get_extension(i)
            if 'subjectAltName' in str(ext.get_short_name()):
                sub = ext._subjectAltNameString()
                for row in [x.strip() for x in sub.split(',')]:
                    if row.startswith('DNS:'):
                        domains.append(row[len('DNS:'):])

        if domains:
            data['domains'] = domains

        int_path = domain
        if self.conf('path'):
            int_path = os.path.join(self.conf('path'), domain)

        self.hvac_client.secrets.kv.v2.create_or_update_secret(
            mount_point=self.conf('mount'),
            path=int_path,
            secret=data
        )

    def enhance(self, domain, enhancement, options=None):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def supported_enhancements(self):  # pylint: disable=missing-docstring,no-self-use
        return []  # pragma: no cover

    def get_all_certs_keys(self):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def save(self, title=None, temporary=False):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def rollback_checkpoints(self, rollback=1):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def recovery_routine(self):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def view_config_changes(self):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def config_test(self):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def restart(self):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover
