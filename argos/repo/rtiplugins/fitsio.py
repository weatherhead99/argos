""" Repository Tree Items (RTIs) for FITS data.
It uses the astropy package for data i/o.

See: https://docs.astropy.org/en/stable/io/fits/index.html

"""

import logging

from astropy.io import fits
from typing import Optional, Union, List

from argos.repo.baserti import BaseRti
from argos.repo.iconfactory import RtiIconFactory, ICON_COLOR_UNDEF

logger = logging.getLogger(__name__)

EXTENSION_TYPES = Union[fits.PrimaryHDU, fits.ImageHDU, fits.BinTableHDU, fits.TableHDU, fits.CompImageHDU]


class FITSExtensionRti(BaseRti):
    """ Repository Tree Item (RTI) representing a FITS extension """

    _defaultIconGlyph = RtiIconFactory.ARRAY
    
    def __init__(self, hdu, nodeName, fileName="", iconColor=ICON_COLOR_UNDEF):
        super().__init__(nodeName=nodeName,  iconColor=iconColor, fileName=fileName)
        self._hdu: Optional[EXTENSION_TYPES] = hdu

    @property
    def nDims(self):
        return int(self._hdu.header["NAXIS"])

    @property
    def attributes(self):
        if self._hdu is not None:
            return dict(self._hdu.header)
        return {}


    def hasChildren(self) -> bool:
        return False

    def __getitem__(self, index):
        return self._hdu.data.__getitem__(index)

class FITSImageExtensionRti(FITSExtensionRti): ...

class FITSTableExtensionRti(FITSExtensionRti): ...


    
def constructExtensionRti(hdu: EXTENSION_TYPES, *args, **kwargs):
    if isinstance(hdu, Union[fits.ImageHDU, fits.CompImageHDU]):
        return FITSImageExtensionRti(hdu, *args **kwargs)
    elif isinstance(hdu, Union[fits.TableHDU, fits.BinTableHDU]):
        return FITSTableExtensionRti(hdu, *args, **kwargs)

    
class FITSFileRti(FITSExtensionRti):
    """ Repository Tree Item (RTI) representing a FITS file (i.e. a primary HDU with zero or more extensions)"""
    _defaultIconGlyph = RtiIconFactory.FILE

    def __init__(self, nodeName, fileName='', iconColor=ICON_COLOR_UNDEF):
        self._hdul: Optional[fits.HDUList] = None
        super().__init__(hdu=None, nodeName=nodeName, iconColor=iconColor, fileName=fileName)
        self._checkFileExists()

    def _openResources(self) -> None:
        """opens a FITS file"""
        logger.info("opening HDUL: {}".format(self._fileName))
        self._hdul = fits.open(self._fileName, lazy_load_hdus=True,
                               mode="readonly")
        self._hdu = self._hdul[0]

    def _closeResources(self) -> None:
        """closes the FITS file"""
        logger.info("closing HDUL: {}".format(self._fileName))
        self._hdul.close()

    def hasChildren(self):
        return True

    def _fetchAllChildren(self) -> List[FITSExtensionRti]:
        assert self._hdul is not None
        
        children = []

        for hdu in self._hdul[1:]:
            nm = hdu.name
            children.append(FITSExtensionRti(hdu, nodeName=nm, fileName=self._fileName,
                                             iconColor=ICON_COLOR_UNDEF))

        return children


