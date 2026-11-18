# 🧭 Founder's Office Playbook

**Tools, templates and frameworks from my work as Chief of Staff Executive in the Founder's Office of an early-stage startup.**

At a startup, the founder's office handles the work that doesn't fit a single team: hiring, research that feeds strategy, outreach operations, and making sure priorities actually turn into results each day. This repo holds the reusable parts of that work. **No company-confidential data is included.** All sample data is fictional.

| Folder | What's inside | Type |
|---|---|---|
| [`interview-kit/`](interview-kit) | Structured first-round interview process, level-calibrated scorecards (Platform Engineer, Business & Product Associate/Manager, generic), debrief template | Process |
| [`candidate-screening/`](candidate-screening) | Python scorer that applies hard filters, ranks candidates against a role profile and removes repeats from earlier shortlists | Code |
| [`contact-finding/`](contact-finding) | Free business-email finder for outreach lists: MX check, pattern generation, learns each company's pattern (no paid tools) | Code |
| [`research-frameworks/`](research-frameworks) | Competitor analysis, market-entry scoring, customer research brief | Framework |
| [`operating-rhythm/`](operating-rhythm) | Daily outcome commits to the founder, weekly update template | Process |

## Quick start
```bash
pip install pandas dnspython
python candidate-screening/screen.py candidate-screening/sample/candidates.csv --role platform_engineer
python contact-finding/find_email.py contact-finding/sample_leads.csv
```

## Principles behind this work
- **Outcomes over activity.** Every day starts with commitments to results, not tasks.
- **Same yardstick for everyone.** Structured interviews and written evidence, not gut feel.
- **Problem first, data second.** Research leads with the problem and the use case; numbers go in the appendix.
- **Free before paid.** Use free tools and our own systems before buying subscriptions.

---
**Madhvi Singh** · [LinkedIn](https://linkedin.com/in/madhvi-singh265)
