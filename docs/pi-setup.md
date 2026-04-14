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

## 5. Real-Time Clock (RTC) (Required for Reliable Timestamps)

Bard Box systems must maintain correct time even when network connectivity
is unavailable. This requires enabling and validating the onboard RTC
with a backup battery.

Without a functioning RTC, systems may produce invalid timestamps at boot
(e.g. 1970), which can compromise logged data.

### Enable RTC

Edit config:

```bash
sudo nano /boot/firmware/config.txt
```

Add:

```
dtparam=rtc
```

Reboot:

```bash
sudo reboot
```

### Install RTC tools

On newer Raspberry Pi OS versions, `hwclock` is provided by:

```bash
sudo apt install util-linux-extra -y
```

### Initialize RTC

Ensure system time is correct (via NTP), then write to RTC:

```bash
date
sudo hwclock -w
```

### Enable periodic RTC synchronization (REQUIRED)

Create service:

```bash
sudo nano /etc/systemd/system/bardbox-rtc-sync.service
```

```ini
[Unit]
Description=Write synchronized system time to RTC
After=network-online.target time-sync.target
Wants=time-sync.target

[Service]
Type=oneshot
ExecStart=/usr/sbin/hwclock --systohc --utc
```

Create timer:

```bash
sudo nano /etc/systemd/system/bardbox-rtc-sync.timer
```

```ini
[Unit]
Description=Periodic RTC refresh from system clock

[Timer]
OnBootSec=5min
OnUnitActiveSec=30min
Persistent=true

[Install]
WantedBy=timers.target
```

Enable:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now bardbox-rtc-sync.timer
```

### Verify RTC functionality (REQUIRED)

```bash
sudo systemctl start bardbox-rtc-sync.service
date
sudo hwclock -r
```

Times must match closely.

Then test persistence:
1. Power off and disconnect power
2. Wait several minutes
3. Boot and check: `date`

Time must be correct without waiting for network synchronization.

**Failure condition:** If system time resets after power loss, check the RTC
battery connection and replace the battery if necessary.

Deployments without a functioning RTC must not be considered production-ready.

---

## 6. Timezone

Set the correct timezone:

```bash
sudo timedatectl set-timezone America/New_York
```

Verify:

```bash
timedatectl
```

---

## 7. Networking / Static IP

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

## 8. Python Virtual Environment

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

## 9. Repo and Config Placement

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

## 10. Systemd Service

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

## 13. Validation Checklist

Before handing off the deployment, verify each item:

- [ ] SSH access works from Mac using shortcut (`ssh golab`)
- [ ] Passwordless SSH is configured
- [ ] System packages are up to date
- [ ] `chrony` is running and time is synchronized
- [ ] RTC is enabled and retains time after power loss
- [ ] RTC is periodically synchronized from system clock
- [ ] Correct timezone is set
- [ ] Static IP is assigned and reachable over Bard network
- [ ] Bard VPN access confirmed
- [ ] Virtual environment is created and packages installed
- [ ] Application starts without errors (`systemctl status labdash`)
- [ ] Dashboard is accessible at `http://<pi-ip>:8000`
- [ ] All connected devices appear in the dashboard
- [ ] Serial devices visible under `/dev/serial/by-id/`
- [ ] Logs show no repeated errors (`journalctl -u labdash -n 50`)
