
transaction = web3.eth.getTransaction('0x2937393f947e449aaf6bae64d168ca9e380f4cc6670c8f95d5aed05b8e43fd6b');
print("Transaction", transaction)
print("Wallet Blance: ", balance)

humanReadable = web3.fromWei(balance,'ether')
print("Wallet Blance: ", humanReadable)

#Contract Address of Token we want to buy
tokenToBuy = web3.toChecksumAddress(input("Enter TokenAddress: "))            #web3.toChecksumAddress("contract")

spend = web3.toChecksumAddress("0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c")  #wbnb contract

#Setup the PancakeSwap contract
contract = web3.eth.contract(address=panRouterContractAddress, abi=panabi)

print('contract' , contract)
print('functions' , contract.functions)
allFunctions = contract.functions

print('get function', allFunctions.DOMAIN_SEPARATOR())
# print('nonce' , nonce)
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
