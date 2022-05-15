base_exceptions = ['self', '__class__']

class Base():

    def __init__(self, params, exceptions = []):
        self.__store__(params, exceptions)

    def __store__(self, params, exceptions = []):
        exceptions   += base_exceptions
        self.__params = []
        for key, value in params.items():
            if key not in exceptions and key:
                setattr(self, key, value)
                self.__params.append(key)

        self.__name__ = self.__class__.__name__

    def __repr__(self):
        inner = ', '.join([f'{key} = {getattr(self, key)}' for key in self.__params])
        return f'{self.__name__}({inner})'

class ObjectPatch(Base):

    def __init__(self, Patch, loc, *args, **kwargs):
        super().__init__(locals())

    @property
    def xy(self):
        return self._correction(self.loc)

    def _correction(self, loc):
        return loc

    @property
    def patch(self):
        return self.Patch(self.xy, *self.args, **self.kwargs)
        
    def __call__(self, loc):
        self.loc = loc
        return self

    def contains(self, patch):
        me  = self.patch
        return me.get_path().contains_points(patch.vertices, me.get_transform())

    @property
    def vertices(self):
        return self.patch.get_verts()
