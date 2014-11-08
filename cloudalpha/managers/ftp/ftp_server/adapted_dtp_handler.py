from pyftpdlib.handlers import DTPHandler

########## TEMP #####################
from pyftpdlib.ioloop import AsyncChat
######################################

class AdaptedDTPHandler(DTPHandler):

    file_path = None

    class FileAdapter(object):

        _manager_unique_id = None
        _file_system_view = None
        _file_path = None

        closed = False

        @property
        def name(self):
            return self.file_path

        def __init__(self, manager_unique_id, file_system_view, file_path):
            self._manager_unique_id = manager_unique_id
            self._file_system_view = file_system_view
            self._file_path = file_path

        def write(self, chunk):
            self.file_system_view.write_to_new_file(self._manager_unique_id, self._file_path, chunk)

        def close(self):
            self.closed = True

    _file_adapter = None

    @property
    def file_obj(self):
        print("file_obj")
        if self.file_path is None:
            return None
        else:
            return self.FileAdapter(self.cmd_channel.fs.manager_unique_id, self.cmd_channel.fs.file_system_view, self.file_path)

    @file_obj.setter
    def file_obj(self, obj):
        print("file_obj", obj)

        pass

    def __init__(self, sock, cmd_channel):
        super(AdaptedDTPHandler, self).__init__(sock, cmd_channel)

    def _posix_ascii_data_wrapper(self, chunk):
        print("_posix_ascii_data_wrapper", chunk)

        return chunk

    def enable_receiving(self, type, cmd):
        print("enable_receiving", type, cmd)

        self.file_path = self.cmd_channel.upload_path
        file_system_view = self.cmd_channel.fs.file_system_view
        file_system_view.create_new_file(self.cmd_channel.fs.manager_unique_id, self.file_path)
        super(AdaptedDTPHandler, self).enable_receiving(type, cmd)

    def close(self):
        print("close")

        if not self._closed and self.file_obj != None:
            file_system_view = self.cmd_channel.fs.file_system_view
            if self.transfer_finished:
                file_system_view.commit_new_file(self.cmd_channel.fs.manager_unique_id, self.file_path)
            else:
                file_system_view.flush_new_file(self.cmd_channel.fs.manager_unique_id, self.file_path)
        self.cmd_channel._on_dtp_close()
        super(AdaptedDTPHandler, self).close()






    ###### TEMP ######

    def __repr__(self):
        print("__repr__")
        return super(AdaptedDTPHandler, self).__repr__()

    __str__ = __repr__

    def _use_sendfile(self, producer):
        print("_use_sendfile")
        return super(AdaptedDTPHandler, self)._use_sendfile(producer)

    def push(self, data):
        return super(AdaptedDTPHandler, self).push(data)

    def push_with_producer(self, producer):
        print("push_with_producer")

        self._initialized = True
        self.ioloop.modify(self._fileno, self.ioloop.WRITE)
        if self._use_sendfile(producer):
            print ("... if")
            self._offset = producer.file.tell()
            self._filefd = self.file_obj.fileno()
            self.initiate_sendfile()
            self.initiate_send = self.initiate_sendfile
        else:
            print("... else")
            AsyncChat.push_with_producer(self, producer)

    def close_when_done(self):
        print("close_when_done")
        return super(AdaptedDTPHandler, self).close_when_done()

    def initiate_send(self):
        print("initiate_send")
        return super(AdaptedDTPHandler, self).initiate_send()

    def initiate_sendfile(self):
        print("initiate_sendfile")
        return super(AdaptedDTPHandler, self).initiate_sendfile()

    # --- utility methods

    def get_transmitted_bytes(self):
        print("get_transmitted_bytes")
        return super(AdaptedDTPHandler, self).get_transmitted_bytes()

    def get_elapsed_time(self):
        print("get_elapsed_time")
        return super(AdaptedDTPHandler, self).get_elapsed_time()

    def transfer_in_progress(self):
        print("transfer_in_progress")
        return super(AdaptedDTPHandler, self).transfer_in_progress()

    # --- connection

    def send(self, data):
        print("send")
        return super(AdaptedDTPHandler, self).send(data)

    def refill_buffer(self):
        print("refill_buffer")
        return super(AdaptedDTPHandler, self).refill_buffer()

    def handle_read(self):
        print("handle_read")
        return super(AdaptedDTPHandler, self).handle_read()

    handle_read_event = handle_read  # small speedup

    def readable(self):
        print("readable")
        return super(AdaptedDTPHandler, self).readable()

    debug_writable = False
    def writable(self):
        if not self.debug_writable:
            print("writable")
            self.debug_writable = True
        return super(AdaptedDTPHandler, self).writable()

    def handle_timeout(self):
        print("handle_timeout")
        return super(AdaptedDTPHandler, self).handle_timeout()

    def handle_error(self):
        print("handle_error")
        return super(AdaptedDTPHandler, self).handle_error()

    def handle_close(self):
        print("handle_close")
        return super(AdaptedDTPHandler, self).handle_close()
