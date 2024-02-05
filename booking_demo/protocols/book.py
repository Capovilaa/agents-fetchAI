from uagents import Context, Model, Protocol
 
from .query import TableStatus

# this represents the request to book a table
class BookTableRequest(Model):
    table_number: int
    time_start: int
    duration: int
 
# his contains the response to the table booking request.
# It includes a boolean attribute success, indicating whether the booking was successful or not
class BookTableResponse(Model):
    success: bool
 
book_proto = Protocol()

# when book_proto receive a message
@book_proto.on_message(model=BookTableRequest, replies=BookTableResponse)
async def handle_book_request(ctx: Context, sender: str, msg: BookTableRequest):
    
    # get all tables from storage
    tables = {
        int(num): TableStatus(**status)
        for (
            num,
            status,
        ) in ctx.storage._data.items()
        if isinstance(num, int)
    }
    
    # get exactly table by parameter
    table = tables[msg.table_number]
 
    if (
        table.time_start <= msg.time_start
        and table.time_end >= msg.time_start + msg.duration
    ):
        # if attends requirements, set and return true (success)
        
        success = True
        table.time_start = msg.time_start + msg.duration
        ctx.storage.set(msg.table_number, table.dict())
    else:
        
        # if it doesn't, return false (not success)
        success = False
 
    # send the response
    await ctx.send(sender, BookTableResponse(success=success))