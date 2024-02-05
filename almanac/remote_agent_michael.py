from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

# message struct
class Message(Model):
    message: str

# create michael agent
michael = Agent(
    name="michael",
    port=8001,
    seed="michael secret phrase",
    endpoint=["http://127.0.0.1:8001/submit"],
)

# make sure that has enough tokens
fund_agent_if_low(michael.wallet.address()) 

# create a behavior to receive and send messages
@michael.on_message(model=Message)
async def message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")
 
    # we're using sender as address
    await ctx.send(sender, Message(message="hello there capovila"))
 
if __name__ == "__main__":
    michael.run()
    
# NOTE

# we're using 2 files to interact with each other to send messages
# is the same flow from the local messages, but now we need to define port and url

# start michael first, because michael only will send message when it receive