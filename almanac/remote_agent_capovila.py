from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

# message struct
class Message(Model):
    message: str

# who's sendind    
RECIPIENT_ADDRESS = "agent1qten9tnnafq3fhc0x3ruudjgxr5azg0rz0cmj4mpm5gyyuh9fz0k5w23pxz"

# create capovila's agent
capovila = Agent(
    name="capovila",
    port=8000,
    seed="capovila secret phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)

# make sure that has enough token
fund_agent_if_low(capovila.wallet.address())

# create a behavior to capovila send messages
@capovila.on_interval(period=2)
async def send_message(ctx: Context):
    await ctx.send(RECIPIENT_ADDRESS, Message(message='Hello there michael'))
    
# create a behavior to capovila receive messages
@capovila.on_message(model=Message)
async def receive_message(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f'Received message {sender} : {msg.message}')
    
if __name__ == '__main__':
    capovila.run()
    
# NOTE

# we're using 2 files to interact with each other to send messages
# is the same flow from the local messages, but now we need to define port and url

# start michael first, because michael only will send message when it receive