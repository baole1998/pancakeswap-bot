from web3 import Web3
from wallet_infor import my_private_key, sender_address
from pancakeswap_contract import panabi, panRouterContractAddress
import time

bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))

print(web3.isConnected())

balance = web3.eth.get_balance(sender_address)
# print("Wallet Blance: ", balance)
 
humanReadable = web3.fromWei(balance,'ether')
print("Wallet Blance: ", humanReadable)
 
#Contract Address of Token we want to buy
tokenToBuy = web3.toChecksumAddress(input("Enter TokenAddress: "))            #web3.toChecksumAddress("contract")

spend = web3.toChecksumAddress("0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c")  #wbnb contract
 
#Setup the PancakeSwap contract
contract = web3.eth.contract(address=panRouterContractAddress, abi=panabi)


nonce = web3.eth.get_transaction_count(sender_address)
 
start = time.time()

pancakeswap2_txn = contract.functions.swapExactETHForTokens(
10000000000, # set to 0, or specify minimum amount of tokeny you want to receive - consider decimals!!!
[spend,tokenToBuy],
sender_address,
(int(time.time()) + 10000)
).buildTransaction({
'from': sender_address,
'value': web3.toWei(0.001,'ether'),#This is the Token(BNB) amount you want to Swap from
'gas': 150000,
'gasPrice': web3.toWei('5','gwei'),
'nonce': nonce,
})
    
signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=my_private_key)
tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
print("Transaction Success !!! ", web3.toHex(tx_token))