from gridworld_continuous.patches import RectanglePatch, CirclePatch


def gold_defaults(kwargs):
    kwargs.setdefault('fc', 'y')
    kwargs.setdefault('ec', 'k')


def bomb_defaults(kwargs):
    kwargs.setdefault('fc', 'r')
    kwargs.setdefault('ec', 'k')


class Event():

    def __init__(self, name, reward):
        self.name   = name
        self.reward = reward


class RectangleEvent(Event, RectanglePatch):

    def __init__(self, name, loc, reward, dx, dy, **kwargs):
        Event.__init__(self, name, reward)
        RectanglePatch.__init__(self, loc, dx, dy, **kwargs)
        self.__store__(locals())


class CircleEvent(Event, CirclePatch):

    def __init__(self, name, loc, reward, r, **kwargs):
        Event.__init__(self, name, reward)
        CirclePatch.__init__(self, loc, r, **kwargs)
        self.__store__(locals())


class RectangleGold(RectangleEvent):

    def __init__(self, loc, reward = 10, dx = 0.5, dy = 0.5, **kwargs):

        gold_defaults(kwargs)
        
        super().__init__('gold', loc, reward, dx, dy, **kwargs)
        self.__store__(locals())
        

class RectangleBomb(RectangleEvent):

    def __init__(self, loc, reward = -10, dx = 0.5, dy = 0.5, **kwargs):

        bomb_defaults(kwargs)
        
        super().__init__('bomb', loc, reward, dx, dy, **kwargs)
        self.__store__(locals())


class SquareGold(RectangleEvent):

    def __init__(self, loc, reward = 10, dx = 0.5, **kwargs):

        gold_defaults(kwargs)
        
        super().__init__('gold', loc, reward, dx, dx, **kwargs)
        self.__store__(locals())


class SquareBomb(RectangleEvent):

    def __init__(self, loc, reward = -10, dx = 0.5, **kwargs):

        bomb_defaults(kwargs)
        
        super().__init__('bomb', loc, reward, dx, dx, **kwargs)
        self.__store__(locals())


class CircleGold(CircleEvent):

    def __init__(self, loc, reward = 10, r = 0.5, **kwargs):

        gold_defaults(kwargs)
        
        super().__init__('gold', loc, reward, r, **kwargs)
        self.__store__(locals())


class CircleBomb(CircleEvent):

    def __init__(self, loc, reward = -10, r = 0.5, **kwargs):

        bomb_defaults(kwargs)
        
        super().__init__('bomb', loc, reward, r, **kwargs)
        self.__store__(locals())

