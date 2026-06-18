# 📚 IBPS Clerk Prelims — Study Tracker

A Streamlit-based study tracker for IBPS Clerk Prelims 2025 with block-based SRS (Spaced Repetition System).

## Features

- **92 topics · 186 modules · 2,609 pages** across QA, Reasoning, Puzzles, DI, English
- **SRS scheduling** — reviews auto-scheduled at +1, +3, +7, +15, +30 blocks (VH priority)
- **One-click workflow** — see task → study pages → click Done → get next
- **Progress dashboard** — section & priority breakdowns, topic status table
- **Review schedule** — upcoming reviews sorted by due block
- **Offline-first** — state stored in JSON, no database needed

## Run Locally

```bash
pip install streamlit
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Fork this repo
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub and select this repo
4. Set `app.py` as the main file
5. Deploy — done!

## SRS Priority Gaps

| Priority | Reviews | Block gaps after completion |
|:---------|:--------|:----------------------------|
| 🟣 Very High | 5 | +1, +3, +7, +15, +30 |
| 🔴 High | 4 | +3, +7, +15, +30 |
| 🟡 Medium | 3 | +7, +15, +30 |
| 🟢 Low | 2 | +15, +30 |
