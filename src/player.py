class Player:
    def __init__(self, name='', username='', wins=0, losses=0, points=0):
        self._name = name
        self._username = username
        self._wins = wins
        self._losses = losses
        self._points = points
        self._lastGameWon = False
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        self._username = username
    
    @property
    def wins(self):
        return self._wins

    @wins.setter
    def wins(self, wins):
        self._wins = wins
    
    @property
    def losses(self):
        return self._losses

    @losses.setter
    def losses(self, losses):
        self._losses = losses

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        self._points = points

    @property
    def lastGameWon(self):
        return self._lastGameWon

    @lastGameWon.setter
    def lastGameWon(self, lastGameWon):
        self._lastGameWon = lastGameWon