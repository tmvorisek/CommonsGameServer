$(document).foundation()
ws = {};
id_number = Math.floor((Math.random() * 100000000) + 1)
name = ""
commons_value = "1000";
my_button = "";
max_round = "";

function sendObject(obj) {
    json = JSON.stringify(obj);
    ws.send(json);
}

function initPage(msg) 
{
    max_round = msg["max_round"];
    $("#commons-index").text(parseFloat(msg["commons_index"]).toFixed(1));
    $("#summit-index").text(msg["summit_num"]);
    $("#round-index").text(msg["active_round"] + "/" + msg["max_round"]);
    $("#wealth").text(msg["wealth"]);
    $("#player-id").text(msg["player_id"]);
    populate_players_table(msg["players"]);
}

function addChat(player_id, name, message)
{
    var chat = document.getElementById("chat");
    chat.innerHTML += "<b>("+ player_id + ") " + name + "</b> " + message + "<br>";
}

function addError(message)
{
    var error = $("#Error")
    error.append("<h2>Error:</h2><p><h3>"+message["message"]+"</h3>")
    error.foundation('open');
}

function populateScoreboard(scoreboard) 
{
    html_string = ""
    for (summit = 0; summit < scoreboard.length; summit++){
        console.log(summit)
        for (round = 0; round < scoreboard[summit].length; round++){
            console.log("  " + round)
            html_string += "<tr><td>Turn " + ((round + 1) + (summit*max_round)) + "</td>";
            for (move = 0; move < scoreboard[summit][round].length; move++){
                m = ""
                m = scoreboard[summit][round][move];
                console.log("    " + m)
                if (m == "")
                    m = "myclear";
                html_string += "<td><div class='mybox " + m + "'></div></td>";
            }
            html_string += "</tr>"
        }
    }
        $("#moves-list").append(html_string);
}

function addMove(msg) {
    $("#round-index").text(msg["round_index"] + "/" + max_round)
    color = ""
    if (msg["move"] == "sustain") {color = "mygreen";}
    else if (msg["move"] == "police") {color = "myblue";}
    else if (msg["move"] == "overharvest") {color = "myred";}
    else if (msg["move"] == "invest") {color = "myOrange";};
    html_string = 
        "<tr>" +
            "<td>Turn 1</td>" +
            "<td><div class='mybox " + color + "'></div></td>" +
            "<td><div class='mybox myclear'></div></td>" +
            "<td><div class='mybox myclear'></div></td>" +
            "<td><div class='mybox myclear'></div></td>" +
            "<td><div class='mybox myclear'></div></td>" +
            "<td><div class='mybox myclear'></div></td>" +
            "<td><div class='mybox myclear'></div></td>" +
        "</tr>";
    $("#moves-list").append(html_string);
}

function populate_players_table(players) {
    html_string = "<tr><th class='player-heading'>Turns</th>";

    for (player in players) {
        p = players[player];
        html_string += "<th class='player-heading'>" + p[0] + " ";
        if (p[1]) html_string += "[" + p[1] + "]";
        html_string += "</th>";
    }
    html_string += "</tr>\n";
    $("#players-list").append(html_string);
}

function webSocketConnect() {
    ws = new WebSocket("ws://localhost:8888/ws");
    
    ws.onopen = function() {
        sendObject({type:"connect"});
    };
    ws.onmessage = function (evt) { 
        var msg = JSON.parse(evt.data);
        console.log(msg)
        if (msg["type"] == "connection"){
            initPage(msg);
        }
        else if (msg["type"] == "chat"){
            addChat(msg["player_id"], msg["name"], msg["text"]);
        }
        else if (msg["type"] == "move"){
            addMove(msg);
        }
        else if (msg["type"] == "game_data") {
            commons_value = msg["text"];
        }
        else if (msg["type"] == "error") {
            addError(msg);
        }
        else if (msg["type"] == "scoreboard") {
            populateScoreboard(msg["scoreboard"]);
        }
    };
    ws.onclose = function() { 
        // uncomment to delete cookie access on disconnect.
        // document.cookie = 'commons_pass=;Max-Age=-99999999;';
    };

    document.getElementById("chat-input")
        .addEventListener("keyup", function(event) {
            event.preventDefault();
            if (event.keyCode === 13) {
                document.getElementById("submitChat").click();
            }
        });

    document.getElementById("name-input")
        .addEventListener("keyup", function(event) {
            event.preventDefault();
            if (event.keyCode === 13) {
                document.getElementById("submit-name").click();
            }
        });
}

function sendChat() {
    var chatEntry = document.getElementById("chat-input");
    var chatMessage = {
        text: chatEntry.value,
        type: "chat"
    };
    sendObject(chatMessage);

    chatEntry.value = "";

};

function sendName() {
    $('#Name-Modal').foundation('close');
    var nameEntry = document.getElementById("name-input");
    sendObject({
        name: nameEntry.value,
        type: "name"
    });
    nameEntry.value = "";
}

activeMove = null
function makeMove(){
    if(activeMove) {
        sendObject({type:"move",
            "move":activeMove});
    }
    $("#move-button").removeAttr("class");
    $("#move-button").addClass(defaultMoveClass);
    $("#move-button").addClass("secondary");
    activeMove = null;
}

defaultMoveClass = $("#move-button").attr("class");
$("#move-button").addClass("secondary");
function changeMoveButton(color) {
    activeMove = color
    $("#move-button").removeAttr("class");
    $("#move-button").addClass(defaultMoveClass);
    $("#move-button").addClass(color);
}



webSocketConnect();
