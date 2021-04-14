from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs, urlparse

from HyperDeck import HyperDeck
from time import sleep

def get_local_file(file_name):
    with open(file_name) as f:
        lines = f.readlines()
        file_text = ''
        for line in lines:
            file_text += line.replace('\r', '').replace('\n', '')
        return file_text

def get_clips():
    clip_list = hyperdeck.get_clips_list()
    return json.dumps(clip_list)

def play_clip_with_index(clip_index):
    response = hyperdeck.select_clip_with_index(clip_index)
    response = hyperdeck.play()
    return json.dumps(response)

def get_status():
    response = hyperdeck.get_transport_info()
    return json.dumps(response)

def stop():
    response = hyperdeck.stop()
    return json.dumps(response)

def play():
    response = hyperdeck.play()
    return json.dumps(response)

def play_range(from_timecode, to_timecode):
    response = hyperdeck.set_playrange(from_timecode, to_timecode)
    response = hyperdeck.play()
    return json.dumps(response)



class MyHttpRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        response = ''

        # Extract query param
        if self.path == '/':
            response = get_local_file('index.html')

        elif self.path == '/getstatus':
            response = get_status()

        elif self.path == '/stop':
            response = stop()

        elif self.path == '/play':
            response = play()

        elif self.path == '/index.js':
            response = get_local_file('index.js')

        elif self.path == '/getclips':
            response = get_clips()

        elif self.path == '/getclips':
            response = get_clips()

        elif self.path.startswith('/playclip'):
            path_list = self.path.split('/')
            clip_index = int(path_list[2])
            response = play_clip_with_index(clip_index)

        elif self.path.startswith('/playrange'):
            path_list = self.path.split('/')
            from_timecode = path_list[2]
            to_timecode = path_list[3]
            print(from_timecode, to_timecode)
            response = play_range(from_timecode, to_timecode)

        else:
            self.send_response(404)

        # Writing the HTML contents with UTF-8
        try:
            if response != '':
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.send_header("Content-Length", str(len(response)))
                self.end_headers()
                self.wfile.write(response.encode("utf8"))
                self.wfile.flush()
        except TypeError as te:
            print(te)
        except ConnectionAbortedError as cae:
            print(cae)
            print(response)


        return

hyperdeck = HyperDeck("192.168.0.145", 9993)
hyperdeck.connect()
httpd = HTTPServer(("localhost", 8080), MyHttpRequestHandler)
httpd.serve_forever()