from uagents.setup import fund_agent_if_low
from uagents import Agent, Context, Protocol

# create an agent with port and endpoint
capovila = Agent(
    name="capovila",
    port=8000,
    seed="capovila secret phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)

# check if has enough tokens to keep with code
fund_agent_if_low(capovila.wallet.address())

# after connect, print some text
@capovila.on_interval(period=3)
async def hi(ctx: Context):
    ctx.logger.info("Hello")

# run agent, registering on Almanac
capovila.run()

# NOTE

# fund_agent_if_low is a class, that checks if you have enough token

# if it does -> register in the Almanac contract
# if it doesn't -> will add testnet tokens to your Fetch netwok address

# we need to create an agent with more detils now, passing port and url
# these are used to others agents see you and be able to interact with you

# FLOW:

# run
# start registration process automatically
# checks agent's balance and funded if needed
# try to register on the Almanac contract
# then will be ready to start to a remote communication with other agents registered

