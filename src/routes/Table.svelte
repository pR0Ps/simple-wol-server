<script>
  import Spinner from "./Spinner.svelte";
  import PingButton from "./PingButton.svelte";
  import WakeButton from "./WakeButton.svelte";
  import { parseJson } from "./response.js";

  let statuses = {};
  let promise = getHosts();

  async function getHosts() {
    return await parseJson(fetch("/api")).then((data) => {
      if (data.length == 0) {
        throw new Error("No hosts configured");
      }
      return data;
    });
  }
</script>

<table>
  <thead>
    <tr>
      <td>Computer</td>
      <td>Status</td>
      <td>Wake</td>
    </tr>
  </thead>
  <tbody>
    {#await promise}
      <tr>
        <td colspan="4"><Spinner size="30" /></td>
      </tr>
    {:then hosts}
      {#each hosts as host}
        <tr>
          <td>{host}</td>
          <td><PingButton bind:status={statuses[host]} {host} /></td>
          <td><WakeButton status={statuses[host]} {host} /></td>
        </tr>
      {/each}
    {:catch error}
      <tr>
        <td colspan="4"><p>{error.message}</p></td>
      </tr>
    {/await}
  </tbody>
</table>

<style>
  table {
    text-align: left;
    border: 1px solid black;
    border-collapse: collapse;
  }
  thead td {
    background-color: #000;
    color: #fff;
  }
  td {
    border: 1px solid black;
    padding: 8px;
  }
  p {
    color: #dc3545;
    text-align: center;
  }
</style>
