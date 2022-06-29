<script>
    import MessagesContainer from "./MessagesContainer.svelte";
    import { io } from "socket.io-client";

    const socketio = io();

    let msg = "";

    function handleSubmit(event) {
        event.preventDefault();
        socketio.emit("message", msg);
        msg = "";
    }

    function handleClick() {
        socketio.emit("message", msg);
        console.log('Message sent: ' + msg);
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


<div class="messages-container">
    <MessagesContainer socketio={socketio} />
</div>

<input id="entraMsg" bind:value={msg}>

<button id="btnMsg" on:click={handleClick}>
    Enviar
</button>

<style>
    .messages-container {
        overflow-y: scroll;
        height: 300px;
    }
</style>