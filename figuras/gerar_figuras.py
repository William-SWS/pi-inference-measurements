## Gera as 12 figuras do painel (PNG, 300 dpi, texto em inglês, paleta Okabe-Ito, sem título interno) a partir dos CSVs.
## Só lê: nada em `analises-pi/` é alterado. Uso: python3 figuras/gerar_figuras.py
## Não há linha de limite de latência em nenhuma figura (o p95 <= 10 ms foi retirado do projeto).

import csv
from pathlib import Path

import matplotlib
import matplotlib.ticker

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

AQUI = Path(__file__).parent
RAIZ = AQUI.parent
ANALISES = Path("/home/william/Documentos/Vault/projects/mqtt/curso/analises-pi")
VAL = ANALISES / "validacao-do-metodo-de-medicao-2026-11-15/dados"
PAR = ANALISES / "pareto-exploratorio-2026-11-14/dados"
HTTP = ANALISES / "latencia-http-loopback-2026-11-12/dados"
RODADA = ANALISES / "rodada-final-sem-estresse-2026-11-15/dados"

## Paleta Okabe-Ito.
AZUL, LARANJA, VERMELHO, VERDE, CELESTE, ROSA, AMARELO, CINZA, PRETO = (
    "#0072B2", "#E69F00", "#D55E00", "#009E73", "#56B4E9", "#CC79A7", "#F0E442", "#999999", "#000000",
)  # fmt: skip
ARVORE, FLORESTA = "LowVariance-DecisionTree", "LowVariance-RandomForest"
NOME = {ARVORE: "Decision tree", FLORESTA: "Random forest"}

plt.rcParams.update({
    "figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white",
    "font.family": "sans-serif", "font.sans-serif": ["Arial", "Liberation Sans", "DejaVu Sans"],
    "font.size": 8.5, "axes.labelsize": 8.5, "xtick.labelsize": 8, "ytick.labelsize": 8,
    "legend.fontsize": 8, "axes.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False,
})  # fmt: skip


def ler(caminho):  ## Lê um CSV como lista de dicionários.
    with open(caminho, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def salvar(fig, nome):  ## Salva em PNG de 300 dpi e fecha.
    fig.savefig(AQUI / nome, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("figura", nome)


def decisao(experimento, trecho=""):  ## Linha de `decisoes.csv` cujo experimento e configuração casam.
    for r in ler(VAL / "decisoes.csv"):
        if r["experimento"].startswith(experimento) and trecho in r["configuracao"]:
            return r
    raise KeyError((experimento, trecho))


def pontos(ax, x, ys, cor, largura=0.1, semente=1):  ## Pontos de um grupo com espalhamento horizontal fixo.
    ax.scatter(x + np.random.default_rng(semente).uniform(-largura, largura, len(ys)), ys, s=24, color=cor,
               alpha=0.9, edgecolor="white", linewidth=0.4, zorder=3)  # fmt: skip


def traco_mediana(ax, x, ys, texto, lado):  ## Traço da mediana do grupo e o valor exato ao lado.
    m = float(np.median(ys))
    ax.hlines(m, x - 0.28, x + 0.28, color=PRETO, linewidth=1.6, zorder=4)
    ax.text(x + lado * 0.34, m, texto(m), va="center", ha="right" if lado < 0 else "left", fontsize=8)
    return m


## ---------- 1. Mesmo processo × processo novo ----------
def fig1():
    linhas = ler(VAL / "mesmo-processo-vs-processo-novo.csv")
    fig, eixos = plt.subplots(1, 2, figsize=(9.6, 3.9))
    for ax, modelo, fator, un in zip(eixos, (ARVORE, FLORESTA), (1, 1000), ("µs", "ms")):
        for x, (grupo, cor, nome) in enumerate([("mesmo processo", AZUL, "Same process"), ("processo novo", LARANJA, "New process")]):
            ys = [float(r["p95_us"]) / fator for r in linhas if r["modelo"] == modelo and r["grupo"] == grupo]
            pontos(ax, x, ys, cor, semente=x + 3)
            traco_mediana(ax, x, ys, lambda m: f"median {m:.1f} {un}" if fator == 1 else f"median {m:.3f} {un}", -1 if x == 0 else 1)
        d = decisao("Mesmo processo", modelo.split("-")[1])["valor"]
        ax.set_xticks([0, 1], [f"Same process\n(10 loops of 2,000 calls,\nfrom only 2 processes)", "New process\n(10 processes of\n2,000 calls each)"])
        ax.set_xlim(-1.5, 2.5)
        ax.set_ylabel(f"p95 per unit ({un})")
        ax.set_title(f"{NOME[modelo]}: difference {d} (limit ±5%, not detected)", fontsize=8.5)
        ax.margins(y=0.15)
    fig.tight_layout()
    salvar(fig, "1-mesmo-processo-vs-processo-novo.png")


## ---------- 2. Custo do medidor de memória ----------
def fig2():
    blocos = ler(VAL / "custo-do-medidor-de-memoria.csv")
    d = decisao("Custo do medidor")["valor"]  ## "+43.47 µs [+17.09; +56.93]"
    ic = d.split("[")[1].rstrip("]").split(";")
    dif = {p: np.median([float(b[f"{p}_com_us"]) - float(b[f"{p}_sem_us"]) for b in blocos]) for p in ("p50", "p95", "p99")}
    fig, (a, b) = plt.subplots(1, 2, figsize=(9.8, 4.2), gridspec_kw={"width_ratios": [1.1, 1]})
    for r in blocos:
        a.plot([0, 1], [float(r["p95_sem_us"]), float(r["p95_com_us"])], color=CINZA, linewidth=0.9, zorder=1)
    for x, col, cor in ((0, "p95_sem_us", AZUL), (1, "p95_com_us", LARANJA)):
        pontos(a, x, [float(r[col]) for r in blocos], cor, largura=0.0)
        m = np.median([float(r[col]) for r in blocos])
        a.text(x + (-0.08 if x == 0 else 0.08), m, f"median {m:.1f} µs", ha="right" if x == 0 else "left", va="center", fontsize=8)
    a.set_xticks([0, 1], ["Without memory meter", "With memory meter"])
    a.set_xlim(-0.6, 1.6)
    a.set_ylabel("p95 per block (µs), decision tree, 1 row per call")
    a.set_title("(a) Paired p95, 10 blocks of 2 processes", fontsize=8.5)
    cores = {"p50": CELESTE, "p95": AZUL, "p99": VERMELHO}
    for x, p in enumerate(("p50", "p95", "p99")):
        b.bar(x, dif[p], color=cores[p], width=0.55, zorder=2)
        if p != "p95":
            b.text(x, dif[p] + 20, f"+{dif[p]:.1f} µs", ha="center", fontsize=8)
    b.errorbar(1, dif["p95"], yerr=[[dif["p95"] - float(ic[0])], [float(ic[1]) - dif["p95"]]], color=PRETO, capsize=4, linewidth=1.2, zorder=3)
    limite = float(decisao("Custo do medidor")["limite"].split("<=")[1].split("µs")[0])
    b.text(1, limite + 30, f"+{dif['p95']:.2f} µs\n95% CI {float(ic[0]):+.2f} to {float(ic[1]):+.2f}", ha="center", fontsize=7.5)
    b.hlines(limite, 0.62, 1.38, color=PRETO, linestyle="--", linewidth=1.0, zorder=4, label=f"decision limit {limite:.2f} µs (applies to the p95)")
    b.legend(loc="upper left", frameon=False, fontsize=7.5)
    b.set_xticks(range(3), ["p50", "p95", "p99"])
    b.set_xlim(-0.6, 2.9)
    b.set_ylabel("Median paired difference, with − without (µs)")
    b.set_title("(b) Median difference per percentile", fontsize=8.5)
    fig.tight_layout()
    salvar(fig, "2-custo-do-medidor-de-memoria.png")
    return dif


## ---------- 3. Pico amostrado × contador do sistema ----------
def fig3():
    ps = ler(VAL / "pico-amostrado-vs-contador.csv")
    fig, ax = plt.subplots(figsize=(7.6, 4.0))
    estilos = [("primeira_amostra_mib", "First sample", CELESTE, "o", -0.12), ("maximo_amostrado_mib", "Maximum sampled (1 s meter)", AZUL, "s", 0.0),
               ("pico_do_contador_mib", "System peak counter", LARANJA, "D", 0.12)]  # fmt: skip
    for col, nome, cor, mk, dx in estilos:
        ax.scatter([i + dx for i in range(3)], [float(p[col]) for p in ps], color=cor, marker=mk, s=40, label=nome, zorder=3)
    for i, p in enumerate(ps):
        ax.text(i + 0.2, float(p["pico_do_contador_mib"]), f"counter {float(p['pico_do_contador_mib']):.3f}\nsampled {float(p['maximo_amostrado_mib']):.3f}\nfirst {float(p['primeira_amostra_mib']):.3f}\ngap {float(p['lacuna_pct']):.2f}% ({p['amostras']} samples)", fontsize=7.5, va="center")
    ax.set_xticks(range(3), [p["processo"].replace("processo", "Process") for p in ps])
    ax.set_xlim(-0.4, 3.1)
    ax.set_ylabel("Memory of the cgroup scope (MiB), random forest")
    ax.legend(loc="upper right", frameon=False, fontsize=7.5)
    ax.margins(y=0.25)
    fig.tight_layout()
    salvar(fig, "3-pico-amostrado-vs-contador.png")


## ---------- 4. Leituras do contador de pico ----------
def fig4():
    ls = ler(VAL / "zerar-contador-de-pico.csv")
    nomes = ["1. Memory before allocating (baseline)", "2. Peak after allocating 100 MiB", "3. Current memory after freeing and resetting",
             "4. Peak right after the reset", "5. Peak after allocating 30 MiB more", "6. Peak read through a new descriptor (not reset)"]  # fmt: skip
    cores = [CINZA, AZUL, CINZA, AZUL, AZUL, VERMELHO]
    fig, ax = plt.subplots(figsize=(8.4, 3.8))
    v = [float(r["valor_mib"]) for r in ls]
    ax.barh(range(6)[::-1], v, color=cores, height=0.6, zorder=2)
    for y, x in zip(range(6)[::-1], v):
        ax.text(x + 2, y, f"{x:.3f} MiB", va="center", fontsize=8)
    ax.set_yticks(range(6)[::-1], nomes)
    ax.set_xlim(0, max(v) * 1.2)
    ax.set_xlabel("MiB (blue: peak counter · grey: current memory · red: new descriptor still sees the old peak)")
    fig.tight_layout()
    salvar(fig, "4-leituras-do-contador-de-pico.png")


## ---------- 5. SVM com 1 × 4 threads ----------
def fig5():
    ls = ler(VAL / "svm-1-vs-4-threads.csv")
    fig, eixos = plt.subplots(1, 2, figsize=(9.6, 3.9))
    for ax, lote, nome, dec in zip(eixos, ("1", "1024"), ("1 row per call (2,000 calls)", "1,024 rows per call (200 calls)"), ("+0.47%", "+1.08%")):
        for x, (th, cor) in enumerate((("1", AZUL), ("4", LARANJA))):
            ys = [float(r["p50_us"]) / 1000 for r in ls if r["lote_linhas_por_chamada"] == lote and r["threads"] == th]
            pontos(ax, x, ys, cor, semente=x + 7)
            traco_mediana(ax, x, ys, lambda m: f"median {m:.3f} ms", -1 if x == 0 else 1)
        d = [r for r in ls if r["lote_linhas_por_chamada"] == lote]
        ax.set_xticks([0, 1], ["1 thread\n(5 processes)", "4 threads\n(5 processes)"])
        ax.set_xlim(-1.5, 2.5)
        ax.set_ylabel("p50 per process (ms)")
        ax.set_title(f"SVM, {nome}: {dec} (limit ±5%, unchanged)", fontsize=8.5)
        ax.margins(y=0.15)
    fig.tight_layout()
    salvar(fig, "5-svm-1-vs-4-threads.png")


## ---------- 6. Repetições necessárias para o IC ----------
def fig6():
    ls = ler(VAL / "repeticoes-necessarias-para-o-ic.csv")
    fig, eixos = plt.subplots(1, 2, figsize=(10.2, 4.2))
    for ax, modelo, bloco in zip(eixos, (ARVORE, FLORESTA), (29, 10)):
        d = [r for r in ls if r["modelo"] == modelo]
        R = [int(r["processos_R"]) for r in d]
        media = [float(r["meia_largura_media_pct"]) for r in d]
        pior = [float(r["meia_largura_pior_pct"]) for r in d]
        ax.axvspan(5.6, 6.4, color=LARANJA, alpha=0.22, zorder=0)
        ax.axhline(1.0, color=PRETO, linestyle="--", linewidth=0.9)
        ax.text(7.0, 1.03, "criterion 1.0%", fontsize=7.5, va="bottom", ha="left")
        ax.plot(R, media, "o-", color=AZUL, label="Mean over subsets", zorder=3)
        ax.plot(R, pior, "s--", color=VERMELHO, label="Worst subset", zorder=3)
        for r, m, p in zip(R, media, pior):
            caixa = {"facecolor": "white", "edgecolor": "none", "pad": 0.6, "alpha": 0.85}
            ax.text(r, m - 0.07 * max(pior), f"{m:.3f}", ha="center", va="top", fontsize=7, color=AZUL, bbox=caixa, zorder=5)
            ax.text(r, p + 0.05 * max(pior), f"{p:.2f}", ha="center", va="bottom", fontsize=7, color=VERMELHO, bbox=caixa, zorder=5)
        ax.text(6, ax.get_ylim()[1] * 0.97, "R = 6\n(chosen)", ha="center", va="top", fontsize=8.5, fontweight="bold", color=LARANJA)
        ax.set_xticks(R)
        ax.set_xlabel("Processes R (each 10,000 calls)")
        ax.set_ylabel("Half-width of the 95% CI of the p95 (% of the p95)")
        ax.set_title(f"{NOME[modelo]} (block size {bloco})", fontsize=8.5)
        ax.set_ylim(0, max(pior) * 1.18)
        ax.legend(loc="upper right", frameon=False)
    fig.tight_layout()
    salvar(fig, "6-repeticoes-necessarias-para-o-ic.png")


## ---------- 7. p95 por processo ----------
def fig7():
    ls = ler(VAL / "p95-por-processo.csv")
    fig, eixos = plt.subplots(1, 2, figsize=(10.2, 3.9))
    for ax, modelo, cor, casas in zip(eixos, (ARVORE, FLORESTA), (AZUL, LARANJA), (4, 4)):
        d = [r for r in ls if r["modelo"] == modelo]
        ys = [float(r["p95_ms"]) for r in d]
        ax.scatter(range(1, 11), ys, color=cor, s=30, zorder=3)
        for x, y in zip(range(1, 11), ys):
            ax.annotate(f"{y:.{casas}f}", (x, y), xytext=(0, 7), textcoords="offset points", rotation=90, ha="center", va="bottom", fontsize=7, zorder=4)
        m = float(np.median(ys))
        ax.axhline(m, color=PRETO, linewidth=1.2, zorder=2)
        ax.text(10.6, m, f"median\n{m:.4f} ms", va="center", fontsize=7.5)
        ax.set_xticks(range(1, 11))
        ax.set_xlim(0.4, 12.2)
        ax.set_xlabel("Process (10,000 calls each, 1 row per call)")
        ax.set_ylabel("p95 per process (ms)")
        ax.set_title(NOME[modelo], fontsize=8.5)
        lo, hi = min(ys), max(ys)
        ax.set_ylim(lo - (hi - lo) * 0.2, hi + (hi - lo) * 1.0)
    fig.tight_layout()
    salvar(fig, "7-p95-por-processo.png")


## ---------- 8. Latência p95 por modelo, em processo e via HTTP em loopback ----------
def fig8():
    http = {r["label"]: r for r in ler(PAR / "pareto_http.csv")}
    proc = {r["label"]: r for r in ler(PAR / "pareto_inproc.csv")}
    ordem = sorted(http, key=lambda m: float(http[m]["p95_ms"]))
    fig, ax = plt.subplots(figsize=(10.4, 4.6))
    for i, m in enumerate(ordem):
        for r, dy, cor, mk, nome in ((proc[m], 0.17, AZUL, "o", "In process"), (http[m], -0.17, LARANJA, "s", "HTTP on loopback")):
            y = len(ordem) - 1 - i + dy
            p, lo, hi = (float(r[k]) for k in ("p95_ms", "p95_low_ms", "p95_high_ms"))
            ax.errorbar(p, y, xerr=[[p - lo], [hi - p]], color=cor, capsize=3.5, linewidth=1.6, zorder=2)
            ax.scatter(p, y, color=cor, marker=mk, s=16, zorder=3, label=nome if i == 0 else None)
            ax.text(31.2, y, f"{p:.2f} [{lo:.2f}; {hi:.2f}]", va="center", fontsize=7.5, color=cor)
    ax.set_yticks(range(len(ordem))[::-1], ordem)
    ax.set_xlim(0, 31)
    ax.set_xlabel("p95 latency per call, 1 row per call (ms); bars are the 95% CI (exploratory)")
    ax.text(31.2, len(ordem) - 0.35, "p95 [95% CI] (ms)", fontsize=7.5, fontweight="bold")
    ax.legend(loc="center", bbox_to_anchor=(0.55, 0.45), frameon=False)
    ax.grid(axis="x", color="#e6e6e6", linewidth=0.6, zorder=0)
    fig.tight_layout()
    salvar(fig, "8-latencia-p95-em-processo-vs-http-loopback.png")


## ---------- 9. Pareto exploratório de três eixos ----------
def fig9(nome_csv, sufixo, rotulo_lat):
    d = ler(PAR / nome_csv)
    f = lambda r, k: float(r[k])  # noqa: E731
    fig = plt.figure(figsize=(11.2, 6.9))
    gs = fig.add_gridspec(2, 3, height_ratios=[1.0, 0.55], hspace=0.3, wspace=0.28)
    projecoes = [("p95_ms", "mcc", "p95_low_ms", "p95_high_ms", "mcc_low", "mcc_high", f"p95 latency, {rotulo_lat} (ms, log scale)", "MCC on the test set", "(a) MCC × p95", True),
                 ("dpss_mib", "mcc", "dpss_min_mib", "dpss_max_mib", "mcc_low", "mcc_high", "ΔPSS against the null model (MiB)", "MCC on the test set", "(b) MCC × ΔPSS", False),
                 ("p95_ms", "dpss_mib", "p95_low_ms", "p95_high_ms", "dpss_min_mib", "dpss_max_mib", f"p95 latency, {rotulo_lat} (ms, log scale)", "ΔPSS against the null model (MiB)", "(c) ΔPSS × p95", True)]  # fmt: skip
    desloc = [  ## por painel: nome -> deslocamento do rótulo em pontos
        {"DecisionTree": (-8, 10), "LDA": (-12, -2), "GradientBoosting": (8, 10), "GaussianNB": (-6, -22), "QDA": (-4, 14), "SVM": (14, -4), "RandomForest": (-8, 10)},
        {"DecisionTree": (4, 12), "LDA": (-34, -26), "GradientBoosting": (4, 12), "GaussianNB": (-4, -34), "QDA": (34, -30), "SVM": (36, 14), "RandomForest": (-12, -24)},
        {"DecisionTree": (2, 16), "LDA": (-10, -16), "GradientBoosting": (8, 6), "GaussianNB": (14, -26), "QDA": (26, 28), "SVM": (14, -8), "RandomForest": (-8, 10)},
    ]
    for k, (cx, cy, xl, xh, yl, yh, tx, ty, tit, logx) in enumerate(projecoes):
        ax = fig.add_subplot(gs[0, k])
        for r in d:
            x, y = f(r, cx), f(r, cy)
            ax.errorbar(x, y, xerr=[[x - f(r, xl)], [f(r, xh) - x]], yerr=[[y - f(r, yl)], [f(r, yh) - y]], color=CINZA, linewidth=0.9, capsize=0, zorder=1)
            na = r["point"] == "True"
            ax.scatter(x, y, color=LARANJA if na else AZUL, marker="D" if na else "o", s=46, edgecolor="white", linewidth=0.5, zorder=3)
            dx, dy = desloc[k][r["label"]]
            ax.annotate(r["label"], (x, y), xytext=(dx, dy), textcoords="offset points", fontsize=7, ha="left" if dx > 0 else "right",
                        arrowprops={"arrowstyle": "-", "color": CINZA, "linewidth": 0.5} if abs(dx) + abs(dy) > 20 else None)  # fmt: skip
        if logx:
            ax.set_xscale("log")
            ax.set_xticks([5, 7, 10, 20, 30], ["5", "7", "10", "20", "30"])
            ax.minorticks_off()
        ax.set_xlabel(tx)
        ax.set_ylabel(ty)
        ax.set_title(tit, fontsize=8.5)
        ax.margins(0.12)
    ax = fig.add_subplot(gs[1, :])
    ax.axis("off")
    linhas = []
    for r in sorted(d, key=lambda r: f(r, "p95_ms")):
        quem = "yes" if r["point"] == "True" else f"no (dominated by {r['dominated_by']})" if r["dominated_by"] else "no"
        linhas.append([r["label"], f"{f(r, 'mcc'):.4f} [{f(r, 'mcc_low'):.4f}; {f(r, 'mcc_high'):.4f}]", f"{f(r, 'p95_ms'):.2f} [{f(r, 'p95_low_ms'):.2f}; {f(r, 'p95_high_ms'):.2f}]",
                       f"{f(r, 'dpss_mib'):.3f} [{f(r, 'dpss_min_mib'):.2f}; {f(r, 'dpss_max_mib'):.2f}]", quem])  # fmt: skip
    tb = ax.table(cellText=linhas, colLabels=["Model", "MCC [95% CI]", f"p95, {rotulo_lat} (ms) [95% CI]", "ΔPSS (MiB) [min; max]", "On the 3-axis frontier (point estimates)"], loc="center", cellLoc="center")
    tb.auto_set_font_size(False)
    tb.set_fontsize(7.5)
    tb.scale(1, 1.35)
    for (i, j), c in tb.get_celld().items():
        c.set_linewidth(0.3)
        if i == 0:
            c.set_text_props(fontweight="bold")
    tb.auto_set_column_width(range(5))
    fig.text(0.5, 0.005, "Orange diamond: on the frontier of the three axes together · blue circle: dominated · grey bars: 95% CI (MCC, p95) and min to max over repetitions (ΔPSS) · no line is drawn because in three axes the frontier is not a curve", ha="center", fontsize=7.2)
    salvar(fig, f"9-pareto-exploratorio-mcc-p95-dpss-{sufixo}.png")


## ---------- 10. Temperatura por execução ----------
def segmentos(ax, xs, ini, fim, cores, rot_val=True):  ## Segmento antes→depois de cada execução, com os valores escritos.
    for x, a, b, cor in zip(xs, ini, fim, cores):
        ax.plot([x, x], [a, b], color=cor, linewidth=1.2, zorder=2)
        ax.scatter(x, a, facecolor="white", edgecolor=cor, s=22, zorder=3)
        ax.scatter(x, b, color=cor, s=22, zorder=3)
        if rot_val:
            ax.text(x, b + 0.5, f"{b:.1f}", rotation=90, ha="center", va="bottom", fontsize=6)
            ax.text(x, a - 0.5, f"{a:.1f}", rotation=90, ha="center", va="top", fontsize=6)


def fig10():
    ref = sorted(ler(RAIZ / "ref_execucoes.csv"), key=lambda r: r["hora_antes"])
    http = sorted(ler(HTTP / "http_execucoes.csv"), key=lambda r: r["hora_inicio"])
    cond = ler(VAL / "condicoes-da-bateria.csv")

    def rot(r):  ## Nome por extenso da execução da bateria de referência.
        m = r["modelo"]
        if r["rotulo"].startswith("controle"):
            return f"Decision tree, control at {'start' if r['rotulo'].endswith('inicio') else 'end'}"
        if m == "SVM":
            return "SVM, 1 row per call" if r["lotes"] == "1" else f"SVM, 1,024 rows per call (half {r['rotulo'][-1]})"
        if r["seletor"] != "LowVariance":
            return f"{m}, {r['seletor']} ({r['rotulo'].split('-k')[1].split('__')[0]} features)"
        return m

    nomes_cond = ["Same process × new process", "Memory meter cost", "Sampled peak × counter", "Reset of the peak counter", "SVM with 1 × 4 threads", "Repetitions needed for the CI"]
    fig = plt.figure(figsize=(11.4, 14.0))
    gs = fig.add_gridspec(3, 1, height_ratios=[1.0, 1.0, 0.75], hspace=1.0)
    a = fig.add_subplot(gs[0])
    x = range(len(ref))
    segmentos(a, x, [float(r["temp_antes_C"]) for r in ref], [float(r["temp_depois_C"]) for r in ref], [AZUL] * len(ref))
    a.set_xticks(list(x), [rot(r) for r in ref], rotation=40, ha="right", fontsize=7)
    a.set_ylim(48, 82)
    a.set_ylabel("Board temperature (°C)")
    a.set_title("(a) Reference battery, in process (14 runs, in time order): hollow = before, filled = after", fontsize=8.5, loc="left")
    b = fig.add_subplot(gs[1])
    cor_rodada = [AZUL, LARANJA, VERDE, VERMELHO, ROSA]
    segmentos(b, range(len(http)), [float(r["temp_inicio_C"]) for r in http], [float(r["temp_fim_C"]) for r in http], [cor_rodada[int(r["rep"]) - 1] for r in http])
    b.set_xticks(range(len(http)), [f"{r['modelo']} · r{r['rep']}".replace(" · r", " · round ") for r in http], rotation=60, ha="right", fontsize=6)
    for k, cor in enumerate(cor_rodada):
        b.scatter([], [], color=cor, label=f"Round {k + 1}")
    b.legend(loc="lower right", ncol=5, frameon=False, fontsize=7)
    b.set_ylim(48, 74)
    b.set_ylabel("Board temperature (°C)")
    b.set_title("(b) HTTP on loopback (35 runs: 7 models × 5 rounds, in time order): hollow = before, filled = after", fontsize=8.5, loc="left")
    c = fig.add_subplot(gs[2])
    for i, r in enumerate(cond):
        lo, hi = float(r["temp_min_c"]), float(r["temp_max_c"])
        y = len(cond) - 1 - i
        c.hlines(y, lo, hi, color=AZUL, linewidth=5, alpha=0.75)
        c.text(lo - 0.4, y, f"{lo:.1f}", ha="right", va="center", fontsize=7.5)
        c.text(hi + 0.4, y, f"{hi:.1f} °C · {r['celulas_validas']} cell{'s' if r['celulas_validas'] != '1' else ''}", ha="left", va="center", fontsize=7.5)
    c.set_yticks(range(len(cond))[::-1], nomes_cond)
    c.set_xlim(50, 90)
    c.set_xlabel("Board temperature (°C)")
    c.set_title("(c) Method validation of 2026-11-15 (88 cells; minimum to maximum per experiment)", fontsize=8.5, loc="left")
    for ax in (a, b):
        ax.axhline(80, color=VERMELHO, linestyle="--", linewidth=0.9)
        ax.text(ax.get_xlim()[1], 80.3 if ax is a else 73.2, "80 °C: start of throttling", ha="right", va="bottom", fontsize=7, color=VERMELHO)
    c.axvline(80, color=VERMELHO, linestyle="--", linewidth=0.9)
    salvar(fig, "10-temperatura-por-execucao.png")


## ---------- 11. p95 com IC da rodada final, em processo e via HTTP em loopback ----------
def fig11():
    res = ler(RODADA / "resultados_por_modelo.csv")
    res.sort(key=lambda r: float(r["p95_em_processo_us"]))
    medicoes = (("p95_em_processo", AZUL, "o", 0.17, "In process"), ("p95_http_loopback", LARANJA, "s", -0.17, "HTTP on loopback"))
    ## Eixo quebrado: os 6 modelos rápidos à esquerda, a random forest à direita, mesma escala em µs por cm.
    esq, dir_ = (3000, 10700), (22700, 27300)
    fig, (a, b) = plt.subplots(1, 2, figsize=(10.4, 4.4), sharey=True,
                               gridspec_kw={"width_ratios": [esq[1] - esq[0], dir_[1] - dir_[0]], "wspace": 0.05})  # fmt: skip
    n = len(res)
    for i, r in enumerate(res):
        for pre, cor, mk, dy, nome in medicoes:
            y = n - 1 - i + dy
            p, lo, hi = (float(r[f"{pre}{s}"]) for s in ("_us", "_ic95_inferior_us", "_ic95_superior_us"))
            for ax in (a, b):
                ax.hlines(y, lo, hi, color=cor, linewidth=7, alpha=0.35, zorder=2)
                ax.scatter(p, y, color=cor, marker=mk, s=18, zorder=3, label=nome if i == 0 and ax is a else None)
            hw = float(r[f"{pre}_meia_largura_pct"])
            b.text(1.04, y, f"{p:,.0f} [{lo:,.0f}; {hi:,.0f}] ±{hw:.2f}%", transform=b.get_yaxis_transform(),
                   va="center", fontsize=7.5, color=PRETO)  # fmt: skip
    nomes = [{"DecisionTree": "Decision tree", "RandomForest": "Random forest\n(10 processes in process)"}.get(r["modelo"], r["modelo"]) for r in res]
    a.set_yticks(range(n)[::-1], nomes)
    a.set_xlim(*esq)
    b.set_xlim(*dir_)
    b.text(1.04, n - 0.45, "p95 [95% CI] ±half-width (µs)", transform=b.get_yaxis_transform(), fontsize=7.5, fontweight="bold")
    for ax in (a, b):
        ax.grid(axis="x", color="#e6e6e6", linewidth=0.6, zorder=0)
        ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    a.set_xticks(range(4000, 10001, 2000))
    b.set_xticks([23000, 25000, 27000])
    b.spines["left"].set_visible(False)
    b.tick_params(axis="y", left=False)
    a.spines["right"].set_visible(False)
    for ax, x in ((a, 1), (b, 0)):  ## Marcas diagonais da quebra do eixo.
        ax.plot([x - 0.012 * (1 if ax is a else 1.67), x + 0.012 * (1 if ax is a else 1.67)], [-0.02, 0.02], transform=ax.transAxes, color=PRETO, linewidth=0.8, clip_on=False)
    a.legend(loc="lower right", frameon=False)
    fig.supxlabel("p95 latency per call, 1 row per call (µs); shaded band = 95% CI. x axis broken between 10,700 and 22,700 µs (same scale on both sides)", fontsize=8)
    salvar(fig, "11-latencia-p95-com-ic-rodada-final.png")


## ---------- 12. Memória acima do modelo nulo, rodada final ----------
def fig12():
    res = ler(RODADA / "resultados_por_modelo.csv")
    res.sort(key=lambda r: float(r["p95_em_processo_us"]))
    proc = ler(RODADA / "memoria_por_processo.csv")
    grupos = [(r["configuracao"], {"DecisionTree": "Decision tree", "RandomForest": "Random forest"}.get(r["modelo"], r["modelo"])) for r in res]
    grupos.append(("modelo-nulo", "Null model\n(reference, 0 by definition)"))
    fig, ax = plt.subplots(figsize=(8.6, 4.2))
    n = len(grupos)
    for i, (cfg, nome) in enumerate(grupos):
        ys = [float(p["delta_pss_mib"]) for p in proc if p["configuracao"] == cfg]
        y = n - 1 - i
        cor = CINZA if cfg == "modelo-nulo" else AZUL
        ax.scatter(ys, y + np.random.default_rng(i).uniform(-0.12, 0.12, len(ys)), s=20, color=cor, alpha=0.85, edgecolor="white", linewidth=0.4, zorder=3)
        m = float(np.median(ys))
        ax.vlines(m, y - 0.3, y + 0.3, color=PRETO, linewidth=1.4, zorder=4)
        ax.text(12.4, y, f"median {m:.2f}".replace("-", "−") + f" MiB · range {max(ys) - min(ys):.2f} ({len(ys)} processes)", va="center", fontsize=7.5)
    ax.axvline(0, color=CINZA, linewidth=0.8, zorder=1)
    ax.set_yticks(range(n)[::-1], [g[1] for g in grupos])
    ax.set_xlim(-1, 12.2)
    ax.set_xlabel("ΔPSS: PSS of the process minus the median PSS of the null model (MiB); dots = processes, bar = median")
    ax.grid(axis="x", color="#e6e6e6", linewidth=0.6, zorder=0)
    salvar(fig, "12-memoria-acima-do-modelo-nulo-rodada-final.png")


if __name__ == "__main__":
    fig1()
    dif = fig2()
    print("diferenças medianas do medidor (µs):", {k: round(float(v), 2) for k, v in dif.items()})
    fig3()
    fig4()
    fig5()
    fig6()
    fig7()
    fig8()
    fig9("pareto_http.csv", "http-loopback", "HTTP on loopback")
    fig9("pareto_inproc.csv", "em-processo", "in process")
    fig10()
    fig11()
    fig12()
