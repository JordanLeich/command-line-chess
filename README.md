# command-line-chess
* chess.py and ui.py are the files for command-line chess.
* run chess.py to play.
* move format - <from square><to square><optional promotion piece>
* eg: e2e4
      e7e5
      e1g1
      a7a8q

* uci.py and engine.py are the files used for implementing the
  UCI(Universal Chess Interface) protocol.
* run uci.py to start the engine.

* For connecting it to a GUI like SCID or Arena, make uci.py executable
  or create a shell script to run uci.py, and select that as the
  engine in the GUI.

* Since it follows the UCI protocol, it can also be connected to the
  chess playing website Lichess.
