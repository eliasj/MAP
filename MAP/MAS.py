#! /usr/bin/env python

from PyOBEX import client, headers, responses

MAS_UUID = "\xBB\x58\x2B\x40\x42\x0C\x11\xDB\xB0\xDE\x08\x00\x20\x0c\x9A\xAA"


class Client(client.Client):

    def connect(self):
        response = client.Client.connect(
            self, header_list=[headers.Target(MAS_UUID)])
        if response != responses.ConnectSuccess:
            raise Exception

    def set_notification_registration(self):
        response = self.put("", str(0x30), header_list=[
            self.connection_id,
            headers.Type("x-bt/MAP-NotificationRegistration"),
            headers.App_Parameters(str(0x0e1))])
        if response != responses.Success:
            raise Exception

    def set_folder(self, folder):
        response = self.setpath(name=folder, header_list=[
            self.connection_id])
        if response != responses.Success:
            raise Exception

    def get_folder_listing(self):
        response = self.get(header_list=[
            self.connection_id,
            headers.Type("x-obex/folder-listing")])

        if isinstance(response, responses.FailureResponse):
            raise Exception()
        header, data = response
        return data

    def get_message_listing(self):
        response = self.get(header_list=[
            self.connection_id,
            headers.Type("x-bt/MAP-msg-listing")])

        if isinstance(response, responses.FailureResponse):
            raise Exception()
        header, data = response
        return data

    def get_message(self, message_id):
        response = self.get(header_list=[
            self.connection_id,
            headers.Name(message_id),
            headers.Type("x-bt/message"),
            headers.App_Parameters("\x0A\x01\x14\x01")])
        if isinstance(response, responses.FailureResponse):
            raise Exception()
        header, data = response
        return data

    def set_message_status(self, message_id, indicator, value):
        app_param = "\x17" + indicator + "\x18" + value
        response = self.put(message_id, str(0x30), header_list=[
            self.connection_id,
            headers.Type("x-bt/messageStatus"),
            headers.App_Parameters(app_param)])
        if response != responses.Success:
            raise Exception

    def set_message_read_satus(self, message_id):
        self.set_message_status(message_id, "\x00", "\x01")

    def set_message_unread_satus(self, message_id):
        self.set_message_status(message_id, "\x00", "\x00")

    def set_message_delete_satus(self, message_id):
        self.set_message_status(message_id, "\x01", "\x01")

    def set_message_undelete_satus(self, message_id):
        self.set_message_status(message_id, "\x01", "\x00")

    def push_message(self, folder, message):
        response = self.put(folder, message, header_list=[
            self.connection_id,
            headers.Type("x-bt/message"),
            headers.App_Parameters("\x0A\x01")])
        if response != responses.Success:
            raise Exception

    def update_inbox(self):
        response = self.put("", str(0x30), header_list=[
            self.connection_id,
            headers.Type("x-bt/MAP-messageUpdate")])
        if response != responses.Success:
            raise Exception
