# AI Agent Showcase – how I run multi-agent work safely

I'm JZ de Jager. I run a small business that builds AI assistant templates and
sets up AI agents for clients. I don't hand-code: I design the system, write the
rules and prompts, and direct AI coding agents (mainly Claude and Grok) to build it.
Then I check what they did.

This repo shows the **method**, with clean samples. My real business and client
files stay private on purpose – everything here was written fresh for this repo,
with made-up data.

## The method in one line

**Written rules → approval gates → canary tests → logs.**
Agents can do a lot on their own, but every risky action has a gate, every rule has a
test, and every action leaves a log line.

| Piece | What it does | Sample |
|---|---|---|
| Rules | One master rule file every agent reads at the start of each session. No copies, so no drift. | [rules/approval-gate.md](rules/approval-gate.md) |
| Approval gates | Anything that sends, posts, pays, publishes or deletes needs an exact preview and one human "yes". One yes = one action. | [rules/approval-gate.md](rules/approval-gate.md) |
| Canary tests | Short prompts with a clear "pass if". Every rule change gets re-tested in a fresh agent that hasn't seen the change. A failed canary blocks the change. | [canary-tests/CANARY-TESTS.md](canary-tests/CANARY-TESTS.md) |
| Handoff packets | Agents in different systems talk only through a fixed text format. A checker stops bad packets before they move. | [handoff-packet/](handoff-packet/) |
| Templates | Every build starts with a cost estimate and ends with a security check. | [templates/](templates/) |

## What's inside

```
rules/approval-gate.md          sample rule: the one-action preview + yes gate
canary-tests/CANARY-TESTS.md    5 sample canary tests with "pass if" lines
handoff-packet/FORMAT.md        the packet format agents use to talk to each other
handoff-packet/example-packet.md  a made-up packet
handoff-packet/packet_check.py  checker: required fields, approval line, secret block
handoff-packet/test_packet_check.py  tests for the checker (Python standard library only)
templates/COST-ESTIMATE.md      cost estimate before any build
templates/SECURITY-CHECKLIST.md security check before anything switches on
```

## Run the checker

Python 3.10 or newer, nothing to install.

```
cd handoff-packet
python packet_check.py example-packet.md
python -m unittest -v
```

The checker reports line numbers only. It never prints the packet text, so a secret
that slips into a packet never ends up in a log.

## What I do and don't claim

- This is how I run my own multi-agent setup day to day. The samples are cut-down,
  rewritten versions of it.
- I direct AI coding agents and review their work. I'm not a competitive programmer.
- No client data, business data, keys or account details are in this repo.

## Contact

Through my profile on the platform you found me on.

All rights reserved. You can read and run it. Ask before you reuse it.
