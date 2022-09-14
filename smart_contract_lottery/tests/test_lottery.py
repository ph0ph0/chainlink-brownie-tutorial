# Current price is 1106.21 dollars 2022_06_23
# Therefore, our getEntryFee function should return:
# 50 / 1106.21 ~= 0.0451 = 004510000000000000 wei
from scripts.utils import get_account
from brownie import Lottery, network, accounts, config
import pytest
import web3 from Web3

test_get_entry_fee(): 
    account = accounts[0]
    lottery_contract = lottery.deploy(config["networks"][network.showActive()]["eth_usd_price_feed"], {"from": account})
    entry_fee = lottery_ contract.getEntryFee()
    assert entry_fee > web3.toWei(0.04, 'ether')
    assert entry_fee < web3.toWei(0.05, 'ether')
    