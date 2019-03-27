$(document).foundation()
ws = {};
id_number = Math.floor((Math.random() * 100000000) + 1)
name = ""



function sendObject(obj) {
    json = JSON.stringify(obj);
    ws.send(json);
}

function addChat(name, message)
{
    var chat = document.getElementById("chat");
    chat.innerHTML += "<b>" + name + "</b> " + message + "<br>";
}

function webSocketConnect() {
    ws = new WebSocket("ws://localhost:8888/ws?Id="+id_number);
    // var name_entry = document.getElementById("name-input");
    // var chat_entry = document.getElementById("chat-input");
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
    };
    ws.onclose = function() { 

    };
    document.getElementById("chat-input")
        .addEventListener("keyup", function(event) {
        event.preventDefault();
        if (event.keyCode === 13) {
            document.getElementById("submitChat").click();
        }
    });
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
