# SlimcoinTxBot
Requires Python 3 and slimcoind daemon with RPC interface enabled.

## Configuration
Most of the configuration to the bot needs to be done via edits to
the code, the only CLI parameters accepted and required are, username
and password for the RPC interface. Supported features are:

- Set destination address
- Random amount within a set range
- Sleep by a random amount within a range
- Stop after n transactions
- Stop when the account balance hits x amount
