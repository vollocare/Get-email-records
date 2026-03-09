import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone

from supabase import create_client

PERIOD_DELTAS = {
    "1h": timedelta(hours=1),
    "4h": timedelta(hours=4),
    "12h": timedelta(hours=12),
    "24h": timedelta(hours=24),
    "7d": timedelta(days=7),
}


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="get-email-records",
        description="Query email_records from Supabase",
    )

    time_group = parser.add_mutually_exclusive_group()
    time_group.add_argument(
        "--period",
        choices=PERIOD_DELTAS.keys(),
        help="Preset time period (default: 24h)",
    )
    time_group.add_argument(
        "--from",
        dest="from_dt",
        metavar="DATETIME",
        help="Custom start time (ISO 8601)",
    )

    parser.add_argument(
        "--to",
        dest="to_dt",
        metavar="DATETIME",
        help="Custom end time (ISO 8601, default: now)",
    )
    parser.add_argument("--type", dest="mail_type", help="Filter by mail_type")
    parser.add_argument(
        "--keyword", help="Search in subject and content_summary"
    )
    parser.add_argument(
        "--format",
        dest="fmt",
        choices=["json", "table"],
        default="json",
        help="Output format (default: json)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Max number of records (default: 100)",
    )
    parser.add_argument(
        "--list-types",
        action="store_true",
        help="List all distinct mail_type values in the database",
    )
    parser.add_argument("--supabase-url", help="Supabase URL (or SUPABASE_URL env)")
    parser.add_argument("--supabase-key", help="Supabase Key (or SUPABASE_KEY env)")

    return parser.parse_args(argv)


def resolve_time_range(args):
    now = datetime.now(timezone.utc)

    if args.from_dt:
        dt_from = datetime.fromisoformat(args.from_dt)
        if dt_from.tzinfo is None:
            dt_from = dt_from.replace(tzinfo=timezone.utc)
    elif args.period:
        dt_from = now - PERIOD_DELTAS[args.period]
    else:
        # default: 24h
        dt_from = now - PERIOD_DELTAS["24h"]

    if args.to_dt:
        dt_to = datetime.fromisoformat(args.to_dt)
        if dt_to.tzinfo is None:
            dt_to = dt_to.replace(tzinfo=timezone.utc)
    else:
        dt_to = now

    return dt_from, dt_to


def build_query(client, args):
    dt_from, dt_to = resolve_time_range(args)

    query = (
        client.table("email_records")
        .select("*")
        .gte("mail_date", dt_from.isoformat())
        .lte("mail_date", dt_to.isoformat())
    )

    if args.mail_type:
        query = query.eq("mail_type", args.mail_type)

    if args.keyword:
        kw = args.keyword.replace("%", r"\%")
        query = query.or_(
            f"subject.ilike.%{kw}%,content_summary.ilike.%{kw}%"
        )

    query = query.order("mail_date", desc=True).limit(args.limit)

    query_info = {
        "period": args.period if not args.from_dt else None,
        "type": args.mail_type,
        "keyword": args.keyword,
        "from": dt_from.isoformat(),
        "to": dt_to.isoformat(),
    }

    return query, query_info


def format_table(records):
    if not records:
        print("No records found.")
        return

    columns = ["mail_date", "mail_type", "subject"]
    widths = {col: len(col) for col in columns}
    for r in records:
        for col in columns:
            val = str(r.get(col, ""))
            widths[col] = max(widths[col], min(len(val), 80))

    header = " | ".join(col.ljust(widths[col]) for col in columns)
    sep = "-+-".join("-" * widths[col] for col in columns)
    print(header)
    print(sep)
    for r in records:
        row = " | ".join(
            str(r.get(col, ""))[:80].ljust(widths[col]) for col in columns
        )
        print(row)


def format_output(data, query_info, fmt):
    records = data.data

    if fmt == "json":
        output = {
            "query": query_info,
            "count": len(records),
            "records": records,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2, default=str))
    else:
        print(f"Found {len(records)} record(s)\n")
        format_table(records)


def main():
    args = parse_args()

    url = args.supabase_url or os.environ.get("SUPABASE_URL")
    key = args.supabase_key or os.environ.get("SUPABASE_KEY")

    if not url or not key:
        print(
            "Error: SUPABASE_URL and SUPABASE_KEY must be set "
            "(via --supabase-url/--supabase-key or environment variables)",
            file=sys.stderr,
        )
        sys.exit(1)

    client = create_client(url, key)

    if args.list_types:
        data = client.table("email_records").select("mail_type").execute()
        types = sorted({r["mail_type"] for r in data.data if r.get("mail_type")})
        if args.fmt == "json":
            print(json.dumps({"types": types}, ensure_ascii=False, indent=2))
        else:
            if not types:
                print("No mail types found.")
            else:
                print(f"Found {len(types)} mail type(s):\n")
                for t in types:
                    print(f"  - {t}")
        return

    query, query_info = build_query(client, args)
    data = query.execute()
    format_output(data, query_info, args.fmt)


if __name__ == "__main__":
    main()
