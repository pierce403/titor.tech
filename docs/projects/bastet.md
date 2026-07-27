# bastet.ai

Bastet is a crypto-native protective agent for communities, treasuries, and security work. The project began as an infosec DAO inspired by the Egyptian goddess of protection. Its next form is more concrete: an autonomous-but-bounded agent that can read onchain state, explain risk, coordinate bounty workflows, and prepare transactions without crossing execution boundaries unless policy explicitly allows it.

## Key Features

- **Treasury Awareness**: Track wallets, token balances, yield positions, runway, and spending limits before recommending action.
- **Security Coordination**: Connect bug reports, bounty review, attestations, and disclosure workflows across projects like CheapBugs.
- **NFT and Token-Gated Access**: Use crystals or successor credentials to grant access to protected spaces and agent capabilities.
- **Dry-Run Transaction Planning**: Generate proposed calls, calldata, expected effects, risks, and confirmation prompts before anything is signed.
- **Autonomous Agent Interface**: Expose Bastet as a service that can answer crypto questions, monitor events, and prepare safe action plans.
- **Human-Gated Execution**: Require allowlists, spend caps, and explicit approval for signed transactions.

## The Vision of Bastet

From the project's about page:

> "The ultimate goal of this project is to summon Bastet, in her entirety, as a fully autonomous agent capable of protecting her domain."

The important word is "protecting." Bastet is not a trading bot or an unbounded executor. She is a guardian interface for crypto-native work: aware of wallets, communities, contracts, and risk.

The platform represents an experiment in:

- **Autonomous Community Protection**: AI agents helping communities detect issues, route work, and keep attention on what matters.
- **Decentralized Governance**: A path from manual operation to DAO policy to bounded agent execution.
- **Sustainable Funding**: Treasury yield, grants, and bounty flows supporting security work.
- **Post-Corporate Organization**: New coordination models where humans set goals and agents maintain operational continuity.

## Technology Stack

- **Smart Contracts**: Solidity, historically Polygon; future work should prefer Base/OP where it fits the Titor crypto stack.
- **Treasury**: USDC and yield-aware accounting with explicit policy limits.
- **NFTs / Credentials**: ERC-721 crystal tokens or successor credentials for protected access.
- **Frontend**: Web interface plus agent-readable endpoints.
- **AI Integration**: Local and hosted LLMs with tool access, transaction simulation, and strict action gates.
- **License**: Apache License 2.0

## Current Implementation

- **Treasury Staking**: USDC deposited and earning yield in Compound v3 on Polygon.
- **Reward Distribution**: Interest pays "blessings" to active contributors.
- **Access Control**: NFT crystals grant Discord server access.
- **Governance Evolution**: Planned transition from multisig to DAO policy to bounded AI control.

## Bastet as Crypto Agent 8002

The near-term product shape is a service running around port `8002` with four layers:

1. **Read-only intelligence**: ENS, Base/OP balances, Farcaster identity, CheapBugs status, treasury snapshots, and contract/event monitoring.
2. **Policy engine**: Allowlisted chains, contracts, functions, assets, spend limits, rate limits, and required approvers.
3. **Dry-run planner**: Transaction simulation, calldata summaries, failure modes, and human-readable confirmation text.
4. **Execution adapter**: Signing only through approved wallets or multisigs after an explicit confirmation step.

This keeps Bastet powerful in the places where autonomy helps—monitoring, summarizing, planning, and routing—while keeping irreversible crypto actions behind visible gates.

## Links

- **Website**: [bastet.ai](https://bastet.ai)
- **GitHub**: [GitHub Repository](https://github.com/pierce403/bastet)
- **Discord**: [Temple of Bastet](https://discord.gg/37fXv4Vkhj)
- **OpenSea**: [Bastet AI Collection](https://opensea.io/collection/bastet-ai)

## Future Development

The project has multiple related repositories:

- **bastet**: Core smart contracts and platform
- **bastet-meander**: Research architecture
- **eliza-starter-bastet**: Integration with Eliza AI framework

## Alignment with Titor Mission

Bastet is a practical experiment in beneficial autonomy. Titor Technologies is looking for the happy path where humans and machines empower each other instead of drifting into brittle or adversarial systems. Bastet advances that path by making crypto agents legible, bounded, and useful: they can watch, reason, and prepare action, while humans retain control over policy and irreversible execution.
