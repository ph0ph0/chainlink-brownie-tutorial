from scripts.utils import get_account
from brownie import FundMe, config, network


def fund():
    fund_me_contract = FundMe[-1]
    account = get_account()
    entrance_fee = fund_me_contract.getEntranceFee()
    print(f"The current entrance fee is {entrance_fee}")
    fund_me_contract.fund({"from": account, "value": entrance_fee})
    print(f"Account {account} funded {entrance_fee}")


def withdraw():
    fund_me_contract = FundMe[-1]
    account = get_account()
    fund_me_contract.withdraw({"from": account})
    print(f"{account} withdrew from FundMe contracts")


def main():
    fund()
    withdraw()
