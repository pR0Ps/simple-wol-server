import { writable } from "svelte/store";

export function show(type, message) {
  events.set([type, message]);
}
export const events = writable();
