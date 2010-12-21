#   Copyright 2008, 2009 Aaron Barnes
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


import comms.protocols as protocols, send, receive, requests, responses, test


START_BYTE          = chr(0xAA)
END_BYTE            = chr(0xCC)
ESCAPE_BYTE         = chr(0xBB)
SPECIAL_BYTES       = (ESCAPE_BYTE, START_BYTE, END_BYTE)

HEADER_HAS_LENGTH   = protocols.BIT0
HEADER_IS_NACK      = protocols.BIT1
HEADER_HAS_SEQUENCE = protocols.BIT2

REQUEST_INTERFACE_VERSION       = 0
REQUEST_FIRMWARE_VERSION        = 2
REQUEST_MAX_PACKET_SIZE         = 4
REQUEST_ECHO_PACKET_RETURN      = 6
REQUEST_SOFT_SYSTEM_RESET       = 8
REQUEST_HARD_SYSTEM_RESET       = 10
REQUEST_ASYNC_ERROR_CODE        = 12
REQUEST_ASYNC_DEBUG_INFO        = 14

RESPONSE_INTERFACE_VERSION      = 1
RESPONSE_FIRMWARE_VERSION       = 3
RESPONSE_MAX_PACKET_SIZE        = 5
RESPONSE_ECHO_PACKET_RETURN     = 7
RESPONSE_SOFT_SYSTEM_RESET      = 9
RESPONSE_HARD_SYSTEM_RESET      = 11
RESPONSE_ASYNC_ERROR_CODE       = 13
RESPONSE_ASYNC_DEBUG_INFO       = 15

REQUEST_REPLACE_BLOCK_IN_RAM            = 256
REQUEST_REPLACE_BLOCK_IN_FLASH          = 258
REQUEST_RETRIEVE_BLOCK_FROM_RAM         = 260
REQUEST_RETRIEVE_BLOCK_FROM_FLASH       = 262
REQUEST_BURN_BLOCK_FROM_RAM_TO_FLASH    = 264
REQUEST_ERASE_ALL_BLOCKS_FROM_FLASH     = 266
REQUEST_BURN_ALL_BLOCKS_OF_FLASH        = 268

RESPONSE_REPLACE_BLOCK_IN_RAM           = 257
RESPONSE_REPLACE_BLOCK_IN_FLASH         = 259
RESPONSE_RETRIEVE_BLOCK_FROM_RAM        = 261
RESPONSE_RETRIEVE_BLOCK_FROM_FLASH      = 263
RESPONSE_BURN_BLOCK_FROM_RAM_TO_FLASH   = 265
RESPONSE_ERASE_ALL_BLOCKS_FROM_FLASH    = 267
RESPONSE_BURN_ALL_BLOCKS_OF_FLASH       = 269

REQUEST_ADJUST_MAIN_TABLE_CELL          = 300

#REQUEST_ASYNC_DATALOG_STATUS            = 304
#RESPONSE_ASYNC_DATALOG_STATUS           = 305

REQUEST_BASIC_DATALOG                   = 400
RESPONSE_BASIC_DATALOG                  = 401

REQUEST_PACKET_TITLES = {
        REQUEST_INTERFACE_VERSION:              "InterfaceVersion",
        REQUEST_FIRMWARE_VERSION:               "FirmwareVersion",
        REQUEST_MAX_PACKET_SIZE:                "MaxPacketSize",
        REQUEST_ECHO_PACKET_RETURN:             "EchoPacket",
        REQUEST_SOFT_SYSTEM_RESET:              "SoftReset",
        REQUEST_HARD_SYSTEM_RESET:              "HardReset",
        REQUEST_ASYNC_ERROR_CODE:               "AsyncError",
        REQUEST_ASYNC_DEBUG_INFO:               "AsyncDebug",
        REQUEST_RETRIEVE_BLOCK_FROM_RAM:        "RetrRamBlock",
        REQUEST_RETRIEVE_BLOCK_FROM_FLASH:      "RetrFlashBlock",
        REQUEST_BURN_BLOCK_FROM_RAM_TO_FLASH:   "BurnBlockFlash",
        REQUEST_ADJUST_MAIN_TABLE_CELL:         "AdjustTableCell",
        REQUEST_BASIC_DATALOG:                  "BasicDatalog",
#        REQUEST_ASYNC_DATALOG_STATUS:       "AsyncDatalogStatus",
}

RESPONSE_PACKET_TITLES = {
        RESPONSE_INTERFACE_VERSION:     "InterfaceVersion",
        RESPONSE_FIRMWARE_VERSION:      "FirmwareVersion",
        RESPONSE_MAX_PACKET_SIZE:       "MaxPacketSize",
        RESPONSE_ECHO_PACKET_RETURN:    "EchoPacket",
        RESPONSE_ASYNC_ERROR_CODE:      "AsyncError",
        RESPONSE_ASYNC_DEBUG_INFO:      "AsyncDebug",
#        RESPONSE_ASYNC_DATALOG_STATUS:  "AsyncDatalogStatus",
        RESPONSE_BASIC_DATALOG:         "BasicDatalog",
        RESPONSE_RETRIEVE_BLOCK_FROM_RAM: "DataRequest",
}
        
MEMORY_PACKET_TITLES = {
        REQUEST_RETRIEVE_BLOCK_FROM_RAM:     "RetrieveBlockFromRAM",
        REQUEST_RETRIEVE_BLOCK_FROM_FLASH:   "RetrieveBlockFromFlash",
        REQUEST_BURN_BLOCK_FROM_RAM_TO_FLASH:"BurnBlockFromRamToFlash"
}


UTILITY_REQUEST_PACKETS = {
        'Interface Version':        'InterfaceVersion',
        'Firmware Version':         'FirmwareVersion',
        'Max Packet Size':          'MaxPacketSize',
        'Echo Packet Return':       'EchoPacketReturn',
#        'Async Datalog Status':     'AsyncDatalogStatus'
}


def getProtocolName():
    '''
    Return a human readable protocol name
    '''
    parts = __name__.split('.')
    return ('%s (%s)' % (parts[2], parts[3])).replace('_', '.')


def getSendObject(name, controller, comms):
    return send.thread(name, controller, comms)


def getReceiveObject(name, controller, comms):
    return receive.thread(name, controller, comms)


def getRequestPacket(type):
    '''
    Create and return a request packet
    '''
    return getattr(requests, 'request'+type)()


def getResponsePacket(type):
    '''
    Create and return a response packet
    '''
    return getattr(responses, 'response'+type)()


def getPacketName(id):
    '''
    Return human readable packet type
    '''
    if id in REQUEST_PACKET_TITLES:
        return REQUEST_PACKET_TITLES[id]
    elif id in RESPONSE_PACKET_TITLES:
        return RESPONSE_PACKET_TITLES[id]
    else:
        return 'Unknown'


def getMemoryRequestPayloadIdList():
    '''
    Return list of memory request payload ids
    '''
    return MEMORY_PACKET_TITLES


def getTestResponse(packet):
    '''
    Generate and return the correct response to apacket
    '''
    return test.getResponse(packet)
