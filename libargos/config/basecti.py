# -*- coding: utf-8 -*-

# This file is part of Argos.
# 
# Argos is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Argos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Argos. If not, see <http://www.gnu.org/licenses/>.

""" Configuration TreeItem (CTI) classes
    Tree items for use in the ConfigTreeModel
"""
import logging

from libargos.config.abstractcti import AbstractCti, AbstractCtiEditor
from libargos.qt import QtGui
from libargos.utils.misc import NOT_SPECIFIED

logger = logging.getLogger(__name__)


        
class BaseCtiEditor(AbstractCtiEditor):
    """ A CtiEditor which contains a QLineEdit for editing BaseCti objects. 
    """
    def __init__(self, cti, delegate, parent=None):
        """ See the AbstractCtiEditor for more info on the parameters 
        """
        super(BaseCtiEditor, self).__init__(cti, delegate, [QtGui.QLineEdit()], parent=parent)
    
    
    def setData(self, value):
        """ Provides the main editor widget with a data to manipulate.
        """
        lineEditor = self.mainEditor
        lineEditor.setText(str(value))
        
        
    def getData(self):
        """ Gets data from the editor widget.
        """
        lineEditor = self.mainEditor 
        return lineEditor.text()
    
    
    
class BaseCti(AbstractCti):
    """ Config Tree Item to store a any type of data as long as it can be edited with a QLineEdit.
    """
    def __init__(self, nodeName, data=NOT_SPECIFIED, defaultData=''):
        """ Constructor. For the parameters see the AbstractCti constructor documentation.
        """
        super(BaseCti, self).__init__(nodeName, data=data, defaultData=defaultData)

    
    def _enforceDataType(self, value):
        """ Since BaseCti can store any type of data no conversion will be done. 
        """
        return value
    
    
    def createEditor(self, delegate, parent, option):
        """ Creates an BaseCtiEditor. 
            For the parameters see the AbstractCti constructor documentation.
        """
        return BaseCtiEditor(self, delegate, parent=parent) 
    
