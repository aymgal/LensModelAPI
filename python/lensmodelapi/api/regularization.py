__author__ = 'aymgal'

from typing import Dict

from lensmodelapi.api.base import APIBaseObject
from lensmodelapi.api.parameter import Parameter


class Regularization(APIBaseObject):

    def __init__(self,
                 documentation: str, 
                 parameters: Dict[str, Parameter],
                 applied_to_profile_id: str = None) -> None:
        self.type = self.__class__.__name__  # name of children class
        self.documentation = documentation
        self.parameters = parameters
        self.applied_to_profile_id = applied_to_profile_id
        super().__init__()
