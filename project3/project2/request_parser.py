import sys

class HTTPRequest(object):
    def __init__(self, request_bytes):
        self.raw = request_bytes
        self.headers = {}
        self.parse_request()

    def parse_request(self):
        # decode and split raw byte text
        lines = self.raw.split(b'\r\n\r\n', 1)
        self.data = lines[1]
        lines = lines[0].decode('UTF-8').split('\r\n')

        # first line request line
        self.command, self.path, self.protocol_version = lines[0].split(' ')

        # parse headers
        for line in lines[1:]:
            if (len(line) == 0):
                continue
            header_map = line.split(':', 1)
            assert(len(header_map) == 2)
            self.headers[header_map[0].lower()] = header_map[1].strip()

    def print_request_line(self):
        print(' '.join([self.command, self.path, self.protocol_version]))

    def rebuild_message(self):
        # rejoin request line
        out = ' '.join([self.command, self.path, self.protocol_version]) + '\r\n'

        # rejoin headers
        for header in self.headers.keys():
            out = out + header + ': ' + self.headers[header] + '\r\n'

        # append ending CRLF
        out += '\r\n'

        # encode text
        self.raw = out.encode('UTF-8') + self.data
        return self.raw