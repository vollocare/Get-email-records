---
name: get-email-records
description: Query email records from Supabase. Use when the user asks to search, list, or filter email records by time, type, or keyword.
---

# get-email-records

CLI tool to query `email_records` from Supabase. Outputs JSON (AI-friendly) or table format.

## Prerequisites

The following environment variables must be set:

```bash
export SUPABASE_URL=https://your-project-id.supabase.co
export SUPABASE_KEY=your_publishable_key
```

If not set, provide them via CLI flags: `--supabase-url` and `--supabase-key`.

## Installation

```bash
uv tool install git+https://github.com/vollocare/Get-email-records.git
```

## Command

```bash
get-email-records [OPTIONS]
```

## Parameters

### Time Filters (mutually exclusive)

| Parameter | Description |
|-----------|-------------|
| `--period {1h,4h,12h,24h,7d}` | Preset time range (default: `24h`) |
| `--from DATETIME` | Custom start time (ISO 8601) |
| `--to DATETIME` | Custom end time (default: now) |

If no time parameter is given, defaults to the last 24 hours.

### Content Filters

| Parameter | Description |
|-----------|-------------|
| `--type TYPE` | Filter by exact `mail_type` |
| `--keyword TEXT` | Search `subject` and `content_summary` (server-side fuzzy match) |
| `--list-types` | List all distinct `mail_type` values in the database |

### Output Control

| Parameter | Description |
|-----------|-------------|
| `--format {json,table}` | Output format (default: `json`) |
| `--limit N` | Max number of records (default: `100`) |

## Examples

```bash
# List all available mail types (do this first!)
get-email-records --list-types

# Query last 24 hours (default)
get-email-records

# Query last 7 days
get-email-records --period 7d

# Filter by type
get-email-records --period 24h --type "橘News"

# Keyword search with table output
get-email-records --keyword "測試" --format table

# Custom time range
get-email-records --from 2026-03-01T00:00:00 --to 2026-03-09T00:00:00

# Limit results
get-email-records --period 7d --limit 10
```

## JSON Output Structure

```json
{
  "query": {
    "period": "24h",
    "type": null,
    "keyword": null,
    "from": "2026-03-08T15:00:00+00:00",
    "to": "2026-03-09T15:00:00+00:00"
  },
  "count": 3,
  "records": [
    {
      "id": 123,
      "mail_type": "橘News",
      "subject": "...",
      "content_summary": "...",
      "received_at": "2026-03-09T10:00:00+00:00"
    }
  ]
}
```

## Usage Tips

1. **Start with `--list-types`** to discover available mail types before filtering.
2. **Use `--format table`** when the user wants a human-readable summary.
3. **Use `--format json`** (default) when you need to process or analyze the data programmatically.
4. **Combine filters**: `--type` and `--keyword` can be used together for precise queries.
5. **Time ranges**: Use `--period` for quick queries, `--from`/`--to` for precise ranges.
6. **Parse JSON output** to answer follow-up questions like counts, summaries, or comparisons.
