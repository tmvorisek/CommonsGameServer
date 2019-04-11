import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import argparse
import sys
import os
from tornado.options import define, options, parse_command_line
from WebHandlers import handler, database

define("port", default=8888, help="run on the given port", type=int)
define("players", default=20, help= "number of players", type=int)

# we gonna store clients in dictionary..
clients = dict()

# message_handler = handler.Handler(args.players[0])


def broadcast(obj):
    connect_message = json.dumps(obj)
    for c in clients:
        clients[c]["object"].write_message(connect_message)

class JsHandler(tornado.web.RequestHandler):
    def get(self, script):
        self.render("Foundation/js/" + script)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        cookie = self.get_secure_cookie("commons_pass")
        if(cookie):
            self.render("Foundation/test_site.html")
        else:
            self.render("Foundation/not_allowed.html")

class LinkHandler(tornado.web.RequestHandler):
    def get(self, pass_string):
        db = handler.db
        if(db.check_pass(pass_string)):
            self.set_secure_cookie("commons_pass", pass_string.encode(), expires_days=1)
            self.redirect("/")
        else:
            self.render("Foundation/not_allowed.html")

settings = {'debug': True, 
            'cookie_secret': "Super Secret, don't get haxxed",
            'static_path': os.path.join(os.path.dirname(__file__), "Foundation")}

app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/user/(.*)', LinkHandler),
    (r'/js/(.*)', JsHandler),
    (r'/ws', handler.WebSocketHandler),
], **settings)


if __name__ == '__main__':
    parse_command_line()
    app.listen(options.port)
    print("Running server at http://localhost:"+str((options.port)))
    tornado.ioloop.IOLoop.instance().start()
