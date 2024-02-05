# necessary imports
from uagents import Agent, Context

# create an agent
# name to identify the agent
# seed to others agents interact with this one
capovila = Agent(name='capovila', seed='capovila recovery phrase')

# agent will execute "say_hello" when it starts
@capovila.on_event("startup")
async def say_hello(ctx: Context):
    
    # print a message
    ctx.logger.info(f'hello, my name is {ctx.name}')

if __name__ == '__main__':
    capovila.run()
    
# NOTE

# my first agent, this one can show on console his name
# an "event" was created to call a function when it starts
# allways use async functions
# "Context" is a list of functions

# this create a data json file that storages the current value
# if this file wasn't excluded, the counter won't be 0