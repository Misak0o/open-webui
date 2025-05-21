<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import CodeEditor from '$lib/components/common/CodeEditor.svelte';
	import { copyToClipboard } from '$lib/utils';

	const dispatch = createEventDispatcher();

	export let id = '';
	export let save = false;
	export let run = true;
	export let code = '';
	export let lang = 'bash';

	let _code = code;
	let stdout = '';
	let stderr = '';
	let copied = false;
	let executing = false;

	async function handleCopy() {
		await copyToClipboard(_code);
		copied = true;
		setTimeout(() => (copied = false), 1000);
	}

	function handleRun() {
		executing = true;
		stdout = '';
		stderr = '';

		setTimeout(() => {
			if (_code.includes('error')) {
				stderr = 'Command not found: error';
			} else {
				stdout = `Executed: ${_code}`;
			}
			executing = false;
		}, 1000);
	}

	function handleSave() {
		dispatch('save', _code);
	}

	function handleEdit(newCode: string) {
		_code = newCode;
		dispatch('code', newCode);
	}
</script>

<div class="relative my-4 border border-gray-300 dark:border-gray-700 rounded-md overflow-hidden">
	<div
		class="flex items-center justify-between px-3 py-2 bg-gray-100 dark:bg-gray-800 text-sm font-mono"
	>
		<span class="text-gray-600 dark:text-gray-300">{lang}</span>
		<div class="flex gap-2">
			{#if run}
				<button
					class="hover:text-green-600"
					on:click={handleRun}
					disabled={executing}
					title="Exécuter"
				>
					▶️
				</button>
			{/if}
			<button class="hover:text-blue-600" on:click={handleCopy} title="Copier">
				{#if copied}
					✅
				{:else}
					📋
				{/if}
			</button>
			{#if save}
				<button class="hover:text-orange-600" on:click={handleSave} title="Sauvegarder">
					💾
				</button>
			{/if}
		</div>
	</div>

	<div class="bg-black text-white p-2 text-sm font-mono">
		<CodeEditor code={_code} {lang} readOnly={false} on:edit={(e) => handleEdit(e.detail)} />
	</div>

	{#if executing}
		<div class="p-2 text-yellow-400 font-mono bg-yellow-900">⏳ Exécution en cours...</div>
	{:else if stdout}
		<div class="p-2 text-green-400 font-mono bg-gray-900 whitespace-pre-line">{stdout}</div>
	{:else if stderr}
		<div class="p-2 text-red-400 font-mono bg-gray-900 whitespace-pre-line">{stderr}</div>
	{/if}
</div>

<style>
	button:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}
</style>
