#!/usr/bin/env python3
import subprocess
import json
import sys

"""
Genesis modification script on a exported genesis file from canon-3 umee testnet https://explorer.network.umee.cc/ to do an hard-fork.
Usage:
$ ./umeecanon-3-fork.py genesis_file_path.json tinkered_genesis_path.json
"""

from delegator import to_delegator
from cosmos_genesis_tinker import Validator, GenesisTinker

GENESIS_ARCHIVE = "umeemainnet.genesis.json"
OUTPUT_GENESIS = "tinkered_genesis.json"
if len(sys.argv) > 1:
  GENESIS_ARCHIVE = sys.argv[1]
if len(sys.argv) > 2:
  OUTPUT_GENESIS = sys.argv[2]

DENOM = "uumee"
UUMEE_STAKE_INCREASE = 550000000000000000 * 1000000
UUMEE_LIQUID_TOKEN_INCREASE = 175000000000 * 1000000

UMEE_TESTNET_CHAIN_ID = "canon3-local-testnet"

tinkerer = GenesisTinker(input_file=GENESIS_ARCHIVE, output_file=OUTPUT_GENESIS)

# validator with most power in network. = https://explorer.network.umee.cc/canon-3/staking/umeevaloper1meta6ef76av8rqyhrklau9xuufp7lnt43uf69p
val9Top1 = Validator()
val9Top1.self_delegation_address = 'umee1meta6ef76av8rqyhrklau9xuufp7lnt43cw45t'
val9Top1.self_delegation_public_key = 'AyDIaQJ/uaX/ICtEj+YtL57NZsG/ewEJJex4iolhYXcM'
val9Top1.operator_address = 'umeevaloper1meta6ef76av8rqyhrklau9xuufp7lnt43uf69p'
val9Top1.address = 'C7B14EAF7F406DED475E6A4CFBDA16C68BAEEFF5'
val9Top1.public_key = 'qel+Z+szeQX51EQCAcMtrxJ+kypMmLPYi3/JXv2kr5c='
val9Top1.consensus_address = 'umeevalcons1c7c5atmlgpk76367dfx0hkskc696aml4pdl8v3'

# New Validator
newVal = Validator()
newVal.self_delegation_address = 'umee1pprgkthxc2yhr5gvuk2tcjjchfhq6n96xg427t'
newVal.self_delegation_public_key = 'AoU6ZVoJ3Fig6+cP8qrLJu7hKaySD84FiNZ62nMo9OPL'
newVal.operator_address = 'umeevaloper1pprgkthxc2yhr5gvuk2tcjjchfhq6n96xvj90p'
newVal.address = '7D35FC0DFB01B1433771E45F85CE39765A978CAC'
newVal.public_key = 'opsA/9zZ2RveY0aG+b522CN6TpTvZXa0u1CKBcRYkP4='
newVal.consensus_address = 'umeevalcons1056lcr0mqxc5xdm3u30ctn3ewedf0r9v6ndky4'

tinkerer.add_task(tinkerer.replace_validator,
                 old_validator=val9Top1,
                 new_validator=newVal)

tinkerer.add_task(tinkerer.set_chain_id,
                 chain_id=UMEE_TESTNET_CHAIN_ID)

tinkerer.add_task(tinkerer.increase_balance,
                 address=newVal.self_delegation_address,
                 amount=UUMEE_LIQUID_TOKEN_INCREASE,
                 denom=DENOM)

tinkerer.add_task(tinkerer.increase_delegator_stake_to_validator,
                 delegator=to_delegator(newVal),
                 validator=newVal,
                 increase={'amount': UUMEE_STAKE_INCREASE,
                           'denom': DENOM})

# Set new governance parameters for convenience
tinkerer.add_task(tinkerer.set_min_deposit,
                 min_amount='1',
                 denom=DENOM)
tinkerer.add_task(tinkerer.set_tally_param,
                 parameter_name='quorum',
                 value='0.000000000000000001')
tinkerer.add_task(tinkerer.set_tally_param,
                 parameter_name='threshold',
                 value='0.000000000000000001')
tinkerer.add_task(tinkerer.set_voting_period,
                 voting_period='10s')

# Make redelegations faster
tinkerer.add_task(tinkerer.set_unbonding_time,
                 unbonding_time='1s')

tinkerer.run_tasks()
