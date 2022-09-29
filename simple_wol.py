#!/usr/bin/env python

import functools
import logging
import socket
import subprocess
import time

from flask import Flask, request, send_from_directory
from wakeonlan import send_magic_packet


HOSTS = {
    # fill in your servers
    "server1.lan": "MM:MM:MM:MM:MM:MM", # not a real mac address
}


__log__ = logging.getLogger(__name__)

app = Flask(__name__)


def ttl_lru_cache(ttl=None, maxsize=128, typed=False):
    """functools.lru_cache with a timeout

    Works by automatically adding an ignored timestamp to the args that
    causes the args to change every interval, busting the cache.
    """
    if ttl is None:
        return functools.lru_cache(maxsize=maxsize, typed=typed)

    def wrapper(func):
        @functools.lru_cache(maxsize=maxsize, typed=typed)
        def orig(*args, __time_salt, **kwargs):
            return func(*args, **kwargs)

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            return orig(*args, **kwargs, __time_salt=time.time() // ttl)

        return wrapped

    return wrapper


@ttl_lru_cache(ttl=3600)
def resolve_hostname(host):
    try:
        return socket.gethostbyname(host)
    except socket.error:
        __log__.error("Failed to resolve '%s'", host, exc_info=True)
        return None


@ttl_lru_cache(ttl=5)
def is_up(host):
    try:
        subprocess.run(
            ["ping", "-c", "1", "-w", "1", host],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=2
        ).check_returncode()
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return False
    return True


@app.route("/")
@app.route("/<path:path>")
def root(path="index.html"):
    """Serves the JS application"""
    return send_from_directory("static", path)


@app.route("/api/hosts")
def hosts():
    return {
        "val": list(HOSTS),
        "msg": f"{len(HOSTS)} hosts available"
    }


@app.route("/api/check")
def check():
    if not (host := request.args.get("host")) or host not in HOSTS:
        return {
            "val": None,
            "msg": host and f"Invalid host '{host}'" or "No host specified"
        }

    if not (ip := resolve_hostname(host)):
        return {
            "val": None,
            "msg": f"Failed to resolve '{host}' to an IP"
        }

    try:
        up = is_up(ip)
    except Exception:
        __log__.error("Failed to ping '%s' (%s)", host, ip, exc_info=True)

        return {
            "val": None,
            "msg": f"Failed to ping '{host}'"
        }

    return {
        "val": up,
        "msg": f"Host '{host}' is {'up' if up else 'down'}"
    }


@app.route("/api/wake", methods=["POST"])
def wake():
    if not (data := request.json) or (host := data.get("host")) not in HOSTS:
        return {
            "val": False,
            "msg": "Missing/invalid host"
        }

    try:
        send_magic_packet(HOSTS[host])
    except Exception:
        __log__.error(
            "Failed to send WOL packet to '%s' (%s)",
            host, HOSTS[host],
            exc_info=True
        )
        return {
            "val": False,
            "msg": f"Failed to send wake on LAN packet to '{host}'"
        }

    __log__.info("Sent WOL packet to '%s' (%s)", host, HOSTS[host])

    return {
        "val": True,
        "msg": f"Sent wake on LAN packet to {host}."
    }


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
