from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Install solcx version
install_solc("0.6.0")

# Compile our solidity

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)
print(compiled_sol)

with open("compiled_code.sol", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

print(abi)

# For connecting to ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))
chain_id = 1337
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"

private_key = os.getenv("PRIVATE_KEY")
print(private_key)

# For connecting to rinkeby or göerli testnet
# Go to Infura to get your url
w3 = Web3(
    Web3.HTTPProvider("https://goerli.infura.io/v3/e9dee0df9ea5418f91b6e8598a81ae83")
)
# Chain id can be found at https://chainlist.org/
chain_id = 420
# Won't use my real address and private key - below is the ganache one
# I have used all of my Rinkeby faucets and dont want to risk exposing keys
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
print(SimpleStorage)
# Get the latest transaction count for the nonce
nonce = w3.eth.getTransactionCount(my_address)
print(nonce)
# 1. Build a tx
# 2. Sign a tx
# 3. Send a tx

# 1.
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)
print(transaction)

# 2. Since we are sending the tx from our address, we must use our pK to sign it.
signed_tx = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print(signed_tx)

# 3. Send this signed tx. After running the script, if we go to the transactions pane of ganache we should now see
# our tx
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
# This pauses our code until the tx seals.
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# ---Working with the Contract---

# When working with the contract, there are always two things that you need.
# * Contract address
# * Contract ABI (You can often just google a contracts ABI and get it off GH)

# This creates an interface that we can use to interact with our smart contract
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# When interacting with the BC, there are two ways we can do this:
# * Call -> Simulates making the call and getting a return value, but can also be used to read state.
# * Transact -> Used to modify state.
# Now we can call functions in our s.c
print("favourite number", simple_storage.functions.retrieveFavouriteNumber().call())

# Notice how if we print the call from below, we are only simulating the transaction.
# We set the value for favourite number, and the value is returned, but it is simualted
# so we aren't actually updating the state of the blockchain.
print("simulated transaction call", simple_storage.functions.store(15).call())
print(
    "fav number is still 0: ", simple_storage.functions.retrieveFavouriteNumber().call()
)

# -build tx to modify state-
store_tx = simple_storage.functions.store(15).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
signed_store_tx = w3.eth.account.sign_transaction(store_tx, private_key=private_key)
send_store_tx = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
# Now if we check in Ganache we will see our tx
print(
    "updated favourite number state to",
    simple_storage.functions.retrieveFavouriteNumber().call(),
)

# To run ganache-cli with the same pK's, use `ganache-cli --deterministic`
