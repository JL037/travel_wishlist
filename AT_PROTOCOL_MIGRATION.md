# Travel Wishlist → AT Protocol Migration Plan

> **Status:** Phase 1 (Auth) is implemented — see `app/routers/atproto_auth.py`,
> `app/utils/atproto_identity.py`, `app/utils/atproto_dpop.py`,
> `app/utils/atproto_oauth.py`, and the `AtprotoSession`/`AtprotoOAuthRequest`
> models. It has not been exercised against a real PDS in this environment
> (no live network access to atproto.com/docs.bsky.app to pin exact PAR/AS
> discovery field names against the current spec) — verify against a real
> account before enabling in production. Phases 2-5 are not started.

## 1. Executive Summary

This document lays out a plan to move Travel Wishlist onto the **AT Protocol** (the
decentralized network behind Bluesky) as a full social app, not just a login
integration:

- **Identity** becomes AT Proto–native: users sign in via OAuth against
  **their own PDS** (bring-your-own-PDS — e.g. `bsky.social` or any other
  provider). We do not run our own PDS.
- **Data** is split into a public and a private half. Shareable fields
  (destination, dates, coordinates) are written as records into the user's
  PDS repo under our own custom Lexicons. Private fields (personal notes,
  optionally ratings) stay in our own Postgres DB, linked to the public
  record by its AT-URI.
- **Social features** — following other travelers, browsing public
  wishlists, a "trips my follows are planning" feed — become possible for
  the first time, but require us to build and operate a custom **AppView**:
  a service that consumes the network firehose, indexes our Lexicons plus
  the follow graph, and serves the queries no central AT Proto API can
  answer.

The rollout is staged so the existing app keeps working throughout: AT Proto
login is additive before any data leaves Postgres, dual-write happens behind
a per-user flag, and the AppView/social layer is the last phase, built once
there's real public data to index.

## 2. AT Protocol Primer

A short reference for the concepts the rest of this doc assumes:

- **DID (Decentralized Identifier)**: a permanent, cryptographic user ID
  (e.g. `did:plc:abc123...`). A **handle** (e.g. `alice.bsky.social`) is a
  human-readable, changeable alias that resolves to a DID via DNS or
  `.well-known`.
- **PDS (Personal Data Server)**: hosts a user's **repo** — a signed Merkle
  Search Tree of records, grouped into **collections** named by NSID (e.g.
  `app.bsky.feed.post`). The PDS is the source of truth for that user's
  data; anyone can read a public repo, only the owner (via OAuth) can write
  to it.
- **Lexicon**: a JSON-Schema-like definition of a record type, namespaced by
  reverse-DNS NSID (e.g. `app.travelwishlist.wishlist.location`). Lexicons
  are how two unrelated apps agree on a data shape without a shared
  database.
- **OAuth**: AT Proto uses OAuth 2.0 with **PAR** (Pushed Authorization
  Requests) and **DPoP**-bound tokens, issued by the user's own PDS
  (discovered from their handle). There's no central "AT Proto login
  server" — every PDS is its own authorization server.
- **Relay / Firehose**: a public infrastructure component
  (`com.atproto.sync.subscribeRepos`) that aggregates every PDS's commit
  stream into one feed. Apps that need cross-user queries subscribe to this
  firehose and build their own index — there is **no central query API**
  for arbitrary Lexicons.
- **AppView**: the app-specific indexing/query service every non-trivial AT
  Proto app ends up building. Bluesky's own AppView indexes
  `app.bsky.*`; since our Lexicons are custom, only *our* AppView will ever
  know how to answer "show me public wishlists from people I follow."

## 3. Current State Recap

- **Backend**: FastAPI + SQLAlchemy 2.0 (async) + PostgreSQL, Alembic
  migrations. Cookie-based JWT auth (`app/dependencies/auth.py`,
  `app/utils/security.py`), with server-side refresh tokens
  (`app/models/refresh_tokens.py`).
- **Models** (`app/models/`): `User`, `WishlistLocation`, `VisitedLocation`,
  `TravelPlan`, `UserSavedCity`, `RefreshToken`. Everything is scoped to
  `owner_id`/`user_id` — fully private, single-tenant data with no
  cross-user relationships anywhere in the schema.
- **API** (`app/routers/`): REST routers `auth`, `wishlist`, `visited`,
  `travel_plans`, `user_saved_cities`, `weather`, all mounted in
  `app/main.py`. Write logic lives mainly in `app/crud.py` and
  `app/services/wishlist_services.py`.
- **Frontend**: React 18 + TypeScript + Vite, React Router, no global state
  manager — pages fetch their own data via `frontend/src/api/fetchWithAuth.ts`
  and check auth via `frontend/src/hooks/useAuthUser.ts`.
- **Social features**: none exist today — no follows, sharing, comments,
  likes, or visibility flags.

This grounds every change below in a real seam in the existing codebase
rather than a rewrite.

## 4. Target Architecture

```
┌─────────────┐        AT Proto OAuth        ┌──────────────────┐
│   Browser    │ ───────────────────────────▶ │   User's PDS      │
│  (React app) │                               │ (bsky.social, etc)│
└──────┬───────┘                               └─────────┬────────┘
       │  REST (as today)                                │ repo writes
       ▼                                                   (via our API,
┌─────────────────────┐   PDS OAuth session    on the user's behalf)
│ Travel Wishlist API   │────────────────────────────────┘
│ (FastAPI, extended)   │
│  - private-fields DB  │
│  - dual-write to PDS  │
└──────────┬───────────┘
           │ reads for cross-user data (feeds, public profiles, follows)
           ▼
┌─────────────────────┐   subscribes to    ┌────────────────┐
│ Travel Wishlist       │◀──────────────────│ Relay/Firehose  │◀── all PDSs
│ AppView (new service) │  com.atproto.sync  │ (public infra)  │
│  - indexes our        │  .subscribeRepos   └────────────────┘
│    Lexicons + follows │
│  - own Postgres DB    │
│  - read-only query API│
└─────────────────────┘
```

- The **React frontend** is mostly unchanged for private/own-data views; it
  gains an AT Proto login flow and new public/social pages that call the
  AppView (via our API, or directly — see §9).
- The **Travel Wishlist API** stays the primary backend the client talks to.
  It's extended to hold an OAuth session with each user's PDS and to write
  public-field records there, while continuing to own the private-fields
  table.
- **We never run a PDS.** Identity and public-data hosting is entirely
  bring-your-own.
- The **AppView is new infrastructure** we do have to build and run — it's
  the only piece that can answer cross-user questions, because no other
  AppView knows about `app.travelwishlist.*` records.

## 5. Lexicon Design

Proposed namespace: **`app.travelwishlist.*`**.

### `app.travelwishlist.wishlist.location`
Public fields only — mirrors `WishlistLocation` minus `notes` and
`owner_id` (ownership comes from being in the user's own repo):

```json
{
  "lexicon": 1,
  "id": "app.travelwishlist.wishlist.location",
  "defs": {
    "main": {
      "type": "record",
      "key": "tid",
      "record": {
        "type": "object",
        "required": ["city", "country", "createdAt"],
        "properties": {
          "name": { "type": "string", "maxLength": 200 },
          "city": { "type": "string", "maxLength": 100 },
          "country": { "type": "string", "maxLength": 100 },
          "latitude": { "type": "number" },
          "longitude": { "type": "number" },
          "proposedDate": { "type": "string", "format": "datetime" },
          "createdAt": { "type": "string", "format": "datetime" }
        }
      }
    }
  }
}
```

### `app.travelwishlist.visited.location`
Mirrors `VisitedLocation`; `rating` is optional/public-by-choice, and
`wishlistUri` is a **strong ref** back to the wishlist record it converted
from (mirrors today's `wishlist_id` FK):

```json
{
  "lexicon": 1,
  "id": "app.travelwishlist.visited.location",
  "defs": {
    "main": {
      "type": "record",
      "key": "tid",
      "record": {
        "type": "object",
        "required": ["city", "country", "visitedOn"],
        "properties": {
          "city": { "type": "string", "maxLength": 100 },
          "country": { "type": "string", "maxLength": 100 },
          "latitude": { "type": "number" },
          "longitude": { "type": "number" },
          "visitedOn": { "type": "string", "format": "datetime" },
          "rating": { "type": "integer", "minimum": 1, "maximum": 5 },
          "wishlistUri": {
            "type": "ref",
            "ref": "com.atproto.repo.strongRef"
          }
        }
      }
    }
  }
}
```

### `app.travelwishlist.travelPlan`
Mirrors `TravelPlan`:

```json
{
  "lexicon": 1,
  "id": "app.travelwishlist.travelPlan",
  "defs": {
    "main": {
      "type": "record",
      "key": "tid",
      "record": {
        "type": "object",
        "required": ["startDate", "endDate", "location"],
        "properties": {
          "location": { "type": "string", "maxLength": 200 },
          "startDate": { "type": "string", "format": "datetime" },
          "endDate": { "type": "string", "format": "datetime" }
        }
      }
    }
  }
}
```

### Reuse existing Lexicons where possible
- **Follows**: use `app.bsky.graph.follow` rather than a custom collection,
  so "following a traveler" interoperates with the broader Bluesky graph
  instead of being a silo only our app understands.
- **Profile basics** (display name, avatar, bio): use `app.bsky.actor.profile`
  — we only need custom Lexicons for wishlist-domain records themselves.

### Private counterpart (not a Lexicon — internal schema only)
A new Postgres table, e.g. `wishlist_private_fields`, keyed by
`(user_id, record_uri)`, holding `notes` and any field the user didn't opt
to publish. The `record_uri` (the AT-URI returned when the PDS record is
created) is the join key between the public PDS record and the private row.

Once implementation starts, generate typed clients from these Lexicon JSON
files with `@atproto/lex-cli` (or write/validate against them directly with
the Python `atproto` SDK, which accepts raw Lexicon JSON for validation).

## 6. Identity & Auth Migration

- Extend `User` (`app/models/users.py`) with `did` and `pds_url` columns —
  the link between a local account and an AT Proto identity.
- Add an AT Proto OAuth flow alongside the existing one: discover the user's
  PDS/authorization server from their entered handle, run PAR + DPoP-bound
  token exchange (via the `atproto` Python SDK's OAuth client support), and
  persist the resulting session server-side — this plays the same role
  `RefreshToken` (`app/models/refresh_tokens.py`) plays today, but for a
  DPoP-bound PDS session rather than our own JWT.
  - New/updated files: `app/routers/auth.py` (new `/auth/atproto/*`
    endpoints), `app/dependencies/auth.py` (accept either session type),
    new `app/utils/atproto_oauth.py` for the OAuth client logic, new
    `app/models/atproto_session.py` for persisted PDS sessions.
- **Open question** (flagged, not decided here): whether email/password
  login is deprecated once AT Proto coverage is broad enough, or kept
  indefinitely as a fallback for users without a PDS. Recommend keeping it
  through at least Phase 4 (§10).
- **Frontend**: new "Sign in with AT Protocol" entry point (handle input →
  OAuth redirect → callback), replacing/augmenting
  `frontend/src/hooks/useAuthUser.ts` and the login page.

## 7. Backend Write Path (dual-write pattern)

Extend the existing write seam at `app/services/wishlist_services.py` and
`app/crud.py` (today's single-Postgres-write path) to:

1. Write public fields to the user's PDS via
   `com.atproto.repo.createRecord` (or `putRecord` for updates), using the
   session persisted in §6.
2. Store the returned AT-URI + any private fields (`notes`) in our own DB.
3. On delete, call `com.atproto.repo.deleteRecord` on the PDS and remove the
   local private row.
4. "Mark visited" (today's `WishlistLocation` → `VisitedLocation`
   conversion) mirrors the same pattern, additionally creating the strong
   ref back to the wishlist record's URI per the Lexicon in §5.

**Failure handling**: a PDS write and a local DB write are not atomic across
two systems. Recommended pattern: write locally first with a `sync_pending`
flag, then a background job pushes to the PDS and clears the flag on
success, retrying on failure — rather than treating the two writes as a
single transaction.

## 8. AppView (new service)

- New standalone service, proposed to live in this repo under `appview/`
  (Python/FastAPI + its own Postgres DB, reusing the SQLAlchemy patterns
  already established in `app/`) to minimize new tooling for the team.
- Subscribes to `com.atproto.sync.subscribeRepos` on a public relay,
  filters commits touching `app.travelwishlist.*` collections (plus
  `app.bsky.graph.follow` edges relevant to our users), validates against
  the Lexicons in §5, and indexes into tables mirroring the public fields
  of `WishlistLocation`/`VisitedLocation`, plus `did` and `follows` tables.
- Exposes read-only endpoints for anything cross-user: a public profile's
  shared wishlist, a "trips my follows are planning" feed, search/discovery.
  These are called by the main API or directly by the frontend (decide
  per-endpoint during Phase 3/4 based on latency/auth needs).
- **Backfill**: on first boot, walk existing users' repos via
  `com.atproto.sync.listRepos`/`getRepo` rather than relying solely on the
  live firehose, so records written before the AppView existed still get
  indexed.

## 9. Frontend Changes

- New AT Proto login screen/flow (§6).
- New "public profile" and "following" pages backed by AppView endpoints,
  additive to the existing private pages (e.g.
  `frontend/src/pages/CombinedLocationsPage.tsx`), which continue to hit our
  own API for the signed-in user's full (public + private merged) view.
- A per-item "share publicly" toggle in the wishlist UI — the main new
  product surface reflecting the public/private split from §5.

## 10. Phased Rollout

1. **Phase 0 — Spike.** Stand up a throwaway PDS test account, hand-write
   one `app.travelwishlist.wishlist.location` record via a script using the
   `atproto` SDK, confirm round-trip read/write and Lexicon validation. No
   product code changes.
2. **Phase 1 — Auth.** Add AT Proto OAuth login as an additional method;
   store `did`/`pds_url` on `User`. Existing Postgres-only wishlist flow is
   untouched.
3. **Phase 2 — Dual-write.** New/edited wishlist and visited-location items
   write to the user's PDS (public fields) + local DB (private fields),
   behind a per-user feature flag. One-time backfill script creates PDS
   records for pre-existing data for opted-in users.
4. **Phase 3 — AppView MVP.** Firehose consumer + backfill indexing; a
   read-only public-profile page powered by it.
5. **Phase 4 — Social features.** Follow graph (via
   `app.bsky.graph.follow`), a following feed, discovery — the actual
   "social AT Proto app" payoff.
6. **Phase 5 — Cutover.** Local Postgres becomes purely a private-fields +
   cache store; local wishlist tables' public columns become derived/cached
   from the AppView rather than authoritative. Revisit whether
   password-only accounts are still needed.

## 11. Risks & Open Questions

- **Non-atomic dual writes** across Postgres and a user's PDS — needs the
  outbox/retry pattern from §7, real added complexity.
- **BYO-PDS reliability**: a user's PDS may be slow, rate-limited, or
  briefly unreachable; the API should degrade to serving last-known local
  data rather than failing the request outright.
- **Existing users have no DID.** 100% of today's user base needs either a
  path to acquire a PDS identity or continues on legacy auth indefinitely —
  a product decision, not just a technical one.
- **New ops surface.** Running an AppView (firehose consumer that must stay
  caught up, its own DB, backfill jobs) is meaningfully larger operational
  burden than today's single web+db `docker-compose` setup.
- **Public ratings later**: even with the private-by-default split, some
  users may eventually want ratings public (a "reviews" feature) — the
  Lexicon in §5 already leaves `rating` as an optional public field to
  support this without a schema change.
- **Namespace ownership**: `app.travelwishlist.*` should be documented/
  registered so other AT Proto apps could interoperate with this data later.

## 12. References

- AT Protocol docs: https://atproto.com/docs
- Bluesky docs (Lexicons, OAuth, firehose): https://docs.bsky.app
- `atproto` Python SDK: https://github.com/MarshalX/atproto
- Self-hosting a PDS (for future reference, not needed for BYO-PDS):
  https://github.com/bluesky-social/pds
- Lexicon specification: https://atproto.com/specs/lexicon
