import hashlib
from uagents import Agent, Bureau, Context, Model
from uagents.crypto import Identity
 
class Message(Model):
    message: str # message text
    digest: str # hash of message SHA-256
    signature: str # private key from who sent message

# this function is used to hash a string message
# using the SHA-256 algorithm and return the resulting digest as bytes
def encode(message: str) -> bytes:
    hasher = hashlib.sha256()
    hasher.update(message.encode())
    return hasher.digest()

# create 2 agents
capovila = Agent(name="capovila", seed="capovila recovery password")
michael = Agent(name="michael", seed="michael recovery password")

# in each 3 seconds, capovila will send a message to michael
@capovila.on_interval(period=3.0)
async def send_message(ctx: Context):
    msg = "hello there michael"
    digest = encode(msg)    
    await ctx.send(
        michael.address,
        Message(message=msg, digest=digest.hex(), signature=capovila.sign_digest(digest)),
    )
    
# takes care when capovila receives a message of type "Message"
@capovila.on_message(model=Message)
async def capovila_rx_message(ctx: Context, sender: str, msg: Message):
    
    # assert do a verification, if it's not true, show an assertError message
    assert Identity.verify_digest(
        sender, bytes.fromhex(msg.digest), msg.signature
    ), "couldn't verify michael's message"
    
    # after pass assert, show the message in the log
    ctx.logger.info("michael's message verified!")
    ctx.logger.info(f"Received message from {sender}: {msg.message}")
    
# takes care when michael receives a message of type "Message"
@michael.on_message(model=Message)
async def michael_rx_message(ctx: Context, sender: str, msg: Message):
    
    # assert do a verification, if it's not true, show an assertError message
    assert Identity.verify_digest(
        sender, bytes.fromhex(msg.digest), msg.signature
    ), "couldn't verify capovila's message"
 
    # after pass assert, show the message in the log
    ctx.logger.info("capovila's message verified!")
    ctx.logger.info(f"Received message from {sender}: {msg.message}")
 
    # send a message back to capovila
    msg = "hello there capovila"
    digest = encode(msg)
    await ctx.send(
        capovila.address,
        Message(message=msg, digest=digest.hex(), signature=michael.sign_digest(digest)),
    )

# bereau to both agents run together
bureau = Bureau()
bureau.add(capovila)
bureau.add(michael)
 
if __name__ == "__main__":
    bureau.run()