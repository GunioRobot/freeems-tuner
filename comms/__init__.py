#   Copyright 2009 Aaron Barnes
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


import libs.config, action


# Tuner's comms connections
_connection = {}


def createConnection(controller, name = 'default', type = None):
    '''
    Create new comms connection, with an optional name
    '''
    if type == None:
        type = _loadDefault()
    
    type = 'comms.'+type

    # Logger
    controller.log('comms', 'DEBUG', 'Loading comms module: %s' % type)

    # Dynamically import
    _connection[name] = __import__(type, globals(), locals(), 'connection').connection(name, controller)


def getConnection(name = 'default'):
    '''
    Get comms connection
    '''
    return _connection[name]


def _loadDefault():
    '''
    Load default comms connection type from config
    '''
    return libs.config.get('Comms', 'default')


class actions:

    class _action(action.action):

        def _getConnection(self):
            '''
            Get connection from action data, or use default
            '''
            if 'connection' in self._data:
                return getConnection(self._data['connection'])
            else:
                return getConnection()


    class sendRequest(_action):

        def run(self):
            '''
            Send packet to correct thread
            '''
            self._getConnection().send(self._data['packet'])


    class sendUtilityRequest(_action):

        def run(self):
            '''
            Create packet and send to correct thread
            '''
            comms = self._getConnection()

            comms.send(comms.getProtocol().getRequestPacket(self._data['type']))


    class sendMemoryRequest(_action):

        def run(self):
            '''
            Create memory request packet and send to correct thread
            '''
            comms = self._getConnection()

            packet = comms.getProtocol().getRequestPacket(self._data['type'])
            packet.setPayload(self._data['block_id'])

            comms.send(packet)


    class updateMainTableCell(_action):

        def run(self):
            '''
            Create packet and send to correct thread
            '''
            comms = self._getConnection()
            packet = comms.getProtocol().getRequestPacket(self._data['type'])

            packet.setTableId(self._data['block_id'])
            packet.setRpmAxis(self._data['rpm'])
            packet.setLoadAxis(self._data['load'])
            packet.setValue(self._data['value'])

            comms.send(packet)

    
    class handleReceivedPackets(action.action):

        def run(self):
            '''
            Trigger events in gui or anything else required
            '''
            comms = self._data['comms']
            protocol = comms.getProtocol()

            while self._data['queue']:

                response = self._data['queue'].pop(0)

                # Trigger watchers
                comms.triggerReceiveWatchers(response)

                # If a datalog packet, do not create a debug message
                if isinstance(response, protocol.responses.responseBasicDatalog):
                    return

                self._controller.log(
                        'comms.handleReceivedPackets',
                        'DEBUG',
                        '%s packet received and processed' % protocol.getPacketName(response.getPayloadIdInt())
                )


