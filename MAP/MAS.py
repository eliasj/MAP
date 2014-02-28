#! /usr/bin/env python

from PyOBEX import client, headers, responses

MAS_UUID = "\xBB\x58\x2B\x40\x42\x0C\x11\xDB\xB0\xDE\x08\x00\x20\x0c\x9A\xAA"

class Client(client.Client):

    def connect(self):
        
        response = client.Client.connect(
            self, header_list=[headers.Target(MAS_UUID)])

    def set_notification_registration(self):
        response = self.put("", str(0x30),header_list=[
            self.connection_id,
            headers.Type("x-bt/MAP-NotificationRegistration"),
            headers.App_Parameters(str(0x0e1))])

    def set_folder(self, folder):
        response = self.setpath(name=folder, header_list=[
            self.connection_id])

    def get_folder_listing(self):
        response = self.get(header_list=[
            self.connection_id,
            headers.Type("x-obex/folder-listing")])

        if isinstance(response, responses.FailureResponse):
            raise Exception()
        print response
        header, data = response
        return data

    def get_message_listing(self):
        response = self.get(header_list=[
            self.connection_id,
            headers.Type("x-bt/MAP-msg-listing")])

        if isinstance(response, responses.FailureResponse):
            raise Exception()
        print response
        header, data = response
        return data
        pass

    def get_message(self, message_id):
        pass

    def set_message_status(self, message_id):
        pass

    def push_message(self, message):
        pass

    def update_inbox(self):
        pass
