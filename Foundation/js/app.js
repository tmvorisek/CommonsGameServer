$(document).foundation()
ws = {};
id_number = Math.floor((Math.random() * 100000000) + 1)
name = ""
commons_value = "1000";
my_button = "";

function sendObject(obj) {
    json = JSON.stringify(obj);
    ws.send(json);
}

function addChat(name, message)
{
    var chat = document.getElementById("chat");
    chat.innerHTML += "<b>" + name + "</b>:" + message + "<br>";
}

function get_data() {
    var message = {
       type: "game_data"
    }
    console.log("get_data_called");
    sendObject(message);
}

function webSocketConnect() {
    ws = new WebSocket("ws://localhost:8888/ws?Id="+id_number);
    
    ws.onopen = function() {
        sendObject({type:"connect"});
    };
    ws.onmessage = function (evt) { 
        var msg = JSON.parse(evt.data);
        console.log(msg)
        if (msg["type"] == "connect"){
            addChat("Commons", "User " + msg["number"] + " Connected");
        }
        else if (msg["type"] == "chat"){
            addChat(msg["name"], msg["text"]);
        }
        else if (msg["type"] == "game_data") {
            commons_value = msg["text"];
        }
        else if (msg["type"] == "ret_commons_data") {
            console.log(msg["commons"]);
            commons_value = msg["commons"];
            document.getElementById("commons").innerText = commons_value;
        }
    };
    ws.onclose = function() { 

    };
    document.getElementById("commons").innerText = commons_value;

    document.getElementById("chat-input")
        .addEventListener("keyup", function(event) {
        event.preventDefault();
        if (event.keyCode === 13) {
            document.getElementById("submitChat").click();
        }
    });
}

function focusButton(button) {
    if (button == 1) {
        my_button = "police";
    } else if (button == 2) {
        my_button = "sus";
    } else if (button == 3) {
        my_button = "mean";
    } else if (button == 4) {
        my_button = "good";
    }
    console.log(my_button);
}

function sendButtonChoice() {
    console.log("sending choice...")
    var message = {
        text: my_button,
        type: "move"
    }
    sendObject(message);
}

function sendChat() {
    var chatEntry = document.getElementById("chat-input");
    var nameEntry = document.getElementById("name-input");
    var chatMessage = {
        text: chatEntry.value,
        name: nameEntry.value,
        type: "chat",
        id: id_number
    };
    sendObject(chatMessage);

    chatEntry.value = "";
};

function deleteAccount() {
    sendObject({type:"delete"});
}

function makeMove(){
    sendObject({type:"move"});
}

webSocketConnect();
