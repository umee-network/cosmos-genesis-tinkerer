#!/usr/bin/env python3
import subprocess
import json
import sys

"""
Genesis modification script on a exported genesis file from umeemania-1 umee testnet.
Usage:
$ ./umeemainnet-fork.py genesis_file_path.json tinkered_genesis_path.json
"""

from cosmos_genesis_tinker import Validator, Delegator, GenesisTinker

def to_delegator(validator: Validator):
  """
  Returns a new Delegator based on the validator
  """
  delegator = Delegator()
  delegator.address = validator.self_delegation_address
  delegator.public_key = validator.self_delegation_public_key
  return delegator

GENESIS_ARCHIVE = "umeemainnet.genesis.json"
OUTPUT_GENESIS = "tinkered_genesis.json"
if len(sys.argv) > 1:
  GENESIS_ARCHIVE = sys.argv[1]
if len(sys.argv) > 2:
  OUTPUT_GENESIS = sys.argv[2]

DENOM = "uumee"
UUMEE_STAKE_INCREASE = 550000000 * 1000000
UUMEE_LIQUID_TOKEN_INCREASE = 175000000 * 1000000

UMEE_TESTNET_CHAIN_ID = "umeemain-local-testnet"

tinkerer = GenesisTinker(input_file=GENESIS_ARCHIVE, output_file=OUTPUT_GENESIS)
tinkerer.auto_load()
validators = tinkerer.validators

topval = tinkerer.get_top1_validator()
keysParseProcess = subprocess.run(['umeed', 'keys', 'parse', topval.address, '--output', 'json'], check=True, capture_output=True)
jsonAddresses = json.loads(keysParseProcess.stdout)

topval.consensus_address = jsonAddresses["formats"][4]

# New Validator
newValidator = Validator()
newValidator.self_delegation_address = 'umee1pprgkthxc2yhr5gvuk2tcjjchfhq6n96xg427t'
newValidator.self_delegation_public_key = 'AoU6ZVoJ3Fig6+cP8qrLJu7hKaySD84FiNZ62nMo9OPL'
newValidator.operator_address = 'umeevaloper1pprgkthxc2yhr5gvuk2tcjjchfhq6n96xvj90p'
newValidator.address = 'C913552357B2B69C728EB645B528C94A30DB7AB4'
newValidator.public_key = '+LCKUZH2o+2V5G4Nvl7apMoIFml6eW5zXNO69+DvaIA='
newValidator.consensus_address = 'umeevalcons1pprgkthxc2yhr5gvuk2tcjjchfhq6n96jlperq'


tinkerer.add_task(tinkerer.replace_validator,
                 old_validator=topval,
                 new_validator=newValidator)

tinkerer.add_task(tinkerer.set_chain_id,
                 chain_id=UMEE_TESTNET_CHAIN_ID)

tinkerer.add_task(tinkerer.increase_balance,
                 address=newValidator.self_delegation_address,
                 amount=UUMEE_LIQUID_TOKEN_INCREASE,
                 denom=DENOM)

tinkerer.add_task(tinkerer.increase_delegator_stake_to_validator,
                 delegator=to_delegator(newValidator),
                 validator=newValidator,
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
