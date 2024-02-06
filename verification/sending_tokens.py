from uagents import Agent, Bureau, Context, Model
from uagents.network import wait_for_tx_to_complete
from uagents.setup import fund_agent_if_low

# payment struct
class PaymentRequest(Model):
    wallet_address: str
    amount: int
    denom: str

# transaction struct (after payment)
class TransactionInfo(Model):
    tx_hash: str

# data to be send
AMOUNT = 100
DENOM = "atestfet"

# create agents
capovila = Agent(name="capovila", seed="capovila secret phrase")
michael = Agent(name="michael", seed="michael secret phrase")

# verify both agents to keep going
fund_agent_if_low(michael.wallet.address())
fund_agent_if_low(capovila.wallet.address())

# in every 10 seconds request for funds
@capovila.on_interval(period=10.0)
async def request_funds(ctx: Context):
    
    # send to michael a request for 100 tokens
    await ctx.send(
        michael.address,
        PaymentRequest(
            wallet_address=str(ctx.wallet.address()), amount=AMOUNT, denom=DENOM
        ),
    )

# after request (when michael send back tokens)
@capovila.on_message(model=TransactionInfo)
async def confirm_transaction(ctx: Context, sender: str, msg: TransactionInfo):
    
    # show that received
    ctx.logger.info(f"Received transaction info from {sender}: {msg}")
    
    # wait for transaction be done by complete (passing parameters)
    tx_resp = await wait_for_tx_to_complete(msg.tx_hash, ctx.ledger)
    # ctx.logger.info(f"tx_resp : {tx_resp}") # get info from transaction
 
    # after transaction done, checks if sender match
    coin_received = tx_resp.events["coin_received"]
    if (
        coin_received["receiver"] == str(ctx.wallet.address())
        and coin_received["amount"] == f"{AMOUNT}{DENOM}"
    ):
        ctx.logger.info(f"Transaction was successful: {coin_received}")

# when michael receive a request by capovila
@michael.on_message(model=PaymentRequest, replies=TransactionInfo)
async def send_payment(ctx: Context, sender: str, msg: PaymentRequest):
    ctx.logger.info(f"Received payment request from {sender}: {msg}")
 
    # send the payment
    # method. It takes the wallet address (msg.wallet_address),
    # amount (msg.amount), denomination (msg.denom), and ctx.wallet()
    # as parameters. This method is responsible for sending the requested payment.
    transaction = ctx.ledger.send_tokens(
        msg.wallet_address, msg.amount, msg.denom, ctx.wallet
    )
 
    # send the tx hash so capovila can confirm
    await ctx.send(capovila.address, TransactionInfo(tx_hash=transaction.tx_hash))

# bereau to both agents run together
bureau = Bureau()
bureau.add(capovila)
bureau.add(michael)
 
if __name__ == "__main__":
    bureau.run()