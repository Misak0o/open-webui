<script lang="ts">
	import Terminal from '$lib/components/common/Terminal.svelte';
</script>

<h1 class="text-xl font-bold mb-4">Test du composant CommandBlock</h1>

<Terminal command="ls" canRun={true} />
