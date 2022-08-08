#!/usr/bin/env python3

from cosmos_genesis_tinker import Validator, Delegator

def to_delegator(validator: Validator):
  """
  Returns a new Delegator based on the validator
  """
  delegator = Delegator()
  delegator.address = validator.self_delegation_address
  delegator.public_key = validator.self_delegation_public_key
  return delegator
