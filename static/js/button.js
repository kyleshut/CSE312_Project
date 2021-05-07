
    // const socket = io.connect("http://127.0.0.1:5000");
    const socket = io.connect("http://cse312-05.dcsl.buffalo.edu");

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
