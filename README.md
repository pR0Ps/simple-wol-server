simple-wol-server
=================
A simple web server for sending Wake-on-LAN packets.

Built using [SvelteKit](https://kit.svelte.dev/)

![Screenshot](./screenshot.png)

Deploying
=========

1. Clone the repo
2. Configure the backend: Edit `routes/api/[[host]]/+server.js` and add your
   hostnames and MAC addresses to the `HOSTS` dictionary.
3. Install dependencies: `npm install`
4. Build application: `npm run build` (will generate a `build` folder)
5. To verify it works, run the application locally with: `HOST=127.0.0.1 PORT=3000 node build/`
6. Use the included `simple-wol-server.service` to have the project run at startup, restart if it fails, etc.

Development
===========

1. Install dependencies: `npm install`
2. Run the development server: `npm run dev`
3. Open the application in a browser to test it

Licence
=======
Licensed under the [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html)
