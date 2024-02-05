from uagents import Agent, Context

# create an agent
capovila = Agent(name="capovila", seed="capovila recovery phrase")

# in every second get "count" from storage, show and updete it
@capovila.on_interval(period=1.0)
async def on_interval(ctx: Context):
    
    # get from storage
    current_count = ctx.storage.get("count") or 0
    
    # show current counter
    ctx.logger.info(f"My count is: {current_count}")
 
    # increase by 1 (set to storage)
    ctx.storage.set("count", current_count + 1)
    
if __name__ == '__main__':
    capovila.run()
    
# NOTE

# this a demo to show get and set functions
# get and set were used with a "storage" prefix