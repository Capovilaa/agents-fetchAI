from typing import List
 
from uagents import Context, Model, Protocol

# this represents the status of a table and includes attributes
class TableStatus(Model):
   seats: int
   time_start: int
   time_end: int
 
# his is used for querying table availability
class QueryTableRequest(Model):
   guests: int
   time_start: int
   duration: int
 
# this contains the response to the query table availability
class QueryTableResponse(Model):
   tables: List[int]

# this is used to request the total number of queries made to the system
class GetTotalQueries(Model):
   pass

# this contains the response to the total queries request, including the count of total queries made to the system 
class TotalQueries(Model):
   total_queries: int

# create protocol instance
query_proto = Protocol()

# when it receive a query
@query_proto.on_message(model=QueryTableRequest, replies=QueryTableResponse)

# processes the table availability query based on the provided parameters, checks the table
# statuses stored in the agent's storage, and sends the available table numbers as a response
async def handle_query_request(ctx: Context, sender: str, msg: QueryTableRequest):
    
    # all tables
    tables = {
        int(num): TableStatus(**status)
        for (
            num,
            status,
        ) in ctx.storage._data.items()
        if isinstance(num, int)
    }
 
    available_tables = []
    
    # check number and status availability that came by parameter
    for number, status in tables.items():
        if (
            status.seats >= msg.guests
            and status.time_start <= msg.time_start
            and status.time_end >= msg.time_start + msg.duration
        ):
            # if atends requirements, appen to list
            available_tables.append(int(number))
 
    # show available tables
    ctx.logger.info(f"Query: {msg}. Available tables: {available_tables}.")
 
    # send back to sender available tables
    await ctx.send(sender, QueryTableResponse(tables=available_tables))
 
    # increments on total_queries
    total_queries = int(ctx.storage.get("total_queries") or 0)
    ctx.storage.set("total_queries", total_queries + 1)

# when on query, gets total queries and return it
@query_proto.on_query(model=GetTotalQueries, replies=TotalQueries)
async def handle_get_total_queries(ctx: Context, sender: str, _msg: GetTotalQueries):
    total_queries = int(ctx.storage.get("total_queries") or 0)
    await ctx.send(sender, TotalQueries(total_queries=total_queries))