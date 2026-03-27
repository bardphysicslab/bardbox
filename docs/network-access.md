# Network Access

This document describes how to reach Bard Box Pi gateways remotely.

## Requirements

- Connected to **Bard internal network** or **Bard VPN**
- SSH key access to the target Pi

## Deployed gateways

| Hostname | IP | Project | SSH shortcut | Dashboard |
|---|---|---|---|---|
| `golab-pi` | `10.60.10.59` | GoLab Monitor | `ssh golab` | `http://10.60.10.59:8000` |

## SSH access

```bash
ssh golab                        # shortcut (requires ~/.ssh/config entry)
ssh golab@10.60.10.59            # direct
```

## Checking a deployed service

```bash
ssh golab "systemctl status labdash --no-pager"
ssh golab "journalctl -u labdash -n 50 --no-pager"
```

## Adding a new gateway

1. Assign a static IP through Bard ITS
2. Add an SSH config entry on your Mac (`~/.ssh/config`)
3. Add a row to the table above
4. Document the service name and dashboard URL

## SSH config example

```
Host golab
  HostName 10.60.10.59
  User golab
  IdentityFile ~/.ssh/id_ed25519
```
