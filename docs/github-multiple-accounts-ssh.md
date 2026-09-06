# GitHub SSH setup for Bard + personal accounts

This Mac uses separate SSH identities for Bard and personal GitHub work so both accounts can stay available without logging in and out.

## Current SSH config

`~/.ssh/config` contains:

```sshconfig
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes

Host github-personal
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_personal
    IdentitiesOnly yes
    AddKeysToAgent yes
    UseKeychain yes
```

Meaning:

- `github.com` uses `~/.ssh/id_ed25519` for the Bard GitHub account (`bardphysicslab`).
- `github-personal` uses `~/.ssh/id_ed25519_personal` for the personal GitHub account (`kornpop73`).

## Test which account a host alias uses

Bard:

```bash
ssh -T git@github.com
```

Expected response starts with:

```text
Hi bardphysicslab!
```

Personal:

```bash
ssh -T git@github-personal
```

Expected response starts with:

```text
Hi kornpop73!
```

GitHub also says it does not provide shell access; that is normal.

## Clone URLs

For Bard repositories, use the normal GitHub SSH host:

```bash
git clone git@github.com:bardphysicslab/REPOSITORY.git
```

For personal repositories, use the personal alias:

```bash
git clone git@github-personal:kornpop73/REPOSITORY.git
```

Example:

```bash
cd ~/Code/personal
git clone git@github-personal:kornpop73/julep-acting.git
```

## Existing repository: check or fix the remote

Check:

```bash
git remote -v
```

A personal repository should use a remote like:

```text
git@github-personal:kornpop73/REPOSITORY.git
```

If it does not, change it with:

```bash
git remote set-url origin git@github-personal:kornpop73/REPOSITORY.git
```

A Bard repository should normally use:

```text
git@github.com:bardphysicslab/REPOSITORY.git
```

## Important rule for agents and future setup

Do not create a new SSH key just because a private repository returns `Repository not found`.

First run:

```bash
ssh -T git@github.com
ssh -T git@github-personal
```

Then inspect:

```bash
cat ~/.ssh/config
git remote -v
```

The most likely cause is that the repository is being accessed through the wrong SSH host alias/account.

Do not replace or modify the Bard SSH identity when setting up a personal repository. Use `github-personal` for personal GitHub repositories.
