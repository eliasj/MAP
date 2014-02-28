#!/usr/bin/env python

import bluetooth
from PyOBEX import server, headers, responses, requests

MNS_CLASS = "1133"
MNS_PROFILE = (MNS_CLASS, 0x0100)

class Server(server.Server):
    _p = None
    def start_service(self, port = None):
        if port is None:
            port = bluetooth.get_availiable_port(blutooth.RFCOMM)

        name = "MNS"
        uuid = "BB582B41-420C-11DB-B0DE-0800200C9A66"
        service_classes = [MNS_CLASS]
        service_profiles = [MNS_PROFILE]
        provider = ""
        description = " Message Access Profile (Message Notification Service)"
        protocols = [bluetooth.OBEX_UUID]

        socket = server.Server.start_service(
            self, port, name, uuid, service_classes, service_profiles,
            provider, description, protocols
            )

    def put(self, socket, request):
        request_type = None
        request_body = ""

        for header in request.header_data:
            if isinstance(header, headers.Type):
                request_type = header.decode()
            elif isinstance(header, headers.Body):
                request_body.appand(header.decode())
            elif isinstance(header, header.End_Of_Body):
                request_body.append(header.decode())

        if request_type == "x-bt/MAP-event-report":
            response = responses.Success()
            self.send_response(socket, response)
        else:
            self._reject(socket)
