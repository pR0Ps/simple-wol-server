<script>
  import { events } from "./alert";
  import { onDestroy } from "svelte";
  import { fly } from "svelte/transition";

  const ALERT_TIMEOUT = 5; // seconds to display the alert

  let msg;
  let color;
  let visible = false;
  let timerId;

  const unsubscribe = events.subscribe((value) => {
    if (value != undefined) {
      let type;
      [type, msg] = value;
      if (type == "err") {
        color = "red";
      } else {
        color = "white";
      }

      // set to invisible and back to re-display the bar
      visible = false;
      setTimeout(() => (visible = true), 100);
    }
  });

  $: if (visible === true) {
    clearTimeout(timerId);
    timerId = setTimeout(() => {
      visible = false;
    }, ALERT_TIMEOUT * 1000);
  }

  onDestroy(() => {
    clearTimeout(timerId);
    unsubscribe();
  });
</script>

{#if visible}
  <div
    class="snackbar"
    in:fly={{ y: 50, duration: 350 }}
    out:fly={{ y: 50, duration: 350 }}
  >
    <div style="color: {color}" class="message">{msg}</div>
  </div>
{/if}

<style>
  .snackbar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
  }
  .message {
    display: inline-block;
    padding: 20px;
    background: black;
  }
</style>
