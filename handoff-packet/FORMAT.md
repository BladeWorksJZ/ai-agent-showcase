# Handoff packet format

Agents that run in different systems never share logins or files. They talk only through
plain-text packets dropped in a shared folder. A small script moves each packet to the
other side, but only after `packet_check.py` passes it.

A packet is always a **request, never an order**. The receiving agent acts only after its
own human says yes (or the request is on that agent's allowed list).

## Header (required, one per line, in this order)

```
PACKET ID: <PREFIX>-<YYYYMMDD>-<NN>
FROM: <sending agent>
TO: <receiving agent>
TYPE: request | reply | info
REPLY TO: <packet ID> | none
APPROVAL: <YYYY-MM-DD HH:MM> <who approved, or "not needed">
```

## Body sections

```
## WHAT I NEED
## WHAT I NEED BACK
## DO NOT
```

## Checker rules (`packet_check.py`)

| Check | Stops the packet when |
|---|---|
| Header | a required field is missing, empty or out of order |
| Packet ID | it doesn't match `PREFIX-YYYYMMDD-NN` or the date isn't real |
| Type | it isn't `request`, `reply` or `info` |
| Reply | a `reply` has `REPLY TO: none` |
| Approval | the line doesn't start with a real date and time |
| Sections | `WHAT I NEED` or `WHAT I NEED BACK` is missing |
| Secrets | anything looks like a key, token, private key or password |
| Size | the file is over 20 KB |

Output: `PASS` or `STOP` plus reasons with **line numbers only** – never the packet text.

The receiving side also sends a one-line acknowledgement ("read by <agent> <time>") as soon
as it opens a packet, and a reply packet (`REPLY TO` = that ID) when the work is done.
