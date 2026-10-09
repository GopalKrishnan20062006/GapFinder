# GapFinder

Live Demo 
https://gap-finder.streamlit.app/

**Evidence-driven commercialization gap detection.**

GapFinder investigates a simple but difficult question: where does strong technological or market interest exist without a matching level of commercial supply?

It pulls evidence from six independent search dimensions (research, patents, products, public demand, industry news, and hiring), normalizes each into a comparable signal, and measures the distance between what a technology promises and what the market currently offers.

Built for the SerpApi Hackathon 2026, Wildcard track.

---

## The Problem

A technology can have deep academic research, rising public interest, growing industry coverage, and companies actively hiring for it, while still having very few products on the market.

That mismatch is a potential commercialization gap. Today, those signals are usually examined in isolation: a researcher reads papers, an analyst checks trends, a founder browses the shelf. GapFinder puts them side by side and reasons over them together.

```text
High research
+ High demand
+ High industry activity
+ High hiring
+ Low commercial supply
------------------------------
= Potential commercialization gap
```

When demand is rising and supply remains thin, GapFinder additionally flags an **emerging gap**, the early-stage version of the same pattern.

---

## How It Works

```text
                  User technology
                         |
                  Query strategy
                         |
        +----------------+----------------+
        |                |                |
     Scholar          Patents          Shopping
        |                |                |
        +----------------+----------------+
        |                |                |
      Trends            News             Jobs
        |                |                |
        +----------------+----------------+
                         |
                      Evidence
                         |
                Signal normalization
                         |
               Cross-signal analysis
                         |
              +----------+----------+
              |                     |
    Commercialization gap     Convergence
              |                     |
              +----------+----------+
                         |
                  Opportunity score
                         |
                   Evidence report
```

Each engine receives its own purpose-built query rather than a single shared search string. A research query and a job-listing query should not look the same, and GapFinder does not treat them as if they do.

---

## Data Layer: SerpApi

SerpApi is the acquisition layer for the entire system. Six engines, six evidence dimensions:

| Engine | Signal | What it measures |
|---|---|---|
| `google_scholar` | Research | Technical and academic maturity |
| `google_patents` | Patents | Intellectual-property activity |
| `google_shopping` | Commercial supply | Products currently available |
| `google_trends` | Demand | Public search interest and direction |
| `google_news` | Industry | Breadth of industry attention |
| `google_jobs` | Hiring | Real-world adoption and talent demand |

The value is in the combination. No single source is treated as sufficient on its own.

---

## Signal Model

Every evidence source is converted into a normalized score between 0 and 100.

**Research.** Based on the number of retrieved papers and the number of highly cited papers. A larger, better-cited footprint indicates greater maturity.

**Patents.** Based on the count of relevant patent results, adding an IP perspective that academic output alone does not provide.

**Commercial supply.** Based on the number of products returned by Google Shopping. This is the reference signal for the whole analysis: the gap is measured against it, and a low supply score strengthens the gap hypothesis.

**Demand.** Derived from Google Trends using average, recent, and historical interest, from which a trend direction is classified as `Rising`, `Stable`, `Falling`, or `Unknown`.

**Industry.** Based on the number of relevant news articles and the number of unique sources. Independent coverage carries more weight than repeated coverage.

**Hiring.** Based on the number of job listings and the number of unique employers. Hiring is an indirect but useful indicator of adoption.

---

## Scoring

### Commercialization Gap

The core analysis compares two quantities:

```text
Technology / market strength   vs.   Commercial supply
```

Technology strength aggregates research, patents, demand, industry, and hiring. Commercial supply is the market signal from product availability.

### Signal Convergence

Convergence counts how many independent signals are strong enough to support the same conclusion. A gap backed by five agreeing sources is more credible than one backed by a single outlier, so convergence reduces dependence on any one search result.

### Emerging Gap Bonus

When demand is rising and commercial supply is low, an Emerging Gap Bonus is applied. This is intended to surface markets that are forming before competition arrives.

### Opportunity Score

The final score combines demand, research, industry activity, hiring, the commercialization gap, and signal convergence.

| Score | Classification |
|---:|---|
| 75 to 100 | High opportunity |
| 55 to 74 | Promising opportunity |
| 35 to 54 | Moderate opportunity |
| 0 to 34 | Low opportunity |

These classifications are analytical heuristics, not predictions of commercial success.

### Evidence Confidence

A separate score reflects the quantity and diversity of evidence retrieved across research, patents, products, news, and hiring. It is a heuristic measure of evidence quality. It is not a statistical confidence interval and not a probability of success.

---

## Evidence Transparency

GapFinder is designed to avoid black-box conclusions. Every number on the dashboard can be traced back to the raw material behind it.

```text
Input -> Generated queries -> SerpApi evidence -> Signals
      -> Convergence -> Commercialization gap -> Opportunity score
```

After an analysis, the dashboard exposes:

- **Research:** paper titles, authors and publication details, links
- **Patents:** titles, snippets, links
- **Commercial products:** product names, prices, sources
- **Industry:** headlines, sources, links
- **Hiring:** job titles, companies, locations

The exact query sent to each SerpApi engine is also displayed, so the search strategy itself can be audited.

---

## Dashboard

The Streamlit interface is organized into the following sections:

- **Executive results:** Opportunity Score, Commercialization Gap, Technology Strength, Evidence Confidence
- **Executive verdict:** a concise interpretation of the overall opportunity
- **Market signals:** scores for research, patents, commercial supply, demand, industry, and hiring
- **Commercialization assessment:** technology strength, commercial supply, signal convergence, trend momentum, and emerging gap bonus
- **Evidence quality:** how much evidence supports each signal
- **Detailed evidence:** expandable sections with the underlying papers, patents, products, articles, and jobs
- **Search strategy:** the query generated for every engine

---

## Example

Input:

```text
graphene water purification for rural communities
```

Generated queries:

| Engine | Query |
|---|---|
| Scholar | `graphene water purification for rural communities` |
| Patents | `graphene water purification technology` |
| Shopping | `graphene water purification filter product` |
| Trends | `graphene water purification` |
| News | `graphene water purification industry` |
| Jobs | `graphene water purification engineer` |

The returned evidence is normalized, cross-checked for convergence, and combined into the final assessment.

---

## Project Structure

```text
gapfinder/
|-- analysis/
|   |-- __init__.py
|   |-- evidence.py
|   |-- signals.py
|   |-- gap_detector.py
|   `-- report.py
|
|-- data/
|   |-- cache/
|   `-- examples/
|
|-- search/
|   |-- __init__.py
|   |-- client.py
|   |-- web.py
|   |-- scholar.py
|   |-- patents.py
|   |-- shopping.py
|   |-- trends.py
|   |-- news.py
|   |-- jobs.py
|   `-- query_strategy.py
|
|-- utils/
|
|-- app.py
|-- config.py
|-- requirements.txt
|-- .env
|-- .gitignore
|
`-- test_*.py
```

The `search/` package isolates each SerpApi engine behind its own module, `analysis/` turns raw evidence into signals and scores, and `app.py` is the Streamlit front end. Test scripts exist for each engine as well as for evidence, signals, gap detection, and query generation.

---

## Installation

**Requirements**

- Python 3.10 or later
- A SerpApi account and API key
- An internet connection

**Clone the repository**

```bash
git clone https://github.com/GopalKrishnan20062006/gapfinder.git
cd gapfinder
```

**Create a virtual environment**

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

**Install dependencies**

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file in the project root:

```text
SERPAPI_KEY=your_serpapi_api_key
```

The key is loaded through `python-dotenv`. Never commit `.env` or your API key to version control. The repository's `.gitignore` already excludes it.

---

## Running the Application

```bash
streamlit run app.py
```

Enter a technology or research concept, then select **Analyze Opportunity**. GapFinder retrieves the evidence, computes the signals, and presents the full report.

---

## Caching and API Budget

SerpApi quotas are finite, so GapFinder caches aggressively.

Responses are stored under `data/cache/`. When the same query is run again, the cached response is used instead of a new API request. This gives lower API consumption, faster repeat analyses, safer development on a limited quota, and predictable behavior during demonstrations.

A local usage tracker also records consumption against the project's configured search budget.

---

## Fault Tolerance

The pipeline is built so that a single failed search does not terminate the analysis.

```text
Scholar    OK
Patents    OK
Shopping   FAILED
Trends     OK
News       OK
Jobs       OK
```

In this scenario GapFinder still produces a result from the remaining evidence and warns the user that the evidence base is reduced. Because search engines occasionally return empty results or fail outright, this is treated as a normal operating condition rather than an exception.

---

## Limitations

GapFinder is an early-stage screening tool. It is not a substitute for commercial due diligence.

- Results depend on what the search engines surface.
- Result counts are not precise measures of market size.
- Scores are produced by deterministic heuristics.
- Evidence confidence is not statistical confidence.
- Product availability does not equal total market supply.
- Search trends do not directly represent revenue or purchasing intent.
- Job listings are an indirect indicator of adoption.
- Patent counts do not establish commercial viability.
- A high Opportunity Score does not guarantee business success.

Read the output as a prompt for further investigation, not as a verdict.

---

## Security

Never commit the following:

```text
.env
data/cache/
data/search_usage.json
```

The SerpApi key must always be supplied through an environment variable.

---

## Intended Users

Entrepreneurs, startup founders, product and innovation teams, investors, technology scouts, university researchers, and students exploring commercialization opportunities.

---

## Why GapFinder

Most technology discovery workflows ask one of two questions: what has been researched, or what products exist. GapFinder asks the question in between:

> Where does strong technology or market interest exist without an equivalent level of commercial supply?

By combining independent evidence sources, it attempts to surface those mismatches systematically instead of leaving them to intuition.

---

## Hackathon Context

GapFinder was developed for the **SerpApi Hackathon 2026** under the **Wildcard** track.

The project explores how search infrastructure can move beyond simple information retrieval and become a structured technology-to-market intelligence pipeline, using Google Scholar, Patents, Shopping, Trends, News, and Jobs through SerpApi.

---

## AI Tools Disclosure

**ChatGPT (OpenAI)** was used for engineering assistance throughout development, including architecture planning, Python implementation, debugging, algorithm and scoring design, Streamlit implementation, query strategy, error handling, documentation, and hackathon preparation.

**Claude (Anthropic)** was used for selected UI polishing and presentation refinement, including dashboard layout suggestions and visual improvements.

Implementation, testing, integration, and final project decisions were made by the developer. Both tools are disclosed for transparency.

---

## License

This project is provided for demonstration and hackathon purposes.
