<script>
  import Table from "./Table.svelte";
</script>

<main>
  <a href="/"><h1>Wake on LAN</h1></a>
  <div><Table /></div>
  <details>
    <summary>What is this?</summary>
    <p>The above table shows devices and if they're powered on or not.</p>
    <p>Click the status buttons to refresh.</p>
    <p>Wake devices up by clicking the power buttons.</p>
  </details>
</main>
<footer>
  Powered by <a href="https://github.com/pR0Ps/simple-wol-server">simple-wol-server</a>
</footer>

<style>
  main {
    text-align: center;
    margin: auto;
  }
  h1 {
    padding: 8px;
  }
  div {
    display: table;
    padding: 8px;
    margin: auto;
  }
  footer {
    margin: 100px auto;
    text-align: center;
  }
  p {
    margin: 0.5em;
  }
</style>