# Erlang C Workforce Calculator

**[Live Demo →](https://erlang-c-calculator-hatemshalaby.streamlit.app/)**

Interactive workforce staffing calculator built on real Erlang C queueing theory — not an approximation. Implements the numerically stable recursive Erlang B relation to derive Erlang C, avoiding factorial overflow for large agent counts.

## What it calculates
Given call volume, average handle time, target service level, and shrinkage, this tool determines:
- Traffic intensity (Erlangs)
- Minimum agents required to hit your service level target
- Shrinkage-adjusted final headcount
- Achieved service level and average speed of answer

## Formulas implemented
- Recursive Erlang B (numerically stable, avoids factorial overflow)
- Erlang C derived from Erlang B (standard telecom industry relation)
- Service level via exponential decay model
- Average speed of answer

## Tech stack
Python, Streamlit — pure math functions fully decoupled from UI logic, independently testable.

## Run locally
```powershell
pip install -r requirements.txt
python -m streamlit run app.py
```

## Author
Hatem Shalaby — [GitHub](https://github.com/HatemShalaby) | [LinkedIn](https://www.linkedin.com/in/hatem-shalaby-202902127/)
