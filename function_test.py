from web3 import Web3

bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))
sender_address = '0xA2D5bEE214213ec4BBb94447ce6A84059715c03B'

balance = web3.eth.get_balance(sender_address)
humanReadable = web3.fromWei(balance,'ether')
gas = web3.eth_estimateGas()
print(gas)
print("Balance: ", humanReadable)