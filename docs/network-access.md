# Bard Box Network Access

Bard Box deployments are intended for internal use and are not exposed to the public internet.

---

## Standard Access Model

* Raspberry Pi connected to Bard network via ethernet
* Static IP assigned in coordination with Bard IT
* Dashboard accessible on Bard internal network or via Bard VPN
* No public-facing ports

---

## Why Internal Only

* Sensor data may be sensitive
* Keeps infrastructure simple — no SSL certificates, authentication layers, or firewall configuration required for initial deployments
* Access control is handled by Bard IT at the network level

---

## Setting Up a New Deployment

1. Connect the Pi to the Bard ethernet network
2. Request a static IP from Bard IT
3. Configure the static IP on the Pi
4. Verify connectivity from both:

   * Bard internal network
   * Bard VPN

### Example (`nmcli`) Configuration

```bash
sudo nmcli con mod "Wired connection 1" ipv4.addresses "10.60.10.59/24"
sudo nmcli con mod "Wired connection 1" ipv4.gateway "10.60.10.1"
sudo nmcli con mod "Wired connection 1" ipv4.dns "10.60.10.1 8.8.8.8"
sudo nmcli con mod "Wired connection 1" ipv4.method manual
sudo nmcli con up "Wired connection 1"
```

Notes:

* Connection name (`"Wired connection 1"`) may vary — confirm with `nmcli con show`
* Use values provided by Bard IT (IP, gateway, DNS)

---

## Accessing the Dashboard

Users access the dashboard via a web browser while:

* connected to the Bard network, or
* connected through Bard VPN

No additional software is required beyond the standard Bard VPN client for
dashboard access.

## Remote administration with Tailscale

Tailscale is the recommended remote-management path for Raspberry Pi
deployments. It is additive: existing Ethernet, static addressing, LAN access,
and Bard VPN access remain intact.

Install and enroll the Pi according to the approved deployment account:

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

Prefer the Pi's MagicDNS hostname over a numeric Tailscale address. Administrators
may create convenient local aliases such as `ssh cesh`, `ssh solar`, `ssh rkc`,
or `ssh golab`, but hostnames, addresses, usernames, and keys belong in each
administrator's local `~/.ssh/config`, never in a shared repository or app
configuration.

---

## Operational Rules

* Do not expose Bard Box services to the public internet
* Do not open external ports or configure port forwarding
* Do not bypass Bard IT network policies
* Treat the Pi as an internal infrastructure device, not a public server
* Keep Tailscale additive; do not remove working LAN/VPN networking
* Do not commit administrator-specific SSH aliases, hosts, addresses, or keys

---

## Future Considerations

As deployments grow, a centralized Bard Box portal aggregating multiple dashboards behind a single authenticated interface may be useful.

This is out of scope for current deployments.

## Optional authenticated campus dashboards

A project may add HTTPS authentication for campus/VPN viewers while preserving
internal-only network access. Authentication does not authorize public exposure
or routing campus clients onto the sensor network.

- Separate read-only viewers from administrators. Enforce roles on every route,
  including legacy control endpoints, logs and generated API documentation.
- Require a configured HTTPS origin and trusted proxy boundary. Bind the app to
  loopback; trust forwarded headers only from the local proxy. Keep credentials
  outside Git and reject incomplete enabled configuration.
- Browser mutations require same-origin checks and a custom request header;
  Basic authentication alone does not prevent cross-site requests.
- Keep a minimal side-effect-free local health endpoint for the watchdog.
- Provider webhooks need their own signature verification; browser credentials
  are not a substitute. An outbound-polling deployment can explicitly disable
  unused inbound webhook routes.
- Document the campus/VPN allowlist, certificate ownership, sensor interface
  isolation, credential rotation and rollback before deploying. Check actual
  IPv4 and IPv6 reachability with Bard IT; never infer firewall safety from code.

The optional template `software/app/dashboard_access.py` provides a small access
boundary; projects supply their environment prefix, viewer routes and disabled
webhooks. RKC is the first consumer. CESH's ingestion and OTA authentication are
separate contracts and do not automatically adopt this dashboard gate. No
firmware or measurement protocol changes are required. Existing AI skill
propagation guidance covers this capability; no skill rewrite is needed.
