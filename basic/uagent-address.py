from uagents import Agent

# create an agent
capovila = Agent(name="capovila", seed="capovila recovery phrase")
 
# print agent's address
print("uAgent address: ", capovila.address)

# print agent's network address
print("Fetch network address: ", alice.wallet.address())

# NOTE
# this agent can show on console the agent address
# it has 2 kinds of address:

# uAgent address : main agent identifier, other agents can access this see these agent's data in the Almanac contract
# Fetch network address : will be able to interact with Fetcher ledger

# uAgent -> where all the others agents will find and interact with you
# Fetch ledger is like a record book with all transactions that happens across network 