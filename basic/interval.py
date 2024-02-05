from uagents import Agent, Context

# create an agent
capovila = Agent(name='capovila', seed='capovila recovery phrase')

# show a message every 2 seconds
@capovila.on_interval(period=2.0)
async def say_hello(ctx: Context):
    ctx.logger.info(f'hello, my name is {ctx.name}')

if __name__ == '__main__':
    capovila.run()
    
    
# NOTE

# this file use "on_interval" to set a time to keep running the task
# has the same function from "agent" file