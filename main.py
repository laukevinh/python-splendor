class CollectError(Exception):
    pass

class Game:
    _WHITE = 0
    _BLUE = 1
    _GREEN = 2
    _RED = 3
    _BLACK = 4
    _WILD = 5
    _MAX_BANK_COINS = (None, None, 4, 5, 7)
    _MAX_NOBLEMEN = (None, None, 3, 4, 5)
    _MAX_RESERVE = 3
    _REG_COLLECT = 3
    _DBL_COLLECT = 2
    _CARDS_PER_LEVEL = 4
    _MAX_LEVELS = 3

    def __init__(self, num_players=2, points_to_win=21, max_time=5, display=None):
        self._n = num_players
        self._player = 0
        self._players = [Player(i) for i in range(self._n)]
        self._points_to_win = points_to_win
        self._max_time = max_time
        self._bank = Bank(Game._MAX_BANK_COINS[self._n])
        self._decks = self._new_decks()
        self._board = self._new_board(self._decks)
        self._display = display
        self._noblemen = self._fill_noblemen(Game._MAX_NOBLEMEN[self._n])
        
    def next(self):
        """Ends the turn and goes to the next player"""
        player = self.active_player()
        if self._eligible(player, self._noblemen):
            while True:
                try:
                    pick = self._pick_noble(player, self._noblemen) 
                    break
                except (ValueError, TypeError):
                    print("Not a valid choice")
            noble = self._noblemen.pop(pick)
            player.add_noble(noble)
            player.add_points(noble.points())
        if self._player % self._n == 0:
            winner, high = None, 0
            for P in self._players:
                vp = P.points()
                if self._points_to_win <= vp and high <= vp:
                    high = vp
                    winner = P
            if winner is not None:
                print("{} wins!".format(winner))
                self._reset()
        self._player = (self._player + 1) % self._n

    def _reset(self):
        self._n = self._n
        self._player = 0
        self._players = [Player(i) for i in range(self._n)]
        self._points_to_win = self._points_to_win
        self._max_time = self._max_time
        self._bank = Bank(Game._MAX_BANK_COINS[self._n])
        self._decks = self._new_decks()
        self._board = self._new_board(self._decks)
        self._display = self._display
        self._noblemen = self._fill_noblemen(Game._MAX_NOBLEMEN[self._n])

    def _new_decks(self):
        import random
        level_0 = [Card(Game._BLACK,0,1,1,1,1,0),
                    Card(Game._BLACK,0,1,2,1,1,0),
                    Card(Game._BLACK,0,2,2,0,1,0),
                    Card(Game._BLACK,0,0,0,1,3,1),
                    Card(Game._BLACK,0,0,0,2,1,0),
                    Card(Game._BLACK,0,2,0,2,0,0),
                    Card(Game._BLACK,0,0,0,3,0,0),
                    Card(Game._BLACK,1,0,4,0,0,0),
                    Card(Game._BLUE,0,1,0,1,1,1),
                    Card(Game._BLUE,0,1,0,1,2,1),
                    Card(Game._BLUE,0,1,0,2,2,0),
                    Card(Game._BLUE,0,0,1,3,1,0),
                    Card(Game._BLUE,0,1,0,0,0,2),
                    Card(Game._BLUE,0,0,0,2,0,2),
                    Card(Game._BLUE,0,0,0,0,0,3),
                    Card(Game._BLUE,1,0,0,0,4,0),
                    Card(Game._WHITE,0,0,1,1,1,1),
                    Card(Game._WHITE,0,0,1,2,1,1),
                    Card(Game._WHITE,0,0,2,2,0,1),
                    Card(Game._WHITE,0,3,1,0,0,1),
                    Card(Game._WHITE,0,0,0,0,2,1),
                    Card(Game._WHITE,0,0,2,0,0,2),
                    Card(Game._WHITE,0,0,3,0,0,0),
                    Card(Game._WHITE,1,0,0,4,0,0),
                    Card(Game._GREEN,0,1,1,0,1,1),
                    Card(Game._GREEN,0,1,1,0,1,2),
                    Card(Game._GREEN,0,0,1,0,2,2),
                    Card(Game._GREEN,0,1,3,1,0,0),
                    Card(Game._GREEN,0,2,1,0,0,0),
                    Card(Game._GREEN,0,0,2,0,2,0),
                    Card(Game._GREEN,0,0,0,0,3,0),
                    Card(Game._GREEN,1,0,0,0,0,4),
                    Card(Game._RED,0,1,1,1,0,1),
                    Card(Game._RED,0,2,1,1,0,1),
                    Card(Game._RED,0,2,0,1,0,2),
                    Card(Game._RED,0,1,0,0,1,3),
                    Card(Game._RED,0,0,2,1,0,0),
                    Card(Game._RED,0,2,0,0,2,0),
                    Card(Game._RED,0,3,0,0,0,0),
                    Card(Game._RED,1,4,0,0,0,0)]
        level_1 = [Card(Game._BLACK,1,3,2,2,0,0),
                    Card(Game._BLACK,1,3,0,3,0,2),
                    Card(Game._BLACK,2,0,1,4,2,0),
                    Card(Game._BLACK,2,0,0,5,3,0),
                    Card(Game._BLACK,2,5,0,0,0,0),
                    Card(Game._BLACK,3,0,0,0,0,6),
                    Card(Game._BLUE,1,0,2,2,3,0),
                    Card(Game._BLUE,1,0,2,3,0,3),
                    Card(Game._BLUE,2,5,3,0,0,0),
                    Card(Game._BLUE,2,2,0,0,1,4),
                    Card(Game._BLUE,2,0,5,0,0,0),
                    Card(Game._BLUE,3,0,6,0,0,0),
                    Card(Game._WHITE,1,0,0,3,2,2),
                    Card(Game._WHITE,1,2,3,0,3,0),
                    Card(Game._WHITE,2,0,0,1,4,2),
                    Card(Game._WHITE,2,0,0,0,5,3),
                    Card(Game._WHITE,2,0,0,0,5,0),
                    Card(Game._WHITE,3,6,0,0,0,0),
                    Card(Game._GREEN,1,3,0,2,3,0),
                    Card(Game._GREEN,1,2,3,0,0,2),
                    Card(Game._GREEN,2,4,2,0,0,1),
                    Card(Game._GREEN,2,0,5,3,0,0),
                    Card(Game._GREEN,2,0,0,5,0,0),
                    Card(Game._GREEN,3,0,0,6,0,0),
                    Card(Game._RED,1,2,0,0,2,3),
                    Card(Game._RED,1,0,3,0,2,3),
                    Card(Game._RED,2,1,4,2,0,0),
                    Card(Game._RED,2,3,0,0,0,5),
                    Card(Game._RED,2,0,0,0,0,5),
                    Card(Game._RED,3,0,0,0,6,0)]
        level_2 = [Card(Game._BLACK,3,3,3,5,3,0),
                    Card(Game._BLACK,4,0,0,0,7,0),
                    Card(Game._BLACK,4,0,0,3,6,3),
                    Card(Game._BLACK,5,0,0,0,7,3),
                    Card(Game._BLUE,3,3,0,3,3,5),
                    Card(Game._BLUE,4,7,0,0,0,0),
                    Card(Game._BLUE,4,6,3,0,0,3),
                    Card(Game._BLUE,5,7,3,0,0,0),
                    Card(Game._WHITE,3,0,3,3,5,3),
                    Card(Game._WHITE,4,0,0,0,0,7),
                    Card(Game._WHITE,4,3,0,0,3,6),
                    Card(Game._WHITE,5,3,0,0,0,7),
                    Card(Game._GREEN,3,5,3,0,3,3),
                    Card(Game._GREEN,4,0,7,0,0,0),
                    Card(Game._GREEN,4,3,6,3,0,0),
                    Card(Game._GREEN,5,0,7,3,0,0),
                    Card(Game._RED,3,3,5,3,0,3),
                    Card(Game._RED,4,0,0,7,0,0),
                    Card(Game._RED,4,0,3,6,3,0),
                    Card(Game._RED,5,0,0,7,3,0)]
        random.shuffle(level_0), 
        random.shuffle(level_1),
        random.shuffle(level_2)
        return [level_0, level_1, level_2]

    def _new_board(self, decks):
        board = [[None] * Game._CARDS_PER_LEVEL 
                 for _ in range(Game._MAX_LEVELS)]
        for i in range(len(board)):
            for j in range(len(board[i])):
                card = self._decks[i].pop()
                card.set_key(i, j)
                board[i][j] = card
        return board

    def _fill_noblemen(self, num_noblemen):
        import random
        VP = 3
        nobles = [Noble(VP, 3, 3, 3, 0, 0),
                  Noble(VP, 0, 3, 3, 3, 0),
                  Noble(VP, 0, 0, 3, 3, 3),
                  Noble(VP, 3, 0, 0, 3, 3),
                  Noble(VP, 3, 3, 0, 0, 3),
                  Noble(VP, 4, 4, 0, 0, 0),
                  Noble(VP, 0, 4, 4, 0, 0),
                  Noble(VP, 0, 0, 4, 4, 0),
                  Noble(VP, 0, 0, 0, 4, 4),
                  Noble(VP, 4, 0, 0, 0, 4)]
        random.shuffle(nobles)
        return nobles[:num_noblemen]

    def active_player(self):
        return self._players[self._player]

    def ap(self):
        return self.active_player()

    def _collect(self, coins):
        """Adds coins to wallet

            coins: 6-tuple (0, 0, 0, 0, 0, 0)
        """
        player = self.active_player()
        wallet = player.wallet()
        total = sum(coins)
        if total > Game._REG_COLLECT:
            raise CollectError("Collected too many coins")
        if any(c > 1 for c in coins) and total != Game._DBL_COLLECT:
            raise CollectError("Collect 2 of a single color "
                               "or 3 different colors each")
        if coins[Game._WILD] > 0 and total != 1:
            raise CollectError("Only 1 wild")
        wallet += self._bank.give(coins)
        while wallet.overmax():
            adjustment = wallet.rebalance()
            self._bank.take(adjustment)

    def collect(self, coins):
        endturn = True
        try:
            self._collect(coins)
        except CollectError as e:
            print(e)
            endturn = False
        if endturn:
            self.next()

    def board(self):
        """Prints the board

        Sample Row
            "--------     --------     ---------     ---------",
            "|B    4|     |U    3|     |W     5|     |R     4|",
            "|      |     |      |     |       |     |       |",
            "|    G3|     |R3  G3|     |     W3|     |       |",
            "|B3  R6|     |W3  B5|     |     B7|     |     G7|",
            "|W3  U6|     |W3  B5|     |     B7|     |     G7|",
            "--------     --------     ---------     ---------"
        """
        width = 8
        dash = "-" * width
        space = " " * width
        blank = "|" + " " * (width - 2) + "|"
        header_stamp = "|{:<3}{:>3}|"
        template = "|{}{:<2}{:>2}{}|"
        
        n = len(self._board)
        for i in range(n):
            cards = self._board[n-i-1]
            m = len(cards)
            text = [space.join(dash for _ in range(m)),
                    space.join(header_stamp.format(C.color(), C.points()) for C in cards),
                    space.join(blank for _ in range(m)),
                    space.join(template.format("W", C._w, "U", C._u) for C in cards),
                    space.join(template.format("G", C._g, "R", C._r) for C in cards),
                    space.join(template.format("B", C._b, " ", " ") for C in cards),
                    space.join(dash for _ in range(m))]
            for t in text:
                print(t)
    
    def _buy(self, card):
        """Buy card from board if able. 
        
        Checks for sufficient funds first. If sufficient,
        charges the price from player wallet, checks for
        noblemen award, and adds points. Returns True 
        if purchase was successful, False otherwise.

            card: Card object
        """
        player = self.active_player()
        cost = card.cost()
        charge = cost + [0]
        n = len(cost)
        W = player.wallet()
        wilds = W[Game._WILD]
        for i in range(n):
            remainder = cost[i] - len(player._cards[i])
            if W[i] + wilds < remainder:
                return False, [0] * 6
            elif W[i] < remainder:
                charge[i] = W[i]
                wilds = wilds - (remainder - W[i])
            else:
                charge[i] = remainder
            if wilds < 0:
                return False, [0] * 6
        charge[Game._WILD] = W[Game._WILD] - wilds
        W -= charge
        player.cards()[card.color_index()].append(card)
        if card.key() is not None:
            self._replace(card)
            card.set_key(None)
        return True, charge

    def buy(self, i, j=None, card=None):
        card = i if j is None else self._board[i][j]
        player = self.active_player()
        purchase, payment = self._buy(card)
        if purchase is True:
            player.add_points(card.points())
            self._bank.take(payment)
            self.next()
        else:
            print("Insufficient funds")
            
    def _eligible(self, player, noblemen):
        cards = tuple(len(stack) for stack in player.cards())
        return [noble for noble in noblemen if noble <= cards]

    def _pick_noble(self, player, noblemen):
        for i, noble in enumerate(noblemen):
            print("({}), {}".format(i, noble))
        try:
            resp = int(input("Choose nobleman: "))
        except (ValueError, TypeError):
            raise
        return resp

    def _replace(self, card):
        i, j = card.key()
        new_card = self._decks[i].pop()
        new_card.set_key(i, j)
        self._board[i][j] = new_card

    def reserve(self, i, j=None, card=None):
        """Reserve a card from the board or deck

        card: Card object
        returns True if reservation was successful,
        False otherwise.
        """
        card = i if j is None else self._board[i][j]
        player = self.active_player()
        if Game._MAX_RESERVE <= len(player.reserved()):
            print("Cannot reserve >{} cards".format(Game._MAX_RESERVE))
            return False
        player.reserve(card)
        if card.key() is not None:
            self._replace(card)
            card.set_key(None)
        if 0 < self._bank[Game._WILD]:
            self.collect((0,0,0,0,0,1))
        else:
            self.next()
        return True

    def bank(self):
        print(self._bank)

    def noblemen(self):
        for noble in self._noblemen:
            print(noble, end=" ")
        print()

class Player:

    def __init__(self, name=None):
        self._wallet = Wallet()
        self._cards = [[] for _ in range(5)]
        self._reserved = []
        self._points = 0
        self._noblemen = []
        self._timer = 0
        self._name = name

    def wallet(self):
        return self._wallet

    def cards(self):
        return self._cards

    def reserved(self):
        return self._reserved
    
    def reserve(self, card):
        self._reserved.append(card)

    def unreserve(self, i):
        self._reserved.pop(i)

    def points(self):
        return self._points

    def noblemen(self):
        return self._noblemen

    def time(self):
        return self._timer

    def add_noble(self, noble):
        self._noblemen.append(noble)

    def add_points(self, points):
        self._points += points

class Bank:
    _COLORS = 5
    _NUM_WILDS = 5
    
    def __init__(self, max_coins):
        self._coins = [max_coins] * Bank._COLORS + [Bank._NUM_WILDS]
        self._n = sum(k for k in self._coins)
    
    def give(self, coins):
        for i in range(len(self._coins)):
            if self._coins[i] - coins[i] < 0:
                color = "WUGRBY"[i]
                raise CollectError("Insufficient coins for " + color)
        for i in range(len(self._coins)):
            self._coins[i] -= coins[i]
            self._n -= coins[i]
        return coins

    def take(self, coins):
        for i in range(len(self._coins)):
            self._coins[i] += coins[i]
            self._n += coins[i]

    def __getitem__(self, k):
        return self._coins[k]

    def __len__(self):
        return self._n

    def __str__(self):
        return "Bank<" + str(self._coins)[1:-1] + ">"

class Wallet:
    _MAX_COINS = 10

    def __init__(self, max_colors=6):
        self._max_colors = max_colors
        self._coins = [0] * self._max_colors
        self._n = 0

    def __add__(self, other):
        for i in range(len(self._coins)):
            self._coins[i] += other[i]
            self._n += other[i]
        return self

    def __sub__(self, other):
        for i in range(len(self._coins)):
            self._coins[i] -= other[i]
            self._n -= other[i]
        return self

    def overmax(self):
        return self._n > Wallet._MAX_COINS
    
    def negative(self):
        return any(c < 0 for c in self._coins)

    def rebalance(self):
        adjustment = (0,) * 6
        try:
            resp = input("Enter amount to return as 000000: ")
        except ValueError:
            return adjustment
        try:
            adjustment = tuple(int(c) for c in resp)
        except TypeError:
            return adjustment
        self -= adjustment
        return adjustment

    def __getitem__(self, k):
        return self._coins[k]

    def __len__(self):
        return self._n

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Wallet<" + str(self._coins)[1:-1] + ">"

class Card:
    __slots__ = ("_color", "_points", "_w", "_u", 
                 "_g", "_r", "_b", "_cost", "_key")
    _COLOR_DECODE = "WUGRBY"

    def __init__(self, color, points, 
                       white, blue, green,
                       red, black,
                       key=None):
        self._color = color
        self._points = points
        self._w = white
        self._u = blue
        self._g = green
        self._r = red
        self._b = black
        self._cost = (white, blue, green, red, black)
        self._key = key

    def color(self):
        return Card._COLOR_DECODE[self._color]

    def color_index(self):
        return self._color

    def cost(self):
        return [c for c in self._cost]

    def points(self):
        return self._points

    def key(self):
        return self._key

    def set_key(self, i, j=None):
        self._key = i if j is None else (i, j)

    def __repr__(self):
        return str(self.cost())

class Noble:
    __slots__ = ("_points", "_w", "_u", 
                 "_g", "_r", "_b", "_cost", "_key")
    _COLOR_DECODE = "WUGRBY"

    def __init__(self, points, 
                 white, blue, green, 
                 red, black, 
                 key=None):
        self._points = points
        self._w = white
        self._u = blue
        self._g = green
        self._r = red
        self._b = black
        self._cost = (white, blue, green, red, black)
        self._key = key

    def cost(self):
        return self._cost

    def points(self):
        return self._points

    def __str__(self):
        return "Noble<{}, {}, {}, {}, {}>".format(
                    self._w, self._u, self._g, 
                    self._r, self._b)
    
    def __lt__(self, other):
        cost = self._cost
        for i in range(len(cost)):
            if other[i] <= cost[i]:
                return False
        return True

    def __le__(self, other):
        cost = self._cost
        for i in range(len(cost)):
            if other[i] < cost[i]:
                return False
        return True

    def __gt__(self, other):
        return not (self <= other)

    def __ge__(self, other):
        return not (self < other)
