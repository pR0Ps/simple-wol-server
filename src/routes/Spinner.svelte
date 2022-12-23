<script>
  export let size = 25;
</script>

<div style="width:{size}px; height:{size}px; border-width:{size / 5}px" />

<style>
  @keyframes spinner {
    to {
      transform: rotate(360deg);
    }
  }
  div {
    display: block;
    margin: auto;
    border-color: black;
    border-style: solid;
    border-right-color: transparent;
    border-radius: 50%;
    animation: spinner 0.75s infinite linear;
  }
</style>
