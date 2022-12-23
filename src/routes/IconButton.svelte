<script>
  export let disabled = false;
  export let color = null;
</script>

<button on:click {disabled} class={color}>
  <slot default />
</button>

<style>
  button {
    display: block;
    margin: auto;
    width: 50px;
    height: 50px;
    padding: 0px;
    font-size: 18pt;
  }

  button.green {
    color: #fff;
    background-color: #198754;
    border-color: #198754;
  }
  button.red {
    color: #fff;
    background-color: #dc3545;
    border-color: #dc3545;
  }
</style>
