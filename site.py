import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import argparse
import sys
# import psycopg2
from tornado.options import define, options, parse_command_line

import os

sys.path.insert(0, 'WebHandlers/')
from handler import Handler



define("port", default=8888, help="run on the given port", type=int)

# we gonna store clients in dictionary..
clients = dict()

# Gon keep the db connection global as heck.
# conn = psycopg2.connect(database = "commons", 
                            # user = "postgres", 
                        # password = "pass123",
                            # host = "127.0.0.1", 
                            # port = "5432")
# cursor = conn.cursor()

# Gon parse arguments too, y'all.
parser = argparse.ArgumentParser(description='Commons game public python server.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
args = parser.parse_args()

def broadcast(obj):
    connect_message = json.dumps(obj)
    for c in clients:
        clients[c]["object"].write_message(connect_message)

class JsHandler(tornado.web.RequestHandler):
    # @tornado.web.asynchronous
    def get(self, script):
        self.render("Foundation/js/" + script)
        # self.render("web/commonsGame.js")

class IndexHandler(tornado.web.RequestHandler):
    # @tornado.web.asynchronous
    def get(self):
        self.render("Foundation/test_site.html")
        # self.render("web/index.html")


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    player1 = 0
    player2 = 0
    game_id = 0

    # handler = Handler(cursor)


    def on_message(self, message):        
        msg = json.loads(message);
        if 'type' not in msg:
            return
        elif msg['type'] == 'chat':
            if len(msg['name']) == 0 or len(msg['text']) == 0:
                return
            self.handleChat(msg)
        elif msg['type'] == 'connect':
            self.handleConnection(msg)

    def open(self, *args):
        self.id = len(clients.keys())
        self.handler.open(args, self.id)
        
    def on_close(self):
        self.handler.close(self.id)

    def handleConnection(self, msg):
        self.handler.connection(msg)

    def handleChat(self, msg):
        msg["player_id"] = self.id
        self.handler.chat(msg)
        broadcast(msg)

    def handleMove(self):
        pass

settings = {'debug': True, 
            'static_path': os.path.join(os.path.dirname(__file__), "Foundation")}

app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/js/(.*)', JsHandler),
    (r'/ws', WebSocketHandler),
], **settings)

if __name__ == '__main__':
    parse_command_line()
    app.listen(options.port)
    print("Running server at http://localhost:"+str((options.port)))
    tornado.ioloop.IOLoop.instance().start()