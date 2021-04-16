from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs, urlparse
import argparse

from HyperDeck import HyperDeck
from time import sleep

def get_local_file(file_name):
    with open(file_name) as f:
        lines = f.readlines()
        file_text = ''
        for line in lines:
            # file_text += line.replace('\r', '').replace('\n', '')
            file_text += line
        return file_text

def get_clips():
    clip_list = hyperdeck.get_clips_list()
    return json.dumps(clip_list)

def play_clip_with_index(clip_index, loop):
    response = hyperdeck.select_clip_with_index(clip_index)
    response = hyperdeck.play(loop)
    return json.dumps(response)

def get_status():
    response = hyperdeck.get_transport_info()
    return json.dumps(response)

def stop():
    response = hyperdeck.stop()
    return json.dumps(response)

def play(loop):
    response = hyperdeck.play(loop)
    return json.dumps(response)

def play_range(from_timecode, to_timecode, loop):
    response = hyperdeck.set_playrange(from_timecode, to_timecode)
    response = hyperdeck.play(loop)
    return json.dumps(response)



class MyHttpRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        response = ''

        # Extract query param
        if self.path == '/':
            response = get_local_file('index.html')

        elif self.path == '/status':
            response = get_status()

        elif self.path == '/stop':
            response = stop()

        elif self.path == '/play':
            response = play(False)

        elif self.path == '/play/loop':
            response = play(True)

        elif self.path == '/index.js':
            response = get_local_file('index.js')

        elif self.path == '/getclips':
            response = get_clips()

        elif self.path.startswith('/playclip'):
            path_list = self.path.split('/')
            clip_index = int(path_list[2])
            if self.path.endswith('/loop'):
                response = play_clip_with_index(clip_index, True)
            else:
                response = play_clip_with_index(clip_index, False)

        elif self.path.startswith('/playrange'):
            # Example /playrange/00:30:00:00/00:31:00:00
            # Gets the HyperDeck to play for 1 minute in a loop
            path_list = self.path.split('/')
            from_timecode = path_list[2]
            to_timecode = path_list[3]
            if self.path.endswith('/loop'):
                response = play_range(from_timecode, to_timecode, True)
            else:
                response = play_range(from_timecode, to_timecode, False)

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


if __name__ == "__main__":
    try:
        print("HyperDeck Playlist Controller Web/API Server")
        parser = argparse.ArgumentParser()
        parser.add_argument("address", type=str, help="IP address of the HyperDeck to connect to")
        args = parser.parse_args()
        print("Connecting to HyperDeck at IP address " + args.address + "...")
        hyperdeck = HyperDeck(args.address, 9993)
        hyperdeck.connect()
        print("Connected to HyperDeck at IP address " + args.address)
        print("Starting localhost web server")
        httpd = HTTPServer(("localhost", 8080), MyHttpRequestHandler)
        print("Ready")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down localhost web server")
        httpd.shutdown()
        print("Disconnecting from HyperDeck at IP address " + args.address)
        hyperdeck.disconnect()
        print("Shutdown completed")
    except HyperDeck.HyperDeckException as hde:
        print(hde)