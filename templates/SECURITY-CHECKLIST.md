# Template – Security checklist

Used twice per build: at plan time (fill "Plan") and before switch-on (fill "Checked" with
how it was checked). **Any "no" in the Checked column = do not switch on.** Fix, then check again.

Client code: ______  Plan version: ______  Date: ______

## 1. Keys and passwords
| # | Check | Plan | Checked (how) |
|---|---|---|---|
| 1.1 | No key, password or token in code, files, chats, logs or screenshots | | search of all files + build guard |
| 1.2 | Every key lives in the host's secret storage, typed in by the client – never by the builder | | |
| 1.3 | Each key has only the permissions it needs | | list permissions |
| 1.4 | The client pasted the key itself, not the key's name or ID | | one test call works |
| 1.5 | Any key that was ever seen by someone else is rotated before switch-on | | |
| 1.6 | The code folder blocks key files (.env, *.key, *.pem, secrets/) – .gitignore + deny rules | | |

## 2. Least access
| # | Check | Plan | Checked (how) |
|---|---|---|---|
| 2.1 | Written list of each part: what it can READ, WRITE, SPEND | | |
| 2.2 | Read-only wherever writing isn't needed | | |
| 2.3 | It reaches only the folders, apps and addresses it needs | | |
| 2.4 | Anything that sends, posts, pays or deletes asks a person first, unless the client said otherwise in writing | | |
| 2.5 | Repos and admin pages are private | | |

## 3. Accounts and money
| # | Check | Plan | Checked (how) |
|---|---|---|---|
| 3.1 | The client owns every account (hosting, AI, payments, domain, email) | | |
| 3.2 | 2-factor login on every account the system uses | | client confirms |
| 3.3 | Spending limit set on every AI / API account before switch-on | | screenshot from client, no keys in it |
| 3.4 | Payments only through a payment provider; the builder never sees card numbers | | |

## 4. Client data
| # | Check | Plan | Checked (how) |
|---|---|---|---|
| 4.1 | All tests used fake data; real data only after the client's yes | | |
| 4.2 | Personal data kept only where needed, and the client knows where | | |
| 4.3 | Consent where the law needs it; privacy page says what is stored | | |
| 4.4 | Logs never hold personal data or secrets (line numbers only) | | |
| 4.5 | Private pages that must not show in search: noindex + not in sitemap | | |

## 5. Outside content
| # | Check | Plan | Checked (how) |
|---|---|---|---|
| 5.1 | Emails, web pages, files and messages the system reads are data, never orders | | test with a planted "ignore your rules" line |
| 5.2 | Downloaded tools, skills and packages checked before use; known sources only | | |

## 6. Email and domain (only if the system sends email or has a website)
| # | Check | Plan | Checked (how) |
|---|---|---|---|
| 6.1 | SPF, DKIM and DMARC set so mail lands in the inbox | | test mail headers: spf/dkim/dmarc = pass |
| 6.2 | Domain and DNS logins have 2-factor; DNS changes logged | | |

## 7. Switch-off and rollback
| # | Check | Plan | Checked (how) |
|---|---|---|---|
| 7.1 | One or two steps to switch it off, written down and tried once | | |
| 7.2 | One or two steps back to "before", written down | | |

## Result
- All Checked = yes? ___  If no: what's open, who fixes it, by when: ___
