function WSSHClient() {
};

WSSHClient.prototype._generateEndpoint = function (url) {
    if (window.location.protocol == 'https:') {
        var protocol = 'wss://';
    } else {
        var protocol = 'ws://';
    }
    //var endpoint = protocol + window.location.host + '/sshwall/ws';
    var endpoint = protocol + window.location.host + url;
    return endpoint;
};

WSSHClient.prototype.connect = function (url,options) {
    var endpoint = this._generateEndpoint(url);

    if (window.WebSocket) {
        this._connection = new WebSocket(endpoint);
    }
    else if (window.MozWebSocket) {
        this._connection = MozWebSocket(endpoint);
    }
    else {
        options.onError('WebSocket Not Supported');
        return;
    }

    this._connection.onopen = function () {
        options.onConnect();
    };

    this._connection.onmessage = function (evt) {
        var data = evt.data.toString()
        options.onData(data);
    };


    this._connection.onclose = function (evt) {
        options.onClose();
    };
};

WSSHClient.prototype.send = function (data) {
    this._connection.send(JSON.stringify(data));
};

WSSHClient.prototype.sendInitData = function (server_id,width,height) {
    var data = {
        server_id: server_id,
        width:width,
        height:height
    };
    this._connection.send(JSON.stringify({"tp": "init", "data": data}))
}

WSSHClient.prototype.sendClientData = function (data,target) {
    console.log(data);
    this._connection.send(JSON.stringify({"tp": "client", "data": data,"target":target}))
}

var client = new WSSHClient();
