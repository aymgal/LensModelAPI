__author__ = 'aymgal'

from lensmodelapi.api.base import APIBaseObject


class Coordinates(APIBaseObject):

    _orientations_ra = ['left', 'right']
    _orientations_dec = ['top', 'bottom']
    _origins = ['center', 'bottom left']

    def __init__(self, 
                 orientation_ra: str = 'left', 
                 orientation_dec: str = 'top',
                 origin_position: str = 'center',
                 ) -> None:
        if orientation_ra not in self._orientations_ra:
            raise ValueError(f"RA orientation can only be in {self._orientations_ra}.")
        self.orientation_ra = orientation_ra
        if orientation_dec not in self._orientations_dec:
            raise ValueError(f"Dec orientation can only be in {self._orientations_dec}.")
        self.orientation_dec = orientation_dec
        if origin_position not in self._origins:
            raise ValueError(f"Dec orientation can only be in {self._origins}.")
        self.origin_position = origin_position
        super().__init__()

    def update_with_instrument(self, instrument):
        pixel_size = instrument.pixel_size
        sign_ra  = (self.orientation_ra == 'left')
        sign_dec = (self.orientation_dec == 'top')
        self.pix2angle_matrix = [
            [sign_ra * pixel_size, 0],
            [0, sign_dec * pixel_size],
        ]
        if self.origin_position == 'center':
            half_fov_ra = instrument.field_of_view_ra / 2.
            half_fov_dec = instrument.field_of_view_ra / 2.
            self.ra_at_xy_0 = - half_fov_ra + pixel_size / 2.
            self.dec_at_xy_0 = - half_fov_dec + pixel_size / 2.
        else:
            self.ra_at_xy_0 = 0.
            self.dec_at_xy_0 = 0.