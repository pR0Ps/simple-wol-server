import { error, json } from "@sveltejs/kit";
import { default as dns } from "dns";
import { exec } from "child_process";
import { default as send_wol } from "wakeonlan";

const HOSTS = {
  // fill in your servers
  "server1.lan": "MM:MM:MM:MM:MM:MM",
};

// Use ping to check if a host is up
// TODO: caching
async function is_up(host) {
  return await new Promise((resolve, reject) => {
    exec(`ping -c 1 -w 1 -- ${host}`, (error, stdout, stderr) => {
      if (error) {
        reject();
      } else {
        resolve();
      }
    });
  })
    .then(() => {
      return true;
    })
    .catch(() => {
      return false;
    });
}

// Handle returning the list of hosts and checking if a specific host is up
export async function GET({ params }) {
  const host = params.host;
  if (!host) {
    return json(Object.keys(HOSTS));
  } else if (!HOSTS[host]) {
    throw error(404, `Unknown host '${host}'`);
  }

  let ip = await dns.promises
    .lookup(host)
    .then((result) => {
      return result.address;
    })
    .catch((error) => {
      console.error(`Failed to resolve '${host}': ${error}`);
      return null;
    });

  if (!ip) {
    throw error(500, `Failed to resolve '${host}`);
  }
  return json({
    status: await is_up(ip),
  });
}

// Handle sending the WoL packet to the provided host
export async function POST({ params }) {
  const host = params.host;
  if (!host) {
    throw error(400, `Host to wake not provided`);
  }

  const mac = HOSTS[host];
  if (!mac) {
    throw error(404, `Unknown host '${host}'`);
  }

  // TODO: rate limiting
  return send_wol(mac)
    .then(() => {
      return json({});
    })
    .catch((err) => {
      console.error(`Failed to send WoL packet: ${err}`);
      throw error(500, `Failed to send WoL packet to '${host}'`);
    });
}
