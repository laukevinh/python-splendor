# python-splendor
The Splendor board game adapted to the python interpreter

Start a new game with 

    G = Game()

See the board

    G.board()

Collect coins for player 0

    G.collect((1, 1, 1, 0, 0, 0))
    
Buy the card on bottom row, first position

    G.buy(0,0)
    
Get the active player

    G.ap()
    
Check what cards and how many coins the AP possesses

    G.ap().cards()
    G.ap().wallet()
