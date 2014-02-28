#! /usr/bin/env python

import unittest
from mock import Mock

import PyOBEX
import bluetooth

from MAP import MNS

class MNS_server_test(unittest.TestCase):
    _mns = None
    _socket = None

    def setUp(self):
        self._socket = Mock()
        self._socket.accept.return_value = (self._socket, ("adress","2"))
        PyOBEX.server.Server.start_service = Mock(
            return_value = self._socket)
        self._mns = MNS.Server()
        self._mns.start_service(port="10")


    def test_connect(self):
        data = "\x80\x00\x1a\x10\x00\x20\x00\x46\x00\x13\xbb\x58\x2b\x41\x42\x0c\x11\xdb\xb0\xde\x08\x00\x20\x0c\x9a\x66"
        connect = PyOBEX.requests.Connect()
        connect.read_data(data)
        self._mns.connect(self._socket, connect)
        self.assertIs(connect, self._mns.remote_info)

    def test_disconnect(self):
        self._mns.connected = True
        disconnect = PyOBEX.requests.Disconnect()
        self._mns.disconnect(self._socket, disconnect)
        print self._socket.mock_calls
        self.assertFalse(self._mns.connected)
        self.assertTrue(self._socket.sendall.called)

    def test_send_event(self):
        send_event = PyOBEX.requests.Put()
        send_event.add_header(PyOBEX.headers.Type("x-bt/MAP-event-report"), 50)
        self._mns.put(self._socket, send_event)
        self.assertTrue(self._socket.sendall.called)
