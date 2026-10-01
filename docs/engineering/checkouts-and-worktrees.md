# Checkouts and worktrees

These rules cover where agents write and how a checkout is ended. The tool
behavior described here was checked on 2026-10-01 against the Claude Code
documentation, the Codex documentation, and the maintainer's report of the
current Codex app. Recheck it when either tool changes.

## Terms

- **Canonical checkout:** the one ordinary clone named in a repository's root
  `AGENTS.md`. It tracks the default branch.
- **Task checkout:** where a task writes, either the canonical checkout or a
  linked worktree of it.
- **Managed worktree:** one that a tool creates and removes. The Codex app
  keeps them in `$CODEX_HOME/worktrees` by default. Claude Code keeps them in
  `.claude/worktrees/`, along with its subagent and background-session
  worktrees.
- **Ordinary worktree:** one created with `git worktree add`.

## Rules

1. **One clone per repository.** Make further checkouts as worktrees of the
   canonical clone, not new clones. Do not keep checkouts in folders that a
   tool synchronizes or the system empties, such as chat project mirrors or
   `/tmp`.
2. **Record the task checkout before writing:** repository, path, branch (or
   base commit if detached), purpose and owner (agent and session). Put it in
   the task's durable evidence.
3. **Reuse before creating.** Run `git worktree list`. Reuse an idle worktree
   for the same purpose if it is clean and no process or session is using it.
4. **One writer per working tree.** Concurrent writers use separate
   worktrees. In a shared canonical checkout, edit only files your role owns,
   and recheck `git status` immediately before writing.
5. **Detached HEAD is allowed.** Codex-managed worktrees start detached by
   design. Before cleanup, any unique work must be durably recoverable. Unique
   work means commits not on any remote branch, plus uncommitted changes worth
   keeping. It is recoverable when it is:
   - pushed to a named remote branch;
   - saved as a bundle or patch somewhere durable, outside the checkout and
     outside `/tmp`; or
   - held in the tool's recoverable snapshot.
6. **No secrets or live state in task checkouts.** Do not copy credentials,
   `.env` files, live state, backups or production logs into a task checkout.
   That includes `.worktreeinclude`: both tools copy matching ignored files
   into new worktrees. Tests use synthetic data, or a read-only snapshot kept
   outside the checkout.
7. **Before ending a checkout, check and record:**
   - uncommitted and untracked files;
   - commits not on a remote branch, after a fresh fetch;
   - ignored files that hold unique data;
   - processes or sessions using the checkout;
   - its owner.

   If anything is unresolved, keep the checkout and ask.
8. **Ending a checkout, by kind:**
   - **Codex-managed:** use the app's managed-worktree archive operation
     (`archive_worktree`). It keeps a recoverable snapshot while the chat
     stays open. Do not delete the directory yourself. Codex also removes
     older managed worktrees automatically, except those of pinned or active
     chats and permanent worktrees, so rule 5 applies before work is left
     there.
   - **Claude Code `--worktree`:** at exit, choose Keep unless all unique work
     is recoverable. Choosing Remove deletes the worktree and its local
     branch. Claude Code sweeps subagent and background-session worktrees only
     when they hold no work.
   - **Claude desktop sessions using a worktree:** what archiving the session
     does to its worktree is not yet verified. Apply rule 7 before archiving
     one.
   - **Ordinary:** run `git worktree remove <path>`. It refuses a dirty tree;
     do not force it. Run `git worktree prune` for entries whose directory is
     already gone.
9. **Separate decisions.** Ending a checkout, deleting a branch, and deploying
   are different actions with different approvals. Delete a local or remote
   branch only after its merge is confirmed on GitHub, or after the
   maintainer approves discarding it.
