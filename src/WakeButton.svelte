<script>
  export let host;
  export let status = null;

  import Spinner from "./Spinner.svelte";
  import IconButton from "./IconButton.svelte";

  let promise;

  async function wakeHost() {
    return await fetch("/wake", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ host: host }),
    })
      .then((resp) => {
        if (!resp.ok) {
          throw new Error(`${resp.status}: ${resp.statusText}`);
        }
        return resp.json();
      })
      .then((data) => {
        if (!data.val) {
          throw new Error(data.msg);
        }
        return data;
      })
      .catch((error) => {
        return null;
      });
  }

  function handleClick() {
    promise = wakeHost();
  }
</script>

{#await promise}
  <IconButton disabled><Spinner /></IconButton>
{:then result}
  <IconButton on:click={handleClick} disabled={status === null || status === true}>
    {#if result}
      ✓
    {:else}
      ⏻
    {/if}
  </IconButton>
{/await}