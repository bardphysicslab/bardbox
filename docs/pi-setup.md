# Bard Box — Raspberry Pi Setup Guide

## Purpose

Step-by-step preparation of a Raspberry Pi for a Bard Box deployment.

Complete these steps in order before deploying any Bard Box application.

---

## 1. Base OS

Install **Raspberry Pi OS Lite (64-bit)** using Raspberry Pi Imager.

Recommended settings in Imager before flashing:
- Set hostname (e.g. `golab-pi`)
- Create a user account (e.g. `golab`)
- Enable SSH
- Set locale and timezone

---

## 2. SSH Access

After first boot, verify SSH access from your Mac:

```bash
ssh golab@<pi-ip>
```

Set up passwordless SSH from your Mac:

```bash
ssh-copy-id golab@<pi-ip>
```

Add a shortcut to `~/.ssh/config` on your Mac:

```
Host golab
  HostName <pi-ip>
  User golab
```

Then connect with simply `ssh golab`.

---

## 3. System Update

```bash
sudo apt update && sudo apt upgrade -y
sudo apt autoremove -y
```

---

## 4. NTP / Time Synchronization

All Bard Box systems must maintain synchronized time. Install and configure
`chrony`:

```bash
sudo apt install chrony -y
sudo systemctl enable chrony
sudo systemctl start chrony
```

Verify sync status:

```bash
chronyc tracking
```

The `System time` offset should be well under 1 second. Target accuracy is
±100 ms or better. See `reading-format.md` for the time synchronization
requirement.

---

## 5. Timezone

Set the correct timezone:

```bash
sudo timedatectl set-timezone America/New_York
```

Verify:

```bash
timedatectl
```

---

## 6. Networking / Static IP

Assign a static IP in coordination with Bard IT.

Configure via `nmcli`:

```bash
sudo nmcli con mod "Wired connection 1" ipv4.addresses "<ip>/24"
sudo nmcli con mod "Wired connection 1" ipv4.gateway "<gateway>"
sudo nmcli con mod "Wired connection 1" ipv4.dns "<bard-dns> 8.8.8.8"
sudo nmcli con mod "Wired connection 1" ipv4.method manual
sudo nmcli con up "Wired connection 1"
```

See `network-access.md` for the full network access model and IT coordination
requirements.

---

## 7. Python Virtual Environment

Install Python dependencies:

```bash
sudo apt install python3-pip python3-venv -y
```

Create a virtual environment in the project directory:

```bash
cd ~/golab-monitor
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 8. Repo and Config Placement

Clone the application repo:

```bash
git clone https://github.com/bardphysicslab/<repo>.git ~/golab-monitor
```

Place deployment-specific config files (e.g. `cleanroom_standards.json`) in:

```
~/golab-monitor/raspi/config/
```

Do not commit deployment-specific config values to the repo if they contain
sensitive or site-specific data.

---

## 9. Systemd Service

Create a systemd service file to run the application automatically on boot:

```bash
sudo nano /etc/systemd/system/labdash.service
```

Minimum service file:

```ini
[Unit]
Description=LabDash FastAPI monitoring service
After=network.target time-sync.target

[Service]
Type=simple
User=golab
WorkingDirectory=/home/golab/golab-monitor/raspi
ExecStart=/home/golab/golab-monitor/venv/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable labdash
sudo systemctl start labdash
```

Check status:

```bash
sudo systemctl status labdash
sudo journalctl -u labdash -f
```

---

## 11. Serial Device Access

Ensure the application user has permission to access serial devices:

```bash
sudo usermod -a -G dialout $USER
```

Reboot after applying:

```bash
sudo reboot
```

Verify devices are visible after reboot:

```bash
ls /dev/serial/by-id/
```

Each connected USB serial device should appear here. If a device is missing,
check the USB connection and confirm the driver is loaded.

---

## 12. Validation Checklist

Before handing off the deployment, verify each item:

- [ ] SSH access works from Mac using shortcut (`ssh golab`)
- [ ] Passwordless SSH is configured
- [ ] System packages are up to date
- [ ] `chrony` is running and time is synchronized
- [ ] Correct timezone is set
- [ ] Static IP is assigned and reachable over Bard network
- [ ] Bard VPN access confirmed
- [ ] Virtual environment is created and packages installed
- [ ] Application starts without errors (`systemctl status labdash`)
- [ ] Dashboard is accessible at `http://<pi-ip>:8000`
- [ ] All connected devices appear in the dashboard
- [ ] Serial devices visible under `/dev/serial/by-id/`
- [ ] Logs show no repeated errors (`journalctl -u labdash -n 50`)
