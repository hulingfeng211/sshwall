function openTerminal(server_id) {
    var client = new WSSHClient();
    var size=getTerminalSize()
    
    var term = new Terminal({cursorBlink:true, screenKeys: true, useStyle: true,rows:size.h,cols:size.w});
    //var fitAddon = Terminal.loadAddon('fit');
    term.on('data', function (data) {
        client.sendClientData(data,server_id);
    });
    var terminalParent = document.getElementById('terminal');
    //var terminal_container=$('#terminal')
    term.open(terminalParent,true);
    //$('.terminal').detach().appendTo('#terminal');
    //$("#terminal").show();
    //term.toggleFullscreen();
    term.toggleFullscreen(true);  
    //console.log(term.getOption('rows'))
    //console.log(term.getOption('cols'))
    //term.fit();
    //term.focus();
    //fitAddon.fit(term); 
    term.write('Connecting...');
    client.connect({
        onError: function (error) {
            term.write('Error: ' + error + '\r\n');
            console.debug('error happened');
        },
        onConnect: function () {
            client.sendInitData(server_id,size.w,size.h);
            client.sendClientData('\r',server_id);
            term.focus();
            console.debug('connection established');
        },
        onClose: function () {
            term.write("\rconnection closed")
            console.debug('connection reset by peer');
            $('term').hide()
        },
        onData: function (data) {
            term.write(data);
            console.debug('get data:' + data);
        }
    })
}

var charWidth = 10.2;
var charHeight = 25.2;

/**
 * for full screen
 * @returns {{w: number, h: number}}
 */
function getTerminalSize() {
    var width = window.innerWidth;
    var height = window.innerHeight;
    return {
        w: Math.floor(width / charWidth),
        h: Math.floor(height / charHeight)
    };
}

function connect(server_id) {
    openTerminal(server_id)
}