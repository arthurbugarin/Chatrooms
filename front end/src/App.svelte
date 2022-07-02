<script>
	import ChatroomContainer from "./ChatroomContainer.svelte";
</script>

<main>
	<ChatroomContainer/>
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		margin: 0 10%;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>