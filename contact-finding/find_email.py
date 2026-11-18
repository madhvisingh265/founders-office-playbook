"""
Free business-email finder for outreach lists (no paid tools).

For each (first name, last name, company domain):
  1. checks the domain actually receives email (MX record lookup)
  2. generates the common corporate email patterns, ordered by how often companies use them
  3. if one address at the company is already known, learns that company's pattern and applies it

It does NOT send emails or scrape websites; pick the top guess and verify with a free checker
before sending.

Usage:
    python find_email.py leads.csv            # columns: first_name,last_name,domain[,known_email]
"""
import argparse
import csv
import re
import sys

PATTERNS = [  # most common first
    "{f}.{l}", "{f}", "{f}{l}", "{fi}{l}", "{f}_{l}", "{fi}.{l}", "{l}.{f}", "{f}{li}", "{l}",
]


def clean(s):
    return re.sub(r"[^a-z]", "", s.lower())


def has_mx(domain):
    try:
        import dns.resolver
        return bool(dns.resolver.resolve(domain, "MX", lifetime=5))
    except ImportError:
        print("pip install dnspython to enable MX checks", file=sys.stderr)
        return None
    except Exception:
        return False


def candidates(first, last, domain):
    f, l = clean(first), clean(last)
    v = {"f": f, "l": l, "fi": f[:1], "li": l[:1]}
    return [p.format(**v) + "@" + domain for p in PATTERNS if (l or "{l}" not in p)]


def learn_pattern(known_email, first, last):
    local = known_email.split("@")[0].lower()
    f, l = clean(first), clean(last)
    v = {"f": f, "l": l, "fi": f[:1], "li": l[:1]}
    for p in PATTERNS:
        if p.format(**v) == local:
            return p
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("leads")
    ap.add_argument("--out", default="leads_with_emails.csv")
    args = ap.parse_args()

    rows = list(csv.DictReader(open(args.leads)))
    learned = {}
    for r in rows:
        if r.get("known_email"):
            p = learn_pattern(r["known_email"], r["first_name"], r["last_name"])
            if p:
                learned[r["domain"]] = p

    mx_cache = {}
    for r in rows:
        d = r["domain"].strip().lower()
        mx_cache.setdefault(d, has_mx(d))
        guesses = candidates(r["first_name"], r["last_name"], d)
        if d in learned:
            f, l = clean(r["first_name"]), clean(r["last_name"])
            best = learned[d].format(f=f, l=l, fi=f[:1], li=l[:1]) + "@" + d
            guesses = [best] + [g for g in guesses if g != best]
            r["confidence"] = "high (company pattern known)"
        else:
            r["confidence"] = "medium (most common pattern)"
        r["domain_accepts_email"] = mx_cache[d]
        r["best_guess"] = guesses[0]
        r["alternatives"] = "; ".join(guesses[1:4])

    with open(args.out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(f"Wrote {len(rows)} leads -> {args.out}")


if __name__ == "__main__":
    main()
