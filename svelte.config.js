import adapter from "@sveltejs/adapter-static";

export default {
  kit: {
    adapter: adapter({
      pages: "dist",
      fallback: "index.html",
    }),
  },
};
