# Template – Cost estimate

Used before any build. The client gets it in plain words before saying yes.
Every number is marked **MEASURED** (we ran it), **LIST** (provider's price page + date)
or **GUESS**.

Client code: ______  Date: ______  Plan version: ______

## 0. Plan (approved before any code is written)
- What it does, in plain words: ___
- Parts, one line each – what it does, what it connects to: ___
- How information arrives (email, form, file, API): ___
- Where it runs: ___
- What it never does: ___
- Who approves before it acts: ___
- Tests before handover: normal use, bad input, broken connection, spending limit hit
- Switch-off and rollback in one or two steps: ___

## 1. One-off build cost
| Item | Amount | Notes |
|---|---|---|
| Build fee | | fixed or per hour |
| Client sign-ups needed (client pays the provider directly) | | e.g. domain, hosting plan |
| Total one-off | | |

## 2. Monthly running cost (client pays providers directly)
| Item | Per month | Type |
|---|---|---|
| Hosting | | LIST (date) |
| AI usage (section 3) | | GUESS until measured |
| Other services (email, database, storage) | | LIST (date) |
| Maintenance plan (if chosen) | | |
| Total per month | | |

## 3. AI cost per use (only if the system calls an AI API)
Formula: cost per run = (input tokens × input price + output tokens × output price) ÷ 1,000,000
Per month = cost per run × runs per month.
Rough guide: 1,000 tokens ≈ 750 English words.

| | Input tokens / run | Output tokens / run | Model | Cost / run | Runs / month | Per month |
|---|---|---|---|---|---|---|
| Normal month | | | | | | |
| Busy month (×2) | | | | | | |

Prices: take them from the provider's price page on quote day and write the date.

Worked example (GUESS, made-up job and made-up prices of $2 in / $10 out per million tokens):
5,000 tokens in + 1,000 out per run, 600 runs a month →
(5,000 × 2 + 1,000 × 10) ÷ 1,000,000 = $0.02 per run → $12.00 a month.

## 4. Spending limit (client sets it before switch-on)
- Expected AI cost per month: $___
- Limit to set: $___ (rule of thumb: about 2× expected, never above the client's budget)
- Where the client sets it: ___
- What happens when it's hit: the system stops calling the AI until the limit resets or
  the client raises it. This is tested before handover.

## 5. What we can't know yet (said plainly to the client)
- Real AI cost: GUESS until the first month runs; re-checked after 30 days.
- Provider price changes after today.
- Volume above the expected number of runs.

## 6. Client summary (copied into the proposal)
"Building it costs $___ once. Running it costs about $___ a month (hosting $___ + AI about
$___, our best guess until we measure the first month). You pay those providers directly,
in your own accounts. Before it switches on, you set a spending limit of $___ a month on
your AI account, so the AI part can never cost more than that."
