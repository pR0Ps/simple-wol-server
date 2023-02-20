<script>
  export let host;
  export let status = null;

  import Spinner from "./Spinner.svelte";
  import IconButton from "./IconButton.svelte";
  import { show } from "./alert.js";
  import { parseJson } from "./response.js";

  let promise = getHostStatus(false);

  async function getHostStatus(showMsg = true) {
    status = null;

    let url = new URL(`/api/${host}`, location.href);
    return await parseJson(fetch(url))
      .then((data) => {
        if (data.status == null) {
          throw new Error(`Invalid response when checking host '${host}'`);
        }
        if (showMsg) {
          show("message", `Host '${host}' is ${data.status ? "up" : "down"}`);
        }
        status = data.status;
      })
      .catch((error) => {
        show("err", error);
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
  <IconButton
    on:click={handleClick}
    color={status ? "green" : status === null ? "" : "red"}>↻</IconButton
  >
{/await}

<slot {status} />
