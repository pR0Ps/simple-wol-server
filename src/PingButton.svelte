<script>
  export let host;
  export let status = null;

  import Spinner from "./Spinner.svelte";
  import IconButton from "./IconButton.svelte";

  let promise = getHostStatus();

  async function getHostStatus() {
    status = null;

    let url = new URL("/check", location.href);
    url.searchParams.append("host", host);
    return await fetch(url)
      .then((resp) => {
        if (!resp.ok) {
          throw new Error(`${resp.status}: ${resp.statusText}`);
        }
        return resp.json();
      })
      .then((data) => {
        if (data.val == null) {
          throw new Error(data.msg);
        }
        status = data.val;
      })
      .catch((error) => {
        status = null;
      });
  }

  function handleClick() {
    promise = getHostStatus();
  }
</script>

{#await promise}
  <IconButton disabled><Spinner /></IconButton>
{:then}
  <IconButton on:click={handleClick} color={status ? "green" : status === null ? "" : "red"}>↻</IconButton>
{/await}

<slot {status} />