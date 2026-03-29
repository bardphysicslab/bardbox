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

No additional software is required beyond the standard Bard VPN client.

---

## Operational Rules

* Do not expose Bard Box services to the public internet
* Do not open external ports or configure port forwarding
* Do not bypass Bard IT network policies
* Treat the Pi as an internal infrastructure device, not a public server

---

## Future Considerations

As deployments grow, a centralized Bard Box portal aggregating multiple dashboards behind a single authenticated interface may be useful.

This is out of scope for current deployments.
