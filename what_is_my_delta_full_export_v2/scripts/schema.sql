
-- Supabase schema for Delta community contributions
create table if not exists public.contributions (
  id uuid primary key default gen_random_uuid(),
  created_at timestamp with time zone default now(),
  display_name text,
  prompt_index int,
  prompt_text text,
  answer_text text,
  variant text
);

create table if not exists public.prompt_suggestions (
  id uuid primary key default gen_random_uuid(),
  created_at timestamp with time zone default now(),
  display_name text,
  suggestion text,
  variant text
);

-- Enable RLS
alter table public.contributions enable row level security;
alter table public.prompt_suggestions enable row level security;

-- Policies: anyone can insert, anyone can select aggregates (demo-friendly; tighten for production)
create policy if not exists "insert_contributions_anonymous"
on public.contributions for insert
to anon
with check (true);

create policy if not exists "select_contributions_anonymous"
on public.contributions for select
to anon
using (true);

create policy if not exists "insert_suggestions_anonymous"
on public.prompt_suggestions for insert
to anon
with check (true);

create policy if not exists "select_suggestions_anonymous"
on public.prompt_suggestions for select
to anon
using (true);
