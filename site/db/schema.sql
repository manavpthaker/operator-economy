-- The Operator Economy — capture backend schema
-- Provision once on a Neon (Vercel Postgres marketplace) database.
--   psql "$DATABASE_URL" -f site/db/schema.sql

create table if not exists subscribers (
  id                bigserial primary key,
  email             text        not null,
  tag               text        not null,
  slug              text,
  unsubscribe_token text        not null unique,
  created_at        timestamptz not null default now(),
  unsubscribed_at   timestamptz,
  unique (email, tag)
);

create index if not exists subscribers_tag_idx        on subscribers (tag);
create index if not exists subscribers_slug_idx       on subscribers (slug);
create index if not exists subscribers_created_at_idx on subscribers (created_at desc);
