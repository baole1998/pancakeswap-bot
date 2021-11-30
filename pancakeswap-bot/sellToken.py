from web3 import Web3
import json
import time
from wallet_infor import bao_elemon_wallet_address, bao_elemon_wallet_private_key
from pancakeswap_contract import panabi, panRouterContractAddress, sellabi
from tokenContractsList import iTAM, usdt

bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))

print(web3.isConnected())

spend = web3.toChecksumAddress("0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c")  #WBNB Address
 
#Contract id is the new token we are swaping to
# contract_id = web3.toChecksumAddress(input("Enter the Contract Address of token you want to sell: "))

# Import token contract from tokenContractsList.py
contract_id = web3.toChecksumAddress(usdt)
 
#Setup the PancakeSwap contract
contract = web3.eth.contract(address=panRouterContractAddress, abi=panabi)

#Create token Instance for Token
sellTokenContract = web3.eth.contract(contract_id, abi=sellabi)

#Get Token Balance
balance = sellTokenContract.functions.balanceOf(bao_elemon_wallet_address).call()
symbol = sellTokenContract.functions.symbol().call()
readable = web3.fromWei(balance,'ether')
print("Balance: " + str(readable) + " " + symbol)

#Enter amount of token to sell
tokenValue = web3.toWei(input("Enter amount of " + symbol + " you want to sell: "), 'ether')

#Approve Token before Selling
tokenValue2 = web3.fromWei(tokenValue, 'ether')
start = time.time()
approve = sellTokenContract.functions.approve(panRouterContractAddress, balance).buildTransaction({
            'from': bao_elemon_wallet_address,
            'gasPrice': web3.toWei('5','gwei'),
            'nonce': web3.eth.get_transaction_count(bao_elemon_wallet_address),
            })

signed_txn = web3.eth.account.sign_transaction(approve, private_key=bao_elemon_wallet_private_key)
tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
print("Approved: " + web3.toHex(tx_token))

#Wait after approve 10 seconds before sending transaction
time.sleep(10)
print(f"Swapping {tokenValue2} {symbol} for BNB")


#Swaping exact Token for ETH (BNB)
pancakeswap2_txn = contract.functions.swapExactTokensForETH(
            tokenValue ,0, 
            [contract_id, spend],
            bao_elemon_wallet_address,
            (int(time.time()) + 1000000)

            ).buildTransaction({
            'from': bao_elemon_wallet_address,
            'gasPrice': web3.toWei('10','gwei'),
            'nonce': web3.eth.get_transaction_count(bao_elemon_wallet_address),
            })
    
signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=bao_elemon_wallet_private_key)
tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
print(f"Sold {symbol}: " + web3.toHex(tx_token))