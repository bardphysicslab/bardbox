# Bard Box Network Access

Bard Box deployments are intended for internal use and are not exposed to the 
public internet.

---

## Standard Access Model

- Raspberry Pi connected to Bard network via ethernet
- Static IP assigned in coordination with Bard IT
- Dashboard accessible on Bard internal network or via Bard VPN
- No public-facing ports

---

## Why Internal Only

- Sensor data may be sensitive
- Keeps infrastructure simple — no SSL certificates or authentication layer 
  required for the first version
- IT manages access at the network level

---

## Setting Up a New Deployment

1. Connect the Pi to the Bard ethernet network
2. Contact Bard IT to request a static IP for the device
3. Configure the static IP on the Pi using `nmcli`
4. Confirm the Pi is reachable over VPN

**Example nmcli configuration:**
```bash
sudo nmcli con mod "Wired connection 1" ipv4.addresses "10.60.10.59/24"
sudo nmcli con mod "Wired connection 1" ipv4.gateway "10.60.10.1"
sudo nmcli con mod "Wired connection 1" ipv4.dns "10.60.10.1 8.8.8.8"
sudo nmcli con mod "Wired connection 1" ipv4.method manual
sudo nmcli con up "Wired connection 1"
```

---

## Accessing the Dashboard

Users access the dashboard via browser while on the Bard network or connected 
to Bard VPN. No special software is required beyond the standard Bard VPN client.

---

## Future Consideration

As deployments grow, a centralized Bard Box portal aggregating multiple 
dashboards behind a single authenticated URL may make sense. This is out of 
scope for current deployments.
