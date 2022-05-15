from gridworld_continuous.base import ObjectPatch
from matplotlib                import patches

class RectanglePatch(ObjectPatch):

    def __init__(self, loc, dx, dy, **kwargs):
        super().__init__(patches.Rectangle, loc, dx, dy, **kwargs)
        self.dx = dx
        self.dy = dy
        
    def _correction(self, loc):
        return (loc[0] - self.dx / 2, loc[1] - self.dy / 2)

class CirclePatch(ObjectPatch):

    def __init__(self, loc, r, **kwargs):
        super().__init__(patches.Circle, loc, r **kwargs)        
        self.dx = self.dy = r
