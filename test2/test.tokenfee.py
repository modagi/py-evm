from eth_keys import keys
from eth_utils import decode_hex, to_wei
from eth_typing import Address

from eth.consensus.pow import mine_pow_nonce
from eth import constants, chains
from eth.vm.forks.simple3 import Simple3VM
from eth.db.atomic import AtomicDB

from eth_hash.auto import keccak

import json

GENESIS_PARAMS = {
    'parent_hash': constants.GENESIS_PARENT_HASH,
    'uncles_hash': constants.EMPTY_UNCLE_HASH,
    'coinbase': constants.ZERO_ADDRESS,
    'transaction_root': constants.BLANK_ROOT_HASH,
    'receipt_root': constants.BLANK_ROOT_HASH,
    'difficulty': 1,
    'block_number': constants.GENESIS_BLOCK_NUMBER,
    'gas_limit': 3000000,
    'timestamp': 1514764800,
    'extra_data': constants.GENESIS_EXTRA_DATA,
    'nonce': constants.GENESIS_NONCE
}

SENDER_PRIVATE_KEY = keys.PrivateKey(
  decode_hex('0x45a915e4d060149eb4365960e6a7a45f334393093061116b197e3240065ff2d8')
)

SENDER = Address(SENDER_PRIVATE_KEY.public_key.to_canonical_address())

RECEIVER = Address(b'\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\x02')

FEE_TOKEN = Address(b'\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\x01')

erc20_bytecode = None
with open('ERC20.json') as erc20_file:
    data = json.load(erc20_file)
    erc20_bytecode = bytes.fromhex(data['bytecode'][2:])

address_bytes = b"\0"*12 + SENDER
balance_bytes = b"\0"*31 + b"\1"

token_storage_key = keccak(address_bytes + balance_bytes)

GENESIS_STATE = {
    SENDER: {
        "balance" : to_wei(10, 'ether'),
        "nonce" : 0,
        "code" : b"",
        "storage" : {}
    },
    FEE_TOKEN: {
        "balance" : 0,
        "nonce" : 0,
        "code" : b"erc20_bytecode",
        "storage" : { int.from_bytes(token_storage_key, byteorder='big'): 10**20 }
    },
}

klass = chains.base.MiningChain.configure(
    __name__='TestChain',
    vm_configuration=(
        (constants.GENESIS_BLOCK_NUMBER, Simple3VM),
    )
)

chain = klass.from_genesis(AtomicDB(), GENESIS_PARAMS, GENESIS_STATE)

######### Tx1 ###########################
# nonce = vm.get_transaction_nonce(SENDER)
vm = chain.get_vm()
sender_nonce = vm.state.get_nonce(SENDER)

print("BLOCK0(Genesis) SENDER BALANCE : {}".format(vm.state.get_balance(SENDER)))
print("BLOCK0(Genesis) RECEIVER BALANCE : {}".format(vm.state.get_balance(RECEIVER)))

tx1 = vm.create_unsigned_transaction(
    nonce=sender_nonce,
    gas_price=100,
    gas=100000,
    to=RECEIVER,
    value=10,
    data=b'',
)

signed_tx1 = tx1.as_signed_transaction(SENDER_PRIVATE_KEY)

chain.apply_transaction(signed_tx1)

# We have to finalize the block first in order to be able read the
# attributes that are important for the PoW algorithm
block_result = chain.get_vm().finalize_block(chain.get_block())
block = block_result.block

# based on mining_hash, block number and difficulty we can perform
# the actual Proof of Work (PoW) mechanism to mine the correct
# nonce and mix_hash for this block
nonce, mix_hash = mine_pow_nonce(
    block.number,
    block.header.mining_hash,
    block.header.difficulty
)

block = chain.mine_block(mix_hash=mix_hash, nonce=nonce)

print("BLOCK1 SENDER BALANCE : {}".format(vm.state.get_balance(SENDER)))
print("BLOCK1 RECEIVER BALANCE : {}".format(vm.state.get_balance(RECEIVER)))

######### Tx2 ###########################
# nonce = vm.get_transaction_nonce(SENDER)
vm = chain.get_vm()
sender_nonce = vm.state.get_nonce(SENDER)

tx2 = vm.create_unsigned_transaction(
    nonce=sender_nonce,
    gas_price=100,
    gas=21000,
    to=RECEIVER,
    value=to_wei(1, 'ether'),
    data=b'',
)

signed_tx2 = tx2.as_signed_transaction(SENDER_PRIVATE_KEY)

chain.apply_transaction(signed_tx2)

# We have to finalize the block first in order to be able read the
# attributes that are important for the PoW algorithm
block_result = chain.get_vm().finalize_block(chain.get_block())
block = block_result.block

# based on mining_hash, block number and difficulty we can perform
# the actual Proof of Work (PoW) mechanism to mine the correct
# nonce and mix_hash for this block
nonce, mix_hash = mine_pow_nonce(
    block.number,
    block.header.mining_hash,
    block.header.difficulty
)

block = chain.mine_block(mix_hash=mix_hash, nonce=nonce)
vm = chain.get_vm()

def send_dummy_tx(chain):
    vm = chain.get_vm()
    sender_nonce = vm.state.get_nonce(SENDER)
    tx = vm.create_unsigned_transaction(
        nonce=sender_nonce,
        gas_price=0,
        gas=21000,
        to=RECEIVER,
        value=0,
        data=b'',
    )
    signed_tx = tx.as_signed_transaction(SENDER_PRIVATE_KEY)
    chain.apply_transaction(signed_tx)
    block_result = chain.get_vm().finalize_block(chain.get_block())
    block = block_result.block

    nonce, mix_hash = mine_pow_nonce(
        block.number,
        block.header.mining_hash,
        block.header.difficulty
    )

    block = chain.mine_block(mix_hash=mix_hash, nonce=nonce)

print(f"block: {block}")

send_dummy_tx(chain)
send_dummy_tx(chain)
send_dummy_tx(chain)

print("BLOCK2 SENDER BALANCE : {}".format(vm.state.get_balance(SENDER)))
print("BLOCK2 RECEIVER BALANCE : {}".format(vm.state.get_balance(RECEIVER)))
