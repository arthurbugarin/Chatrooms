<script>
	let mensagem1 = "mensagem";
	let mensagem2 = "mensagem";
	let mensagem3 = "mensagem";
	let mensagem4 = "mensagem";
	let mensagem5 = "mensagem";

	let msg = "";
	const socket = new WebSocket("ws://127.0.0.1:1487");

	function passarMsgs() {
		mensagem1 = mensagem2;
		mensagem2 = mensagem3;
		mensagem3 = mensagem4;
		mensagem4 = mensagem5;
	}

	function handleClick() {
		socket.send(msg);
		passarMsgs();
		mensagem5 = 'Enviado: '.concat(msg); 		
	}	

	// Listen for messages
	socket.addEventListener('message', function (event) {
		console.log('Message from server: ', event.data);
		passarMsgs();
		mensagem5 = event.data;
	});

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

	// Connection opened
	socket.addEventListener('open', function (event) {
		// socket.send('Hello Server!');
		mensagem5 = "Servidor: Olá! Seja bem vindo ao chat. Insira seu nome digitando /nome [seu nome] para entrar na conversa";
	});

</script>

<main>
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

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>