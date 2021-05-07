
    const socket = io.connect("http://cse312-05.dcsl.buffalo.edu");

    function insert_connected(data){
        var tag = document.createElement("p");
        var text = document.createTextNode(data +" is online");
        tag.appendChild(text);
        var element = document.getElementById("online");
        element.appendChild(tag);
    }
    function insert_disconnected(data){
        var tag = document.createElement("p");
        var text = document.createTextNode(data +" disconnected");
        tag.appendChild(text);
        var element = document.getElementById("online");
        element.appendChild(tag);
    }

    $(document).ready(function (){
        socket.on('connect',function (){
            socket.emit("loadOnline");
        });

        socket.on('renderOnline', function (data){
             for (const key in data) {
                 insert_connected(key);
             }
        });

        socket.on('join', function (data) {
            insert_connected(data);
        });
        socket.on("disconnect", function () {
            socket.emit("disconnected");
        });
        socket.on("remove_dis",function (data){
           insert_disconnected(data)
        });

        $('#send_private_message').click(private_button);
            function private_button() {
                var recipient = document.getElementById('send_to_username').value
                var message =document.getElementById('private_message').value
                socket.emit('private_message', {"username": recipient, "message": message});
            }

        socket.on("new_private_message",function (msg){
            alert(msg);
        });
    });
