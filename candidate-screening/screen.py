"""
Candidate screening scorer.

Takes a CSV of sourced candidates and ranks them against a role profile (YAML-free: profiles are
plain Python dicts below so anyone can edit them). Built because manual shortlisting of 100+
profiles per role was slow and inconsistent between reviewers.

Scoring (0-100):
  - Hard filters  : experience window, required degree, open to work  -> fail = excluded, with reason
  - Weighted fit  : role-relevant experience keywords, startup exposure, location preference
  - Dedup         : candidates already in previous shortlists are dropped

Usage:
    python screen.py sample/candidates.csv --role product_ops --exclude sample/previous_shortlist.csv
"""
import argparse
import re
from pathlib import Path

import pandas as pd

ROLE_PROFILES = {
    "product_ops": {
        "title": "Product & Business Operations Manager",
        "min_years": 2, "max_years": 7,
        "degrees": ["b.tech", "b.e", "be ", "btech"],
        "must_keywords": {"product": 15, "operations": 15, "process": 8, "stakeholder": 6,
                          "sql": 6, "roadmap": 6, "go-to-market": 6, "analytics": 5},
        "penalise_if_only": ["business analyst"],
        "location_tiers": [["ahmedabad"], ["gujarat", "gandhinagar", "vadodara", "surat", "rajkot"]],
    },
    "business_product_associate": {
        "title": "Business & Product Associate",
        "min_years": -1, "max_years": 3,
        "degrees": ["b.tech", "b.e", "be ", "btech"],
        "must_keywords": {"product": 12, "business": 8, "analytics": 8, "sql": 8, "excel": 5,
                          "research": 6, "operations": 8, "internship": 5},
        "penalise_if_only": [],
        "location_tiers": [["ahmedabad"], ["gujarat"]],
    },
    "platform_engineer": {
        "title": "Platform Engineer",
        "min_years": 2, "max_years": 7,
        "degrees": ["b.tech", "b.e", "be ", "btech"],
        "must_keywords": {"kubernetes": 12, "docker": 8, "aws": 8, "gcp": 6, "terraform": 10,
                          "ci/cd": 8, "linux": 5, "python": 5, "go": 5, "observability": 6},
        "penalise_if_only": [],
        "location_tiers": [["ahmedabad"], ["gujarat"], ["mumbai", "pune", "maharashtra", "rajasthan", "goa"]],
    },
}
STARTUP_HINTS = ["startup", "seed", "series a", "series b", "early-stage", "founding", "0 to 1", "0-1"]


def score(row, prof):
    text = f"{row.get('headline', '')} {row.get('summary', '')} {row.get('experience', '')}".lower()
    edu = str(row.get("education", "")).lower()
    loc = str(row.get("location", "")).lower()
    years = float(row.get("years_experience", 0) or 0)

    if not (prof["min_years"] < years < prof["max_years"]):  # strict window, e.g. >2 and <7
        return 0, f"experience {years:g} yrs outside the role window"
    if not any(d in edu for d in prof["degrees"]):
        return 0, "no engineering degree"
    if str(row.get("open_to_work", "")).strip().lower() not in {"yes", "true", "1"}:
        return 0, "not open to work"

    s = sum(w for k, w in prof["must_keywords"].items() if re.search(rf"\b{re.escape(k)}\b", text))
    s = min(s, 60)
    if any(h in text for h in STARTUP_HINTS):
        s += 15
    for i, tier in enumerate(prof["location_tiers"]):
        if any(t in loc for t in tier):
            s += 15 - 5 * i
            break
    if prof["penalise_if_only"] and any(p in text for p in prof["penalise_if_only"]) and "product" not in text:
        s -= 15
    s += min(years, 6) * 1.5  # mild preference for more experience inside the window
    return max(0, min(100, round(s))), "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("candidates")
    ap.add_argument("--role", choices=ROLE_PROFILES, required=True)
    ap.add_argument("--exclude", help="CSV of earlier shortlists (column: profile_url)")
    ap.add_argument("--top", type=int, default=15)
    ap.add_argument("--min-score", type=int, default=30, help="minimum fit score to make the shortlist")
    args = ap.parse_args()

    df = pd.read_csv(args.candidates)
    if args.exclude and Path(args.exclude).exists():
        seen = set(pd.read_csv(args.exclude).profile_url)
        before = len(df); df = df[~df.profile_url.isin(seen)]
        print(f"Removed {before - len(df)} candidates already shortlisted earlier")

    prof = ROLE_PROFILES[args.role]
    res = df.apply(lambda r: score(r, prof), axis=1, result_type="expand")
    df["fit_score"], df["note"] = res[0], res[1]
    excluded = df[df.fit_score == 0]
    short = df[df.fit_score >= args.min_score].sort_values("fit_score", ascending=False).head(args.top)

    out = Path(args.candidates).with_name(f"shortlist_{args.role}.csv")
    short.drop(columns=["note"]).to_csv(out, index=False)
    print(f"\n{prof['title']}: {len(short)} shortlisted, {len(excluded)} failed hard filters, {len(df) - len(short) - len(excluded)} below score {args.min_score} -> {out}\n")
    print(short[["name", "years_experience", "location", "fit_score"]].to_string(index=False))
    print("\nExclusion reasons:\n" + excluded.note.value_counts().to_string())


if __name__ == "__main__":
    main()
