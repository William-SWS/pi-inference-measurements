# Inference measurements on the rasp (Raspberry Pi 4)

Static site that tracks, in chronological order, how much it costs to run a trained machine learning model on an edge device. The site content is in Brazilian Portuguese.

## What the dashboard is about

The project detects denial-of-service (DoS) attacks in MQTT traffic on edge devices. This site follows the **inference cost** of the detector on the device itself, not its classification quality.

- **Device:** Raspberry Pi 4 Model B (4 GB RAM, Debian 13, no fan, SD card), called "rasp" here and accessed only over SSH.
- **Model:** decision tree with the LowVariance feature selector (11 input features), already trained.
- **What is measured:**
  - **In-process latency:** the wall-clock time of each `predict` call inside the Python process. It does not include network, HTTP, JSON or feature extraction from packets, so it is not end-to-end detector latency.
  - **Memory:** the memory the model adds to the process (ΔPSS and ΔUSS, compared against a "null model" that always returns the same class), plus absolute PSS, USS and maxrss.
- **How it is measured:** each repetition is a fresh process pinned to one thread. For each batch size, in rows per call (1 row per call, like a detector deciding one packet at a time, and 1,024 rows per call, batch processing), 200 warm-up calls are discarded and 2,000 calls are timed in sequence. One run is one condition measured over several repetitions.
- **Latency over HTTP on loopback** (2026-11-13 entry): the inference service called over HTTP inside the rasp itself (no real network). There is no latency limit anywhere on the site: the p95 limit was withdrawn from the project (decision 186).
- **Conditions compared:** graphical desktop running or stopped, CPU frequency governor (`ondemand` or `performance`, the latter fixing the CPU at its maximum frequency), a temperature/frequency logger running alongside the measurement (an observer effect), and the kernel configuration before or after a reboot. The `performance` governor is the main focus.

The measurement pages answer questions such as:

1. Do the median and the p95 change between conditions, and is the difference larger than the variation between repetitions?
2. Does the tail (p99, slow calls, lag-1 autocorrelation) change, and under which conditions?
3. How are call durations distributed, and do slow calls come in periodic groups?
4. What is the effect of the logger running alongside?
5. Is memory stable across repetitions and runs?
6. Does latency drift with run order or chip temperature?
7. How do 1 row per call and 1,024 rows per call relate in time per row?

Besides measurement pages, the timeline also has short **notes** recording decisions and changes in the method (for example, a kernel configuration change or a new run order).

### Caveats

- The data is **exploratory**: a few models, one rasp without a fan. It should not be generalized to other models, and no number here is a final result.
- Run order was not randomized, so order and temperature are confounded.
- With few repetitions per run (5), the pages show the spread between repetitions instead of claiming statistical significance.
- This public version contains only charts and aggregated numbers: it does not include the duration of each individual call.

## Structure

```
index.html                 home page with the timeline
painel/index.html           project state panel: tickets, decisions, open items, next step
figuras/                   PNG figures (300 dpi, English text, Okabe-Ito palette) and gerar_figuras.py, which reads the CSVs
assets/etapas.js           list of entries ("etapas"), in chronological order (the navigation is built from it)
assets/nav.js              top bar, "previous / next" links and the timeline
assets/estilo.css          colors, fonts and layout (light and dark theme)
assets/fontes/             IBM Plex Sans and Mono, self-hosted (SIL Open Font License)
assets/dash-shim.js        lets the measurement pages run on their own, with the data embedded
assets/d3.min.js           d3 v7.9.0
etapas/<id>/index.html     one page per entry
```

There is no build step: GitHub Pages serves the files as they are, and the pages also open straight from disk, with no internet connection.

## Adding an entry

1. Create the folder `etapas/<id>/`, with an id that starts with the date (`2026-11-20-lote3`).
2. Copy the `index.html` of an entry of the same type:
   - **note** (text only, `tipo: 'nota'`): copy `etapas/2026-11-11-reinicio-cgroup-psi/index.html` and replace the text;
   - **measurement** (charts, `tipo: 'medicao'`): copy `etapas/2026-11-11-lote1-lote2/index.html`; the data lives in the `<script type="text/csv" id="csv-...">` blocks at the end of the page.
3. Change `data-etapa="..."` on the `<body>` to the new id.
4. Add an item at the end of the list in `assets/etapas.js` (`id`, `data` (date), `tipo` (type), `status`, `titulo` (title), `resumo` (summary)).

The home page, the top menu and the previous/next links update on their own.
