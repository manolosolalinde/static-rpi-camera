document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
    socket.on('connect', () => {

        // Each change emits a "switch change" event
        document.querySelector("#onoff").onclick = function () {
            socket.emit('switch change', { [this.id]: this.checked });
        };

        // Each change emits a "switch change" event
        document.querySelector("#recording").onclick = function () {
            socket.emit('switch change', { [this.id]: this.checked });
        };

        document.querySelector("#init_message").innerHTML = '';

    });

    document.querySelector('#resolution').onchange = function () {
        console.log(this.value)
        socket.emit('resolution change', { resolution: this.value })
    }

    // document.querySelectorAll('button').forEach(button => {
    //     button.onclick = () => {
    //         const selection = button.dataset.vote;
    //         socket.emit('submit vote', {'selection': selection});
    //     };
    // });

    // When a new vote is announced, add to the unordered list
    socket.on('update switches', data => {
        document.querySelector('#onoff').checked = data.onoff;
        document.querySelector('#recording').checked = data.recording;
        document.getElementById("video_source").src = window.location.protocol + '//' + window.location.hostname + ':8000' + '/stream.mjpg';
        document.getElementById("video_source").onerror = 'this.onerror=null;this.src="image.jpg"'
        document.getElementById("video_source2").src = window.location.protocol + '//' + data.peer_hostname + ':8000' + '/stream.mjpg';
        document.getElementById("video_source2").onerror = 'this.onerror=null;this.src="image.jpg"'
        document.getElementById("video_source2").hidden = data.hide_peer;
    });

    socket.on('resolution change', data => {
        document.querySelector("#resolution").value = data.resolution
    });

    socket.on('initial message', init_message => {
        document.getElementById('init_message').innerHTML = init_message;
    });
});
