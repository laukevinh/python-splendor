from main import CollectError
from main import Bank
from main import Wallet
from main import Card
from main import Game
from main import Noble

if __name__ == "__main__":
    B = Bank(5)
    assert(len(B) == 30)
    B.give((1,0,0,0,0,0))
    assert(len(B) == 29)
    B.give((0,5,0,0,0,0))
    assert(len(B) == 24)
    catch_error = False
    try:
        B.give((0,0,6,0,0,0))
    except CollectError:
        catch_error = True
    assert(catch_error is True)
    B.take((1,5,0,0,0,0))
    assert(len(B) == 30)
    assert(B[0] == 5)

if __name__ == "__main__":
    W = Wallet()
    W += (1,2,3,4,0,0)
    assert(len(W) == 10)
    W -= (1,2,0,0,0,0)
    assert(len(W) == 7)
    assert(W[2] == 3)
    W += (4,4,1,0,0,0)
    assert(W.overmax())
    W -= (4,4,4,4,0,0)
    assert(W.negative() is False)
    
if __name__ == "__main__":
    _BLACK = 4
    C = Card(_BLACK,0,1,1,1,1,0)
    assert(C.cost() == (1,1,1,1,0))
    assert(C.color() == 'B')
    assert(C.points() == 0)
    C.set_key(0,3)
    assert(C.key() == (0, 3))

if __name__ == "__main__":
    G = Game()
    P1 = G.active_player()
    G.collect((1,1,1,0,0,0))
    P2 = G.active_player()
    assert(P2 is not P1)
    G.collect((0,1,1,1,0,0))
    G.board()

if __name__ == "__main__":
    N = Noble(3, 3, 3, 3, 0, 0)
    assert(N.cost() == (3, 3, 3, 0, 0))
