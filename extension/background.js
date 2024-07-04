chrome.downloads.onCreated.addListener(function(downloadItem) {
    var socket = new WebSocket('ws://localhost:8000');
    socket.onopen = function(event) {
        socket.send(JSON.stringify(downloadItem));
    };
});

