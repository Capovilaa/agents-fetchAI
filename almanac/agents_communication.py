from uagents import Agent, Bureau, Context, Model

# define message struct (only string messages)
class Message(Model):
    message: str
    
# agents that will comunnicate with each other
capovila = Agent(name='capovila', seed='capovila recovery phrase')
michael = Agent(name='michael', seed='micahel recovery phrase')

# capovila will send a message to michael in every 3 seconds
@capovila.on_interval(period=3)
async def send_message(ctx: Context):
    
    # send (to, message)
    await ctx.send(michael.address, Message(message="Hello there michael"))
    
# capovila will receive a message and show it
# this is called every time that micahel receive a message of type "Message"
@capovila.on_message(model=Message)
async def capovila_message_handler(ctx: Context, sender: str, msg: Message):
    
    # print message
    ctx.logger.info(f'Received message from {sender} : {msg.message}')
    
# create a behavior that wait for messages
@michael.on_message(model=Message)
async def michael_message_handler(ctx: Context, sender: str, msg: Message):
    
    # print message
    ctx.logger.info(f"Received message from {sender} : {msg.message}")
    
    # send message
    await ctx.send(capovila.address, Message(message="Hello there capovila"))
    
# create a bureu (escritório) to allow us to run agents together in the same script
bureau = Bureau()

# add agents
bureau.add(capovila)
bureau.add(michael)

if __name__ == '__main__':
    bureau.run()
    
# NOTE

# this file allow us to interact with 2 agents locally, they can send messages to each other
# when it's runned, capovila will send a message to michael, this last will receive and send another one
# remember to allways use await

# FLOW

# create message struct
# create agents
# define behaviors from each agent
# create an enviroment (bureau) to run agents together in the same script
# run bureau