from typing import List
 
from uagents import Context, Model, Protocol

# structs

class TableStatus(Model):
   seats: int
   time_start: int
   time_end: int
 
class QueryTableRequest(Model):
   guests: int
   time_start: int
   duration: int
 
class QueryTableResponse(Model):
   tables: List[int]
 
class GetTotalQueries(Model):
   pass
 
class TotalQueries(Model):
   total_queries: int
 
query_proto = Protocol()