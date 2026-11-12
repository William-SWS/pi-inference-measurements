# Inference measurements on the Raspberry Pi

Static site that tracks, in chronological order, how much it costs to run a trained machine learning model on an edge device. The site content is in Brazilian Portuguese.

## What the dashboard is about

The project detects denial-of-service (DoS) attacks in MQTT traffic on edge devices. This site follows the **inference cost** of the detector on the device itself, not its classification quality.

- **Device:** Raspberry Pi 4 Model B (4 GB RAM, Debian 13, no fan, SD card), accessed only over SSH.
- **Model:** decision tree with the LowVariance feature selector (11 input features), already trained.
- **What is measured:**
  - **In-process latency:** the wall-clock time of each `predict` call inside the Python process. It does not include network, HTTP, JSON or feature extraction from packets, so it is not end-to-end detector latency.
  - **Memory:** the memory the model adds to the process (ΔPSS and ΔUSS, compared against a "null model" that always returns the same class), plus absolute PSS, USS and maxrss.
- **How it is measured:** each repetition is a fresh process pinned to one thread. For each batch size **B** (1 record per call, like a detector deciding one packet at a time, and 1024 records per call, batch processing), 200 warm-up calls are discarded and 2,000 calls are timed in sequence. One run is one condition measured over several repetitions.
- **Conditions compared:** graphical desktop running or stopped, CPU frequency governor (`ondemand` or `performance`, the latter fixing the CPU at its maximum frequency), a temperature/frequency logger running alongside the measurement (an observer effect), and the kernel configuration before or after a reboot. The `performance` governor is the main focus.

The measurement pages answer questions such as:

1. Do the median and the p95 change between conditions, and is the difference larger than the variation between repetitions?
2. Does the tail (p99, slow calls, lag-1 autocorrelation) change, and under which conditions?
3. How are call durations distributed, and do slow calls come in periodic groups?
4. What is the effect of the logger running alongside?
5. Is memory stable across repetitions and runs?
6. Does latency drift with run order or chip temperature?
7. How do B = 1 and B = 1024 relate in time per record?

Besides measurement pages, the timeline also has short **notes** recording decisions and changes in the method (for example, a kernel configuration change or a new run order).

### Caveats

- The data is **exploratory**: one model, one Raspberry Pi without a fan. It should not be generalized to other models, and no number here is a final result.
- Run order was not randomized, so order and temperature are confounded.
- With few repetitions per run (5), the pages show the spread between repetitions instead of claiming statistical significance.
- This public version contains only charts and aggregated numbers: it does not include the duration of each individual call.

## Structure

```
index.html                 home page with the timeline
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

## Publishing on GitHub Pages

Settings → Pages → *Build and deployment* → Source: **Deploy from a branch** → Branch: `main`, folder `/ (root)`.