<script lang="ts">
	import { onMount, createEventDispatcher } from 'svelte';
	import { copyToClipboard } from '$lib/utils';
	import Spinner from './Spinner.svelte';

	export let command = '';
	export let canRun = true;
	let running = false;
	let output = '';
	let error = '';
	let copied = false;

	const dispatch = createEventDispatcher();

	async function copyCommand() {
		copied = true;
		await copyToClipboard(command);
		setTimeout(() => (copied = false), 1000);
	}
	// Execute the command with MCP or Docker. Don't know, using a mock to test
	async function runCommand() {
		running = true;
		output = '';
		error = '';
		try {
			// Mock but waiting for Faustine job or the result of the AI model
			await new Promise((r) => setTimeout(r, 1000));
			output = `Résultat simulé pour: ${command}`;
		} catch (e) {
			error = e.message;
		}
		running = false;
		dispatch('run', { command, output, error });
	}
	// Check if the model returns shell commands
	const isShellLang = (command: string) => {
		if (!command) return false;
		const shellPatterns = [
			/^#!/,
			/\b(sudo|ls|cat|echo|cd|pwd|grep|awk|sed|chmod|chown|ps|kill|nc|nmap|curl|wget|ssh|scp|tar|find|export|ifconfig|ip|route|iptables|bash|sh|zsh|fish|powershell|cmd)\b/,
			/\b(\.\/[a-zA-Z0-9_\-\.]+|\$[a-zA-Z_][a-zA-Z0-9_]*|&&|\|\||\|)/,
			/>|<|2>|2>&1/
		];
		return shellPatterns.some((pattern) => pattern.test(command));
	};
</script>

<div class="terminal-command-block bg-gray-900 text-white rounded-lg p-4 my-2">
	<div class="flex items-center justify-between gap-2">
		<pre class="text-green-400 whitespace-pre-wrap flex-1 select-all">{command}</pre>
		<div class="flex gap-1">
			{#if isShellLang(command)}
				<button
					class="copy-btn px-2 py-1 rounded bg-gray-700 hover:bg-gray-600"
					on:click={copyCommand}
				>
					{#if copied}✅ Copied{:else}Copy{/if}
				</button>
				{#if canRun}
					<button
						class="run-btn px-2 py-1 rounded bg-blue-700 hover:bg-blue-600"
						on:click={runCommand}
						disabled={running}
					>
						{#if running}<Spinner size="xs" /> Executing...{:else}Execute{/if}
					</button>
				{/if}
			{:else}
				<button
					class="copy-btn px-2 py-1 rounded bg-gray-700 hover:bg-gray-600"
					on:click={copyCommand}
				>
					{#if copied}✅ Copied{:else}Copy{/if}
				</button>
			{/if}
		</div>
	</div>
	{#if isShellLang(command)}
		{#if running}
			<div class="mt-2 text-xs text-gray-300">Exécution en cours...</div>
		{:else if output}
			<div class="mt-2 text-xs text-green-300">
				Sortie : <pre>{output}</pre>
			</div>
		{/if}
		{#if error}
			<div class="mt-2 text-xs text-red-400">
				Erreur : <pre>{error}</pre>
			</div>
		{/if}
	{/if}
</div>

<style>
	.terminal-command-block pre {
		font-family: 'Fira Mono', 'Consolas', monospace;
		margin: 0;
	}
</style>
