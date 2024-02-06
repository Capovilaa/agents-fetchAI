from datetime import datetime, timedelta
from typing import List
 
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
 
from uagents import Context, Model, Protocol
from .models import Provider, Availability, User

# protocol features
PROTOCOL_NAME = "cleaning"
PROTOCOL_VERSION = "0.1.0"


# messages structs
class ServiceRequest(Model):
    user: str
    location: str
    time_start: datetime
    duration: timedelta
    services: List[int]
    max_price: float
 
class ServiceResponse(Model):
    accept: bool
    price: float
 
class ServiceBooking(Model):
    location: str
    time_start: datetime
    duration: timedelta
    services: List[int]
    price: float
 
class BookingResponse(Model):
    success: bool

# create a protocol
cleaning_proto = Protocol(name=PROTOCOL_NAME, version=PROTOCOL_VERSION)

# this function will return if service is in range (accessable)
# this function also use a libraty to check it
def in_service_region(
    location: str, availability: Availability, provider: Provider
) -> bool:
    
    # create an instance to access latitude and longitude
    geolocator = Nominatim(user_agent="micro_agents")
 
    # get user and cleaner location
    user_location = geolocator.geocode(location)
    cleaner_location = geolocator.geocode(provider.location)
 
    # validations
    if user_location is None:
        raise RuntimeError(f"user location {location} not found")
 
    if cleaner_location is None:
        raise RuntimeError(f"provider location {provider.location} not found")
 
    # set cleaner and user coordinates
    cleaner_coordinates = (cleaner_location.latitude, cleaner_location.longitude)
    user_coordinates = (user_location.latitude, user_location.longitude)
    
    # set distance and check if is on range
    service_distance = geodesic(user_coordinates, cleaner_coordinates).miles
    in_range = service_distance <= availability.max_distance
 
    return in_range

# when cleaning protocol receive a request
@cleaning_proto.on_message(model=ServiceRequest, replies=ServiceResponse)
async def handle_query_request(ctx: Context, sender: str, msg: ServiceRequest):
    
    # set some data came by ctx
    # will search on models by the parameter past
    provider = await Provider.filter(name=ctx.name).first()
    availability = await Availability.get(provider=provider)
    services = [int(service.type) for service in await provider.services]
    markup = provider.markup
 
    # get or create a user instance based on the user's name and sender address
    user, _ = await User.get_or_create(name=msg.user, address=sender)
    
    # calculates the message duration in hours
    msg_duration_hours: float = msg.duration.total_seconds() / 3600
    ctx.logger.info(f"Received service request from user `{user.name}`")
 
    # validations to check service can be accepted
    if (
        set(msg.services) <= set(services)
        and in_service_region(msg.location, availability, provider)
        and availability.time_start <= msg.time_start
        and availability.time_end >= msg.time_start + msg.duration
        and availability.min_hourly_price * msg_duration_hours < msg.max_price
    ):
        
        # set service available
        accept = True
        price = markup * availability.min_hourly_price * msg_duration_hours
        ctx.logger.info(f"I am available! Proposing price: {price}.")
    else:
        
        # set service not available
        accept = False
        price = 0
        ctx.logger.info("I am not available. Declining request.")
 
    # response to sender (if was accepted and price)
    await ctx.send(sender, ServiceResponse(accept=accept, price=price))

# when cleaning protocol receive a booking
@cleaning_proto.on_message(model=ServiceBooking, replies=BookingResponse)
async def handle_book_request(ctx: Context, sender: str, msg: ServiceBooking):
    
    # set fields to be book
    provider = await Provider.filter(name=ctx.name).first()
    availability = await Availability.get(provider=provider)
    services = [int(service.type) for service in await provider.services]
 
    user = await User.get(address=sender)
    msg_duration_hours: float = msg.duration.total_seconds() / 3600
    ctx.logger.info(f"Received booking request from user `{user.name}`")
 
    # if these verifications is true, set success to true, istead of, set to false
    success = (
        set(msg.services) <= set(services)
        and availability.time_start <= msg.time_start
        and availability.time_end >= msg.time_start + msg.duration
        and msg.price <= availability.min_hourly_price * msg_duration_hours
    )
 
    if success:
        
        # uptade availability
        availability.time_start = msg.time_start + msg.duration
        await availability.save()
        ctx.logger.info("Accepted task and updated availability.")
 
    # send the response
    await ctx.send(sender, BookingResponse(success=success))