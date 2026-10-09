# Titor Technologies

Titor Technologies is a high-level strategic investment enterprise dedicated to shaping the future of humanity through carefully planned investments in emerging technologies and transformative innovations.

## Mission

We believe in a future where humans, augmented and assisted by intelligent machines, illuminate the galaxy and beyond with the light of consciousness. This future is not inevitable—its realization depends on the choices we make today.

## What We Do

Titor Technologies operates as a strategic investment firm that:

- **Forecasts Future Technologies**: We use modern analytical tools to envision what technologies will exist in the futures we want to create
- **Identifies Technology Gaps**: We measure the gaps between future technological requirements and current capabilities
- **Makes Strategic Investments**: We invest in undervalued technologies destined to grow and fill critical gaps in humanity's technological evolution
- **Shares Knowledge**: We amplify our impact by sharing research and teaching our methods to others who share our vision for a bright future

## Investment Philosophy

Our approach is methodical and forward-thinking:

1. **Vision-Driven Analysis**: We start with the end in mind—what does an optimal future look like?
2. **Gap Identification**: We systematically identify what technologies and capabilities are missing
3. **Strategic Positioning**: We invest early in technologies that will bridge these gaps
4. **Knowledge Multiplication**: We share our insights to accelerate global progress toward beneficial outcomes

## Projects

Titor Technologies develops and maintains several innovative projects that demonstrate our commitment to advancing human potential. Visit [titor.tech](https://titor.tech) to explore our research, analysis, and project portfolio.

---

*Building tomorrow's world through today's strategic investments.*

## Cloudflare publishing

The prepared Worker `titor-tech` serves MkDocs output directly through Workers
Static Assets, including directory URLs, search, and the generated real 404 page.
Build locally with `npm ci && npm run build`; check packaging with
`npm run deploy:check`, and preview with `npm run dev`.
`requirements.lock` pins the renderer verified for this migration while the
original `requirements.txt` remains available for dependency maintenance.

Connect `pierce403/titor.tech` in Cloudflare Workers Builds with production branch
`main`, root `/`, build `npm run build`, and deploy `npx wrangler deploy`.
Use all paths and disable builds for other branches. Cloudflare fetches and
publishes each production commit using credentials retained in Cloudflare.
GitHub Actions validates and retains artifacts; it needs no Cloudflare secrets.
`.nvmrc` and `.python-version` select Node.js 22 and Python 3.12.

The configuration initially uses `titor-tech.bcrt43.workers.dev`. Attach
`titor.tech` only after its Cloudflare zone/import is verified. Keep `docs/CNAME`
and the prior `gh-pages` deployment for recovery. Do not overlap manual deployment
with native Git deployment. Git connection, deployment, domain and DNS verification
remain separate migration steps recorded in `NOTES.md`.
