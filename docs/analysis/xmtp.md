---
title: XMTP
---

# XMTP

XMTP is the cleanest candidate for the **secure messaging layer** in an agent stack.

If Farcaster is the public town square (signals, reputation, coordination), then XMTP is the encrypted backchannel: agent↔agent, human↔agent, and private coordination that shouldn’t be forced into public posts.

## Why agents need a messaging layer

Public-only agents get shaped by the crowd.

Agents that can also do **authenticated, encrypted messaging** can:

- negotiate safely (A2A contracts, intent, delegation)
- run private escalation channels with operators
- exchange credentials *without* spraying secrets into public timelines

## The hard rule

**Never mix untrusted social content with privileged tool execution.**

Messaging can be safer than public feeds, but it’s still an attack surface. Treat messages as input, not commands.

## Minimal viable pattern

1. **Agent identity anchor:** custody key (root-of-trust on-box)
2. **Public presence:** Farcaster for discoverability + reputation
3. **Private comms:** XMTP for secure messaging
4. **Permission manifest:** explicit capabilities + “reversible by default” action gating

## What Maelstrom should provide

- A way to bind XMTP identity to the agent’s root key (or a derived key) cleanly.
- A consistent UX for operators: “public post” vs “secure DM” modes.
- Audit logs + provenance so the operator can review what the agent did and why.

In short: **Farcaster for signaling. XMTP for secure messaging.**
