# Scorecard: Platform Engineer (First Round)

**Candidate:** ____________  **Date:** ________  **Interviewer:** ________

This round screens for real hands-on experience, problem-solving approach and startup fit. Deep technical evaluation (system design, live debugging) happens in the engineering round. **Probe for specifics:** people who did the work can name the exact tools, numbers and failures.

---

## 1. Background & motivation (5 min)
- Walk me through the platform/infrastructure you work on today. How many services, which cloud, how many engineers use it?
- Why move now, and why a startup?

**Score:** ___ **Evidence:** ______________________________________

## 2. Hands-on infrastructure (10 min)
- What does a deploy look like at your company, from merge to production? Which parts did *you* build?
- Tell me about something you automated. What was the before/after?

| ✅ Specifics to listen for | 🚩 |
|---|---|
| Names tools they configured (Kubernetes, Terraform, Docker, CI/CD, GitHub Actions/Jenkins, AWS/GCP); gives numbers (deploy time, cost, uptime) | "We use Kubernetes" but can't describe what they did; only clicks in a console |

**Score:** ___ **Evidence:** ______________________________________

## 3. Incidents & reliability (8 min)
- Tell me about a production incident you handled. How was it detected, what was the root cause, and what changed afterwards?
- *Follow-up:* What monitoring/alerting do you rely on?

| ✅ | 🚩 |
|---|---|
| Clear timeline; root cause, not just the symptom; added a guard so it doesn't recur | Can't recall any incident; blames others |

**Score:** ___ **Evidence:** ______________________________________

## 4. Problem-solving approach (7 min)
- **Scenario:** "Our API latency doubled after this morning's deploy, but CPU and memory look normal. How do you investigate?"

| ✅ | 🚩 |
|---|---|
| Checks what changed (diff, config, dependencies); looks at DB, network and external calls; considers a rollback first | Random guessing; no thought of a rollback |

**Score:** ___ **Evidence:** ______________________________________

## 5. Collaboration & ownership (5 min)
- How do you help product engineers ship faster without becoming a ticket queue?
- Something you'd do differently in your current setup if you could start over?

**Score:** ___ **Evidence:** ______________________________________

## 6. Logistics (3 min)
On-site OK: Y/N · Notice period: ____ · Expected CTC: ____ · Current CTC: ____

---

## Summary
| Competency | Score |
|---|---|
| Background & motivation | |
| Hands-on infrastructure | |
| Incidents & reliability | |
| Problem-solving | |
| Collaboration & ownership | |
| **Average** | |

**Recommendation:** ☐ Strong yes ☐ Yes ☐ No  
**Topics for the engineering round to go deeper on:** ____________________
