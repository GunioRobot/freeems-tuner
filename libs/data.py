#   Copyright 2008 Aaron Barnes
#
#   This file is part of the FreeEMS project.
#
#   FreeEMS software is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   FreeEMS software is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with any FreeEMS software.  If not, see <http://www.gnu.org/licenses/>.
#
#   We ask that if you make any changes to this file you send them upstream to us at admin@diyefi.org


import os, sys

def createDirectory():

    # Create path
    path = getPath()

    # Check to see if it exists
    if os.path.exists(path) and os.path.isdir(path):
        return
        
    # Attempt to create
    os.mkdir(path)    


def getPath():

    cwd = sys.path[0]
    if not len(cwd):
        cwd = os.getcwd()
        
    return cwd+'/data/'
