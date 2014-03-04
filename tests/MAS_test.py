#! /usr/bin/env python

import unittest
from mock import Mock

import socket
import struct
import PyOBEX

from MAP import MAS


class MAS_client_test(unittest.TestCase):
    _mas = None
    _connection_id = None
    def setUp(self):
        
        address = "fake"
        port = 0
        self._mas = MAS.Client(address, port)

    def connect(self):
        self._connection_id = PyOBEX.headers.Connection_ID(0x0001)
        response = PyOBEX.responses.ConnectSuccess()
        data = "\xa0\x00\x1f\x10\x00\xff\xfe\xcb\x00\x00\x00\x01\x4a\x00\x13\xbb\x58\x2b\x40\x42\x0c\x11\xdb\xb0\xde\x08\x00\x20\x0c\x9a\x66"
        obex_version, flags, max_packet_length = struct.unpack(">BBH", data[3:7])
        response.obex_version = PyOBEX.common.OBEX_Version()
        response.obex_version.from_byte(obex_version)
        response.flags = flags
        response.max_packet_length = max_packet_length
        response.read_data(data)
 
        PyOBEX.client.Client._send_headers = Mock(
            return_value = response)
        self._mas.set_socket(Mock())
        self._mas.connect()

    def test_not_connected(self):
        self.assertIsNone(self._mas.connection_id)

    def test_connect(self):
        self.connect()
        self.assertIsNotNone(self._mas.connection_id)
        self.assertEqual(self._connection_id.data, self._mas.connection_id.data)

    def test_disconnet(self):
        self.connect()
        self._mas.disconnect()
        self.assertIsNone(self._mas.connection_id)

    def test_set_notifiaction_registration(self):
        self.connect()
        self._mas.set_notification_registration()

    def test_get_folder_listing(self):
        self.connect()
        folder_list = "\x01\x02\x03"
        response = PyOBEX.responses.Success()
        response.add_header(self._connection_id, 8)
        response.add_header(PyOBEX.headers.End_Of_Body(folder_list, True), len(folder_list) + 3)
        PyOBEX.client.Client._send_headers = Mock(
            return_value = response)
        self.assertEqual(folder_list, self._mas.get_folder_listing())

    def test_get_message_listing(self):
        self.connect()
        data = "\xA0\x00\x13\xcb\x00\x00\x00\x01\x49\x00\x0b\x00\x6d\x00\x73\x00\x67\x00\x00"
        message_list = "\x00\x6d\x00\x73\x00\x67\x00\x00"
        response = PyOBEX.responses.Success()
        response.read_data(data)
        PyOBEX.client.Client._send_headers = Mock(
            return_value = response)
        self.assertEqual(message_list, self._mas.get_message_listing())

    def test_set_folder(self):
        self.connect()
        response = PyOBEX.responses.Success()
        response.add_header(self._connection_id, 8)
        PyOBEX.client.Client._send_headers = Mock(
            return_value = response)
        self._mas.set_folder("folder")
