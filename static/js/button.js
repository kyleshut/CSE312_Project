
    const socket = io.connect();

    $(document).ready(function (){
        socket.on('connect',function (){
        socket.emit('load_counter');
        });

        socket.on('receive_counter', function (data){
             document.getElementById('counter').innerHTML = data;
        });

        $("#btn1").click(sendMessage);
        function sendMessage() {
             socket.emit('button_click');
        }
    });
