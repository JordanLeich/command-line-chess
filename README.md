# Description :exclamation:
- Command-line chess game (also supports the UCI protocol - plays random moves)

# Instructions :zap:
1. Run chess.py to play.
2. Use this format to move on the chess board: e2e4, e7e5, e1g1, a7a8q, etc.

## UCI Information :pencil:
* uci.py and engine.py are the files used for implementing the UCI (Universal Chess Interface) protocol.
* run uci.py to start the engine.
* For connecting it to a GUI like SCID or Arena, make uci.py executable or create a shell script to run uci.py, and select that as the engine in the GUI.
* Since it follows the UCI protocol, it can also be connected to the chess playing website Lichess.
