""" Repository Tree Items (RTIs) for FITS data.
It uses the astropy package for data i/o.

See: https://docs.astropy.org/en/stable/io/fits/index.html

"""

import logging

from astropy.io import fits
from typing import Optional, Union

from argos.repo.baserti import BaseRti
from argos.repo.iconfactory import RtiIconFactory, ICON_COLOR_UNDEF

logger = logging.getLogger(__name__)

EXTENSION_TYPES = Union[fits.PrimaryHDU, fits.ImageHDU, fits.BinTableHDU, fits.TableHDU, fits.CompImageHDU]


class FITSExtensionRti(BaseRti): 
    """ Repository Tree Item (RTI) representing a FITS extension """

    def __init__(self, hdu, nodeName, fileName="", iconColor=ICON_COLOR_UNDEF):
        super().__init__(self, nodeName,  iconColor, fileName)
        self._hdu: Optional[EXTENSION_TYPES] = None


    def hasChildren(self):
        """FITS Extensions cannot be hierarchically embedded, thus this is always False"""
        return False




class FITSFileRti(FITSExtensionRti):
    _defaultIconGlyph = RtiIconFactory.FILE

    def __init__(self, nodeName, fileName='', iconColor=ICON_COLOR_UNDEF):
        self._hdul: Optional[fits.HDUList] = None
        super().__init__(self, None, nodeName, iconColor, fileName)
        self._checkFileExists()

    def _openResources(self):
        """opens a FITS file"""
        logger.info("opening: {}".format(self._fileName))
        self._hdul = fits.open(self._fileName, lazy_load_hdus=True,
                               mode="readonly")

    def _closeResources(self):
        """closes the FITS file"""
        logger.info("closing: {}".format(self._fileName))
        self._hdul.close()

    def hasChildren(self):
        """implement it this way to avoid calling len(hdul) and thus losing the
        benefits of lazily loading the 
