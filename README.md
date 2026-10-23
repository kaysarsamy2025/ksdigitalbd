# KS Digital BD

A responsive software-company website with 33 public pages, an inquiry API and an owner-only inquiry workspace.

## Content

- `scripts/source-home.html`: approved home design reference.
- `scripts/generate-site.py`: authored page content and shared styles/scripts generator.
- `app/site-content.json`: generated HTML pages consumed by the route handler.
- `app/[[...slug]]/route.ts`: pages, inquiries, owner authorisation, contact settings and CSV export.
- `db/schema.ts` and `drizzle/`: persistent inquiries and public business settings.
- `public/assets/`: supplied logo and social sharing image.

Run `python scripts/generate-site.py` after changing page content, then build with the Sites workflow.

## Checks

- `python scripts/check-pages.py`
- `node scripts/check-inquiries.cjs`
- `node node_modules/typescript/bin/tsc --noEmit`
- Sites build: `node /root/.codex/plugins/cache/openai-curated-remote/sites/1.1.1/scripts/build-site.mjs`

The API check uses an isolated in-memory SQLite database and mocked identity. It never writes production records.

## Runtime

The Sites manifest binds D1 as `DB`. `OWNER_EMAIL` is a hosted secret used only for owner authorisation. It must match the verified email of the owning ChatGPT account. The owner workspace is `/admin` and uses dispatch-owned ChatGPT sign-in. Public requests cannot read inquiries. Contact settings are escaped before public rendering.

The inquiry API validates consent and input, checks Origin and JSON Content-Type, limits body size, uses a honeypot and atomic submission caps. Limits are three inquiries per email per hour and 200 total per day. No IP address is stored in the application database. Production hosting may process its own technical request logs.

Inquiries are saved in the owner's inbox; outbound email notifications are not configured. The public email field does not enable outbound email. Owner actions include status updates, CSV export (up to 5,000 records) and explicit permanent deletion.

## Operation

The owner can add verified public email, phone, WhatsApp and address in `/admin?view=settings`. Do not fabricate team profiles, client testimonials, screenshots, project results, release dates or product prices.

The custom domain `ksdigitalbd.com` has been requested but needs DNS records configured through its registrar/provider. Exact records appear in `/admin?view=launch`. After domain validation succeeds, update the origin in `scripts/generate-site.py`, regenerate the canonical metadata and sitemap, and publish. Search Console requires the domain owner's account and verification.

The source is versioned in the Sites repository. Hosting publishes generated Worker output and applies the committed schema migration. Local preview database records and private environment configuration are excluded from source and deployment archives.
