<script>
	import ChatroomContainer from "./ChatroomContainer.svelte";
</script>

<main>
	<ChatroomContainer/>
</main>

<style>
	main {
		margin: 100px;
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>