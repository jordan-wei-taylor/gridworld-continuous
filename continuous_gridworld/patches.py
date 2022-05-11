from continuous_gridworld.base import ObjectPatch
from matplotlib                import patches

class RectanglePatch(ObjectPatch):

    def __init__(self, xy, dx, dy, **kwargs):
        super().__init__(patches.Rectangle, xy, dx, dy, **kwargs)
        self.dx = dx
        self.dy = dy
        
    def _correction(self, xy):
        return (xy[0] - self.dx / 2, xy[1] - self.dy / 2)

class CirclePatch(ObjectPatch):

    def __init__(self, xy, r, **kwargs):
        super().__init__(patches.Circle, xy, r **kwargs)        
        self.dx = self.dy = r
