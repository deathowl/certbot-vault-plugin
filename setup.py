from setuptools import setup
from setuptools import find_packages


setup(
    name='certbot-vault',  # Required
    version='0.3.8',  # Required
    description='Certbot plugin to store certificates in Hashicorp Vault',
    url='https://github.com/deathowl/certbot-vault-plugin',  # Optional


    author='Balint Csergo',  # Optional
    author_email='<deathowlzz@gmail.com>',  # Optional

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
