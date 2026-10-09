# Hosting notes

## 2026-10-09: Cloudflare migration preparation

Refreshed HTTPS origin `pierce403/titor.tech` on production `main` at
`be3f233e018a22e54a607484874d54e2b74d1241`; local and remote heads matched before changes.
Prepared Static Assets Worker `titor-tech` in account
`b6d1478423f0bb0c0477df387305e46b`, with workers.dev enabled, directory redirects
and generated real 404s. Logs/traces are configured for Worker execution;
direct static asset responses do not run application code. The initial Worker-only
configuration omitted custom routes; the follow-up below declares the hostname.

Wrangler remains pinned to 4.145.0. Its bundled workerd rejects compatibility
date 2026-10-09 and supports dates through 2026-10-07, so these asset-only
Workers use 2026-10-07 for matching local and production configuration. No
runtime API requires a later date. A deployment dry run alone did not catch
this runtime constraint.

The pinned Python lock preserves the previously verified MkDocs 1.6.1 / Material
9.7.7 renderer and existing plugins. Original requirements and source CNAME remain;
the Worker build excludes output CNAME. GitHub Actions now validates only and
retains a site artifact, preserving the last Pages deployment for recovery.
Cloudflare build `npm run build` and deploy `npx wrangler deploy` avoid duplicate
builds; credentials belong in Cloudflare, never GitHub secrets.

Validation passed with Python 3.12.7: strict pinned MkDocs build, Wrangler
4.145.0 deployment dry run (195 asset files, no bindings), and
10 local Wrangler HTTP checks. The checks verify homepage/article
canonical URLs, directory 307 redirects, linked CSS, populated search
(225 entries), and genuine missing-page 404s. Output CNAME and absent
robots.txt return 404, preserving source/recovery files and current robots behavior.
Local test servers were stopped after verification. Native Git
connection, exact deployed commit, workers.dev checks, domain attachment and
DNS/mail cutover remain pending separate verification steps.

Both generated RSS feeds returned 200 and parsed as RSS in the local runtime.

## 2026-10-09: intended custom-domain route

The source now declares `routes: [{"pattern": "titor.tech", "custom_domain": true}]`
while preserving workers.dev, assets, renderer, runtime date and observability.
The route is exact; no wildcard or additional hostname is introduced. This
follow-up is prepared locally and must remain unpushed until the zone is active
after the approved registrar delegation and its DNS import is verified.

Native Git deployment will provision the hostname's Worker DNS and TLS. Pinned
Wrangler's noninteractive deployment can replace conflicting DNS/origin records
for this exact hostname; preserve the previous website records for recovery and
verify the deployed domain afterward. Mail and unrelated records remain part of
the separate DNS preservation checks. This preparation does not establish a live
custom-domain deployment, delegation, certificate or public HTTPS result.

Exact-configuration schema/packaging dry run passed with Wrangler 4.145.0
(195 existing asset files, no bindings). Initial strict-build and local HTTP
evidence remains applicable because assets and build scripts are unchanged.
No remote deployment, route, DNS or registrar mutation occurred in this step.

Reference: https://developers.cloudflare.com/workers/configuration/routing/custom-domains/
