<script>
  export let host;
  export let status = null;

  import Spinner from "./Spinner.svelte";
  import IconButton from "./IconButton.svelte";
  import { show } from "./alert.js";
  import { parseJson } from "./response.js";

  let promise;

  async function wakeHost() {
    let url = new URL(`/api/${host}`, location.href);
    return await parseJson(fetch(url, { method: "POST" }))
      .then((_) => {
        show("message", `Sent a WoL packet to ${host}`);
        return true;
      })
      .catch((error) => {
        show("err", error);
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
  <IconButton
    on:click={handleClick}
    disabled={status === null || status === true}
  >
    {#if result}
      ✓
    {:else}
      ⏻
    {/if}
  </IconButton>
{/await}
