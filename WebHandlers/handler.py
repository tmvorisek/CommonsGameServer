import json
import argparse
import datetime
from database import DBManager
from tornado import websocket
from GameLogic.Game import Game
from GameLogic.GameRules.GameRules import GameRules


# we gonna store clients in dictionary..
clients = dict()

# Gon parse arguments too, y'all.
parser = argparse.ArgumentParser(description='Commons game public python server.')
parser.add_argument('--players', metavar='N', type=int, nargs=1,
                    help='Number of players expected')

db = DBManager()

def broadcast(obj, round_id, game_id):
    message = json.dumps(obj, default=str)
    for c in clients:
        if clients[c]["object"].details["game_id"] == game_id:
            if clients[c]["object"].details["round_id"] >= round_id:
                clients[c]["object"].write_message(message)

def compute_game_players_counts(player_count):
    rem = player_count % 8
    groups = int(player_count / 8)
    games = []
    for i in range(0,groups):
        games.append(8)
    if (rem < 4):
        i = 0
        while rem > 0:
            games[i] += 1
            rem -= 1
            i += 1
            if i >= len(games):
                i = 0
    elif (rem >= 4):
        games.append(rem)

    print("Created Games with players counts: " + str(games))
    db.create_games(games)
    return games

class WebSocketHandler(websocket.WebSocketHandler):
    args = parser.parse_args()
    if args.players:
        compute_game_players_counts(args.players[0])

    games_list = db.load_games()
    for game_id in games_list:
        rules = GameRules("config.json")
        rules.NUM_PLAYERS = len(games_list[game_id]["players"])
        game = Game(rules, games_list[game_id]["players"])
        games_list[game_id]["game"] = game


    def on_message(self, message):        
        msg = json.loads(message);
        print(msg)
        if 'type' not in msg:
            return
        elif msg['type'] == 'chat':
            if len(msg['text']) == 0:
                return
            self.chat(msg)
        elif msg['type'] == 'name':
            if len(msg['name']) != 0:
                db.set_name(self.id, msg['name'])
                self.details['name'] = msg['name']
        elif msg['type'] == 'game_data':
            self.handleData(msg)
        elif msg['type'] == 'move':
            self.move(msg)

    def on_close(self):
        if hasattr(self, 'id'):
            del clients[self.id]

    def open(self):
        self.stream.set_nodelay(True)
        cookie = self.get_secure_cookie("commons_pass")
        if(cookie):
            self.id = db.check_pass(cookie.decode())
            clients[self.id] = {"id": self.id, "object": self}
            self.details = db.get_player_details(self.id)
            self.send(self.details)
            chat_log = db.get_chats(self.details["round_id"], self.details["game_id"])
            for round_chats in chat_log:
                for chat in round_chats:
                    obj = {
                        "type":"chat",
                        "text":chat[2],
                        "name":chat[7],
                        "time":chat[3],
                        "round_id":chat[4],
                        "player_id":chat[5],
                    }

                    self.send(obj)

    def move(self, msg):
        if self.details["move_num"] < 40:
            if msg["move"] in ["sustain","police","overharvest","invest"]:
                self.details["move_num"] += 1
                db.store_move(self.id, 
                    self.details["game_id"],
                    msg["move"])
                msg["turn"] = db.get_move_num(self.id)
                msg["player_id"] = self.id
                self.send(msg)

    def handleData(self, msg):
        data = self.db.get_round_data(msg)
        for r in data:
            self.write_message(json.dumps({"commons":r["commons_index"],"type":"ret_commons_data"}))

    def handleChat(self,msg):
        db.send_chat(msg)
        name = self.chat({"name":msg["name"],"text":msg["name"]})
        text = self.chat({"name":msg["text"],"text":msg["text"]})
        self.write_message(json.dumps({"name":name["text"],
            "text":text["text"], "type":"chat"}))

    def chat(self,msg):
        msg['player_id'] = self.id;
        msg['round_id'] = self.details['round_id']
        msg['name'] = self.details['name']
        msg['time'] = datetime.datetime.now()
        msg['text'].replace('<','').replace('>','')
        db.store_chat(msg)
        broadcast(msg,self.details['round_id'], self.details['round_id'])

    def send(self, obj):
        message = json.dumps(obj, default=str)
        self.write_message(message)

