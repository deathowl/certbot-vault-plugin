from setuptools import setup
from setuptools import find_packages


setup(
    name='certbot-vault2',  # Required
    version='0.3.7',  # Required
    description='Certbot plugin to store certificates in Hashicorp Vault',
    url='https://github.com/vitalvas/certbot-vault-plugin',  # Optional

    author='Vitaliy Vasilenko',  # Optional
    author_email='<source@vitalvas.com>',  # Optional

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Networking',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities'
    ],

    packages=find_packages(),  # Required
    include_package_data=True,

    install_requires=[
        'acme>=0.22.0',
        'certbot>=0.22.0',
        'PyOpenSSL',
        'setuptools',
        'zope.component',
        'zope.event',
        'zope.interface',
        'hvac'
    ],

    entry_points={
        'certbot.plugins': [
            'vault = certbot_vault.plugin:VaultInstaller',
        ],
    }
)
