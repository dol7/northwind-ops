# Evidence 5: a project-scoped MCP server whose credential is `${VAR}`

Captured with Claude Code 2.1.276 on fresh clones of this repo.

## The file

`.mcp.json` at the repo root, committed:

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer ${GITHUB_TOKEN}"
      }
    }
  }
}
```

The only credential is the reference `${GITHUB_TOKEN}`; the value never appears in the repo.
That is what makes the file safe to commit: a raw token in it would leak with every clone and
force every teammate to run on the author's account. A scan for token-shaped strings
(`ghp_`, `github_pat_`, `sk-ant-`, `Bearer <long string>`) over the working tree **and all git
history** finds nothing. `.mcp.json` is not gitignored; a real `.env` is.

## Expansion works: verified against what was actually sent

A local echo server recorded the `Authorization` header Claude Code sent for five
differently-configured servers (fake tokens only):

| In `.mcp.json` | Where the value came from | Header received |
|---|---|---|
| `${GITHUB_TOKEN}` | shell | `Bearer ghp_FAKE_shell_1111`. It expands; the name is **not** on the credential deny-list |
| `${NW_TEST_TOKEN}` | shell | `Bearer tok_FAKE_shell_2222` |
| `${NW_NEVER_SET:-fallback-val}` | not set, default used | `Bearer fallback-val` |
| `${NW_SETTINGS_ONLY}` | only `.claude/settings.local.json` `env` | `Bearer tok_from_settings_local` |
| `${NW_NEVER_SET}` | not set, no default | `Bearer ${NW_NEVER_SET}` (sent **literally**) |

## The clone test

A teammate clones the repo. What arrives is `.mcp.json` and `.env.example`, with no secret.
What happens next depends only on the token they supply:

| Teammate has | `github` server | GitHub tools exposed |
|---|---|---|
| no `GITHUB_TOKEN` | `failed` (the session still starts and works) | 0 |
| a wrong token | `failed` | 0 |
| a valid token | **`connected`** | **46** |

(The valid-token case used the `gh` CLI's token as a stand-in for a teammate's own token. It was
passed through the environment for one read-only connection check and never printed.)

`claude mcp list` in the clone, with no token, says what is wrong:

```
github: https://api.githubcopilot.com/mcp/ (HTTP) - ⏸ Pending approval (run `claude` to approve)
 └ [Warning] [github] mcpServers.github: Missing environment variables: GITHUB_TOKEN
```

## Onboarding: what a teammate does

1. **Approve the server once.** Project-scoped servers ask for approval the first time
   (`Pending approval`). It is deliberate: a committed `.mcp.json` should not silently start a
   network server on a stranger's machine.
2. **Provide their own token**, in either place:
   - `export GITHUB_TOKEN=github_pat_...` in the shell that launches Claude Code, or
   - `{ "env": { "GITHUB_TOKEN": "github_pat_..." } }` in their gitignored
     `.claude/settings.local.json`. Use this from the VS Code extension, which may not inherit
     shell exports. (Verified to expand in a real session.)
3. Use a **fine-grained, read-only** personal access token. What the server can do is whatever
   the token allows.

Claude Code does **not** read `.env` files; `.env.example` only documents the variable.

## Gotchas found while testing

- An **unset** variable does not fail loudly: the server is loaded and the literal text
  `Bearer ${GITHUB_TOKEN}` is sent, so it fails at connection time. `claude mcp list` prints the
  `Missing environment variables` warning.
- `claude mcp list` may report a variable as missing when it is set only in
  `settings.local.json`; the real session still expands it.
- Some credential names read as **empty** in remote `url` / `headers` (the docs list
  `ANTHROPIC_API_KEY`, `NPM_TOKEN`, and others). `GITHUB_TOKEN` is not one of them, as the
  echo test shows; if a token ever arrives empty, rename the variable.
- The config does not validate the token: a wrong token gives `failed`, the same as none.

## Try it live

In the extension, put a token in `.claude/settings.local.json`, restart the session, approve the
server, then run `/mcp` to see `github` connected.
