#!/usr/bin/env python3
import json
import sys

"""
Genesis modification script on a exported genesis file from umeemania-1 umee testnet.
Usage:
$ ./umeemania-fork.py genesis_file_path.json tinkered_genesis_path.json
"""

from cosmos_genesis_tinker import Validator, GenesisTinker

GENESIS_ARCHIVE = "festival.genesis.json"
OUTPUT_GENESIS = "tinkered_genesis.json"
if len(sys.argv) > 1:
  GENESIS_ARCHIVE = sys.argv[1]
if len(sys.argv) > 2:
  OUTPUT_GENESIS = sys.argv[2]

DENOM = "uumee"
# It is currently less than this...
UMEE_SUPLY = 2000000000000000000
UMEE_SUPLY_3X =  UMEE_SUPLY * 3

# Cope Validator
coping = Validator()
coping.self_delegation_address = 'umee1pprgkthxc2yhr5gvuk2tcjjchfhq6n96xg427t'
coping.self_delegation_public_key = 'AoU6ZVoJ3Fig6+cP8qrLJu7hKaySD84FiNZ62nMo9OPL'
coping.operator_address = 'umeevaloper1pprgkthxc2yhr5gvuk2tcjjchfhq6n96xvj90p'
coping.address = 'C913552357B2B69C728EB645B528C94A30DB7AB4'
coping.public_key = '+LCKUZH2o+2V5G4Nvl7apMoIFml6eW5zXNO69+DvaIA='
coping.consensus_address = 'umeevalcons1pprgkthxc2yhr5gvuk2tcjjchfhq6n96jlperq'

tinkerer = GenesisTinker(input_file=GENESIS_ARCHIVE, output_file=OUTPUT_GENESIS)

tinkerer.add_task(tinkerer.increase_delegator_stake_to_validator,
                  delegator=coping.to_delegator(),
                  validator=coping,
                  increase={'amount': UMEE_SUPLY_3X, 'denom': DENOM})

tinkerer.add_task(tinkerer.set_leverage_last_interest_time)

# Set governance parameters
tinkerer.add_task(tinkerer.set_min_deposit, min_amount='1', denom=DENOM)  # 1 uumee
tinkerer.add_task(tinkerer.set_tally_param,
                  parameter_name='quorum', value='0.000000000000000001')
tinkerer.add_task(tinkerer.set_tally_param,
                  parameter_name='threshold', value='0.000000000000000001')
tinkerer.add_task(tinkerer.set_voting_period, voting_period='10s')
# Make redelegations faster
tinkerer.add_task(tinkerer.set_unbonding_time, unbonding_time='1s')

tinkerer.run_tasks()
