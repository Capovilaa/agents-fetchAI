from datetime import datetime
from pytz import utc
 
from tortoise import Tortoise

# import protocols
from protocols.cleaning import cleaning_proto
from protocols.cleaning.models import Availability, Provider, Service, ServiceType
 
from uagents import Agent, Context
from uagents.setup import fund_agent_if_low

# create cleaner agent
cleaner = Agent(
    name="cleaner",
    port=8001,
    seed="cleaner secret phrase",
    endpoint={
        "http://127.0.0.1:8001/submit": {},
    },
)

# check cleaner's balance
fund_agent_if_low(cleaner.wallet.address())
 
# build the cleaning service agent from the cleaning protocol
cleaner.include(cleaning_proto)

# when cleaner is created
@cleaner.on_event("startup")
async def startup(_ctx: Context):
    
    # prepares sql to work wirh models
    # manage database connections and schema generation for the agent's data models
    await Tortoise.init(
        db_url="sqlite://db.sqlite3", modules={"models": ["protocols.cleaning.models"]}
    )
    
    # generate schemas
    await Tortoise.generate_schemas()
 
    # create an instance and populates with data
    provider = await Provider.create(name=cleaner.name, location="London Kings Cross")
 
    # prepare and create 3 services instances
    floor = await Service.create(type=ServiceType.FLOOR)
    window = await Service.create(type=ServiceType.WINDOW)
    laundry = await Service.create(type=ServiceType.LAUNDRY)
 
    # the instances are associated with the provider,
    # this establishes a relationship between providers and the services they offer    
    await provider.services.add(floor)
    await provider.services.add(window)
    await provider.services.add(laundry)
 
    # definines an Availability instance to represent the availability of the
    # cleaning service provider, it includes details 
    await Availability.create(
        provider=provider,
        time_start=utc.localize(datetime.fromisoformat("2022-01-31 00:00:00")),
        time_end=utc.localize(datetime.fromisoformat("2023-05-01 00:00:00")),
        max_distance=10,
        min_hourly_price=5,
    )

# when it ends, close all connections
@cleaner.on_event("shutdown")
async def shutdown(_ctx: Context):
    await Tortoise.close_connections()
 
if __name__ == "__main__":
    cleaner.run()