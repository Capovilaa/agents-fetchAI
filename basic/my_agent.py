from uagents import Agent, Context

# create an agent
capovila = Agent(name="capovila", seed="capovila recovery phrase")

# when it starts, show at screen some info from agent
@capovila.on_event("startup")
async def introduce_agent(ctx: Context):
    ctx.logger.info(f"Hello, I'm agent {ctx.name} and my address is {ctx.address}.")
 
if __name__ == "__main__":
    capovila.run()
    
# NOTE
# ctx: Context is very important to agent access infos from him, we can instance to get data like name and address