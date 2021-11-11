# Single parameter of a profile

from typing import List

from lensmodelapi.api.base import APIBaseObject
from lensmodelapi.api.probabilities import Prior, PosteriorDistrib


__all__ = [
    'Parameter',
    'NonLinearParameter', 
    'LinearParameter', 
    'HyperParameter',
    'LinearParameterSet',
    'PixelParameterSet',
]


class DefinitionRange(APIBaseObject):

    def __init__(self, min_value=None, max_value=None):
        self.min_value = min_value
        self.max_value = max_value


class PointEstimate(APIBaseObject):

    def __init__(self, value=None):
        self.value = value


class Parameter(APIBaseObject):

    def __init__(self, 
                 name: str, 
                 description: str, 
                 definition_range: DefinitionRange,
                 units: str = None,
                 fixed: bool = False,
                 initial_estimate: PointEstimate = None,
                 posterior: PosteriorDistrib = None,
                 prior: Prior = None,
                 latex_name: str = None) -> None:
        self.name = name
        self.description = description
        self.units = units
        self.definition_range = definition_range
        self.fixed = fixed
        if not isinstance(initial_estimate, PointEstimate):
            self.initial_estimate = PointEstimate(initial_estimate)
        else:
            self.initial_estimate = initial_estimate
        self.point_estimate = PointEstimate(value=self.initial_estimate.value)
        if posterior is None:
            posterior = PosteriorDistrib()
        self.posterior = posterior
        if prior is None:
            prior = Prior()
        self.prior = prior
        if latex_name is None:
            latex_name = name
        self.latex_name = latex_name
        self.id = None
        super().__init__()
        
    def set_value(self, value, overwrite=False):
        if self.value is not None and not overwrite:
            raise ValueError(f"A value ({self.value:.2f}) has already been set.")
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"Value cannot be smaller than {self.min_value}.")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"Value cannot be larger than {self.max_value}.")
        self.value = value

    def set_prior(self, prior):
        if not isinstance(prior, Prior):
            raise ValueError("Parameter prior must be a subclass of Prior.")
        self.prior = prior

    def remove_prior(self):
        self.prior = None

    def fix(self):
        if self.value is None:
            raise ValueError(f"Cannot fix parameter {self.name} as no value has been set.")
        self.fixed = True

    def unfix(self):
        self.fixed = False


class NonLinearParameter(Parameter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LinearParameter(Parameter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class HyperParameter(Parameter):
    """Typically for pixelated profiles"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        


class ParameterSet(Parameter):
    """Typically for pixelated profiles"""

    def __init__(self, *args, **kwargs) -> None:
        if 'initial_estimate' not in kwargs or kwargs['initial_estimate'] is None:
            kwargs['initial_estimate'] = []
        if not isinstance(kwargs['initial_estimate'], list):
            raise ValueError("For any ParameterSet, `initial_estimate` must be a list of values.")
        super().__init__(*args, **kwargs)
        self.num_values = len(self.point_estimate.value)


class LinearParameterSet(ParameterSet):
    """Typically for pixelated profiles"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class PixelParameterSet(ParameterSet):
    """Typically for pixelated profiles"""

    def __init__(self, 
                 *args,
                 x_coords: List[float] = [],
                 y_coords: List[float] = [],
                 order_in_memory: str = 'C',
                 **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if (len(x_coords) != len(self.point_estimate.value) or 
            len(y_coords) != len(self.point_estimate.value)):
            raise ValueError("List of coordinates must have the same length as pixel values in `value`.")
        self.x_coords = x_coords
        self.y_coords = y_coords

        # see https://numpy.org/doc/stable/reference/generated/numpy.ndarray.flatten.html
        self.order_in_memory = order_in_memory
