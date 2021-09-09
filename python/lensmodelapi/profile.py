__author__ = 'aymgal'

from lensmodelapi.parameter_list import ParameterList


__all__ = [
    'Profile', 
    'LightProfile', 
    'MassProfile', 
]


class Profile(object):

    def __init__(self,
                 name: str, 
                 description: str, 
                 parameters: ParameterList) -> None:
        self.name = name
        self.description = description
        self.parameters = parameters
        

class LightProfile(Profile):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MassProfile(Profile):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
