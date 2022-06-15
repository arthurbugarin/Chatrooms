<script>
    import { io } from "socket.io-client";

    let mensagem1 = "mensagem";
    let mensagem2 = "mensagem";
    let mensagem3 = "mensagem";
    let mensagem4 = "mensagem";
    let mensagem5 = "mensagem";

    let msg = "";
    const socketio = io();

    function passarMsgs() {
        mensagem1 = mensagem2;
        mensagem2 = mensagem3;
        mensagem3 = mensagem4;
        mensagem4 = mensagem5;
    }

    socketio.on("message", (msg) => {
        passarMsgs();
        mensagem5 = msg;
        console.log('Message from server: ', msg);
    });


    socketio.on("server message", (msg) => {
        passarMsgs();
        mensagem5 = msg;
        console.log('Server message from server: ', msg);
    });

    function handleSubmit(event) {
        event.preventDefault();
        socketio.emit("message", msg);
        msg = "";
    }

    function handleClick() {
        socketio.emit("message", msg);
        passarMsgs();
        mensagem5 = 'Enviado: '.concat(msg);
    }

    var input = document.getElementById("entraMsg");
    if(input){
        input.addEventListener("keyup", function(event) {
            // Number 13 is the "Enter" key on the keyboard
            if (event.keyIdentifier === 13) {
                // Cancel the default action, if needed
                event.preventDefault();
                // Trigger the button element with a click
                document.getElementById("btnMsg").click();
            }
        });
    }
</script>

<main>
    <p>container</p>
    <p>{mensagem1}</p>
	<p>{mensagem2}</p>
	<p>{mensagem3}</p>
	<p>{mensagem4}</p>
	<p>{mensagem5}</p>

	<input id="entraMsg" bind:value={msg}>

	<button id="btnMsg" on:click={handleClick}>
		Enviar
	</button>
</main>
