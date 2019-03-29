import json
import argparse
from database import DBManager
from tornado import websocket


# we gonna store clients in dictionary..
clients = dict()

# Gon parse arguments too, y'all.
parser = argparse.ArgumentParser(description='Commons game public python server.')
parser.add_argument('--players', metavar='N', type=int, nargs=1,
                    help='Number of players expected')

def broadcast(obj):
    connect_message = json.dumps(obj)
    for c in clients:
        clients[c]["object"].write_message(connect_message)

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
    return games

class WebSocketHandler(websocket.WebSocketHandler):
    args = parser.parse_args()
    if args.players[0]:
        games_arr = compute_game_players_counts(args.players[0])
    db = DBManager()
    db.create_games(games_arr)

    def setup(self, player_count, params = {}):
        games_arr = self.compute_game_players_counts(player_count)

    def on_message(self, message):        
        msg = json.loads(message);
        if 'type' not in msg:
            return
        elif msg['type'] == 'chat':
            if len(msg['name']) == 0 or len(msg['text']) == 0:
                return
            self.handleChat(msg)
        elif msg['type'] == 'connect':
            self.connection(msg)

    def on_close(self):
        print("hey guys!")
        message_handler.close(self.id)

    def open(self):
        self.stream.set_nodelay(True)
        self.id = len(clients.keys())
        clients[self.id] = {"id": self.id, "object": self}
  
  
    def close(self, id):
        pass


    def connection(self, msg):
        pass
        # cursor.execute("""SELECT player.name, text, time 
            # FROM chat 
            # INNER JOIN player ON player.id = chat.player_id 
            # ORDER BY time ASC LIMIT 1000;""")
        # chat_log = cursor.fetchall()
        # for log in chat_log:
        # self.write_message(json.dumps({"name":log[0], "text":log[1], "type":"chat"}))


    def move(self, msg):
        pass

    def chat(self,msg):
        """

        > handle_chat({"player_id":"12", "text": "hey guys, sup?"})
        
        """
        if len(msg["text"]) > 0:
            msg["text"] = msg["text"].replace("<","")

            return msg
        return {}

