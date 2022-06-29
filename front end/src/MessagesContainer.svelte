<script>
    export let socketio;
    let messages = [];

    console.log(socketio);

    socketio.on("server message", (msg) => {
        messages.push('Servidor: ' + msg);
        console.log('Server message from server: ', msg);
        messages = messages;
    });

    socketio.on("message", (msg) => {
        messages.push('Mensagem: ' + msg)
        console.log('Message from server: ', msg);
        messages = messages;
    });
</script>

{#each messages as message}
    <p>{message}</p>
{/each}