import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import argparse
import sys
# import psycopg2
from tornado.options import define, options, parse_command_line

import os

# sys.path.insert(0, 'WebHandlers/')
from WebHandlers import handler



define("port", default=8888, help="run on the given port", type=int)

# we gonna store clients in dictionary..
clients = dict()

# Gon keep the db connection global as heck.
# conn = psycopg2.connect(database = "commons", 
                            # user = "postgres", 
                        # password = "pass123",
                            # host = "127.0.0.1", 
                            # port = "5432")

# Gon parse arguments too, y'all.
parser = argparse.ArgumentParser(description='Commons game public python server.')
parser.add_argument('--players', metavar='N', type=int, nargs=1,
                    help='Number of players expected')
args = parser.parse_args()
message_handler = handler.Handler(args.players[0])


def broadcast(obj):
    connect_message = json.dumps(obj)
    for c in clients:
        clients[c]["object"].write_message(connect_message)

class JsHandler(tornado.web.RequestHandler):
    def get(self, script):
        self.render("Foundation/js/" + script)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        cookie = self.get_secure_cookie("commons_pass").decode()
        self.render("Foundation/test_site.html")

class LinkHandler(tornado.web.RequestHandler):
    def get(self, pass_string):
        self.set_secure_cookie("commons_pass", pass_string.encode(), expires_days=1)
        self.redirect("/")



class WebSocketHandler(tornado.websocket.WebSocketHandler):

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
        self.stream.set_nodelay(True)
        self.id = len(clients.keys())
        message_handler.open(self.id)
        clients[self.id] = {"id": self.id, "object": self}
        
    def on_close(self):
        message_handler.close(self.id)

    def handleConnection(self, msg):
        message_handler.connection(msg)

    def handleChat(self, msg):
        msg["player_id"] = self.id
        message_handler.chat(msg)
        broadcast(msg)

    def handleMove(self):
        pass

settings = {'debug': True, 
            'cookie_secret': "Super Secret, don't get haxxed",
            'static_path': os.path.join(os.path.dirname(__file__), "Foundation")}

app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/user/(.*)', LinkHandler),
    (r'/js/(.*)', JsHandler),
    (r'/ws', WebSocketHandler),
], **settings)


if __name__ == '__main__':
    # parse_command_line()
    app.listen(options.port)
    print("Running server at http://localhost:"+str((options.port)))
    tornado.ioloop.IOLoop.instance().start()