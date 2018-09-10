import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from hostmasternoded import hostmasternodeDaemon
from hostmasternode_config import hostmasternodeConfig


def test_hostmasternoded():
    config_text = hostmasternodeConfig.slurp_config_file(config.hostmasternode_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'00000ffd590b1485b3caadc19b22e6379c733355108f107a430458cdf3407ab6'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000121a30a3946b96d3fd5f42889f479f72d741b4a396daa46a0b2a5053598'

    creds = hostmasternodeConfig.get_rpc_creds(config_text, network)
    hostmasternoded = hostmasternodeDaemon(**creds)
    assert hostmasternoded.rpc_command is not None

    assert hasattr(hostmasternoded, 'rpc_connection')

    # hostmasternode testnet block 0 hash == 00000121a30a3946b96d3fd5f42889f479f72d741b4a396daa46a0b2a5053598
    # test commands without arguments
    info = hostmasternoded.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert hostmasternoded.rpc_command('getblockhash', 0) == genesis_hash
