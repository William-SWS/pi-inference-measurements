# Medições de inferência no Raspberry Pi

Site estático com o acompanhamento cronológico das medições de inferência do detector de DoS em MQTT num Raspberry Pi 4 (árvore de decisão LowVariance). Medições exploratórias; nenhum número daqui é resultado final.

Esta versão é pública e traz só gráficos e números agregados: não inclui a duração de cada chamada.

## Estrutura

```
index.html                 página inicial com a linha do tempo
assets/etapas.js           lista das etapas, em ordem cronológica (é aqui que a navegação é montada)
assets/nav.js              barra do topo, "anterior / próxima" e linha do tempo
assets/estilo.css          cores, fontes e layout (tema claro e escuro)
assets/dash-shim.js        faz as páginas de medição rodarem sozinhas, com os dados embutidos
assets/d3.min.js           d3 v7.9.0
etapas/<id>/index.html     uma página por etapa
```

Não há etapa de build: o GitHub Pages serve os arquivos como estão, e as páginas também abrem direto do disco.

## Acrescentar uma etapa

1. Crie a pasta `etapas/<id>/`, com um id que comece pela data (`2026-11-20-lote3`).
2. Copie o `index.html` de uma etapa do mesmo tipo:
   - **nota** (texto): copie `etapas/2026-11-11-reinicio-cgroup-psi/index.html` e troque o texto;
   - **medição** (gráficos): copie `etapas/2026-11-11-lote1-lote2/index.html`; os dados ficam nos blocos `<script type="text/csv" id="csv-...">` no fim da página.
3. Troque `data-etapa="..."` no `<body>` pelo novo id.
4. Acrescente um item no fim da lista em `assets/etapas.js` (`id`, `data`, `tipo`, `status`, `titulo`, `resumo`).

A página inicial, o menu do topo e os links de anterior/próxima se atualizam sozinhos.

## Publicar no GitHub Pages

Settings → Pages → *Build and deployment* → Source: **Deploy from a branch** → Branch: `main`, pasta `/ (root)`.

## Paleta

Contraste pela fórmula WCAG 2.x. "Painel" é o fundo dos módulos; "fundo" é o fundo da página. Texto pede 4,5:1; elementos gráficos pedem 3:1.

| Token | Uso | Claro | Painel / fundo | Escuro | Painel / fundo |
|---|---|---|---|---|---|
| `--color-fg` | texto | `#0E1620` | 18,19 / 16,77 | `#E4EBF2` | 14,87 / 15,99 |
| `--color-fg-muted` | texto secundário | `#4B5A6B` | 7,06 / 6,51 | `#93A3B5` | 6,94 / 7,46 |
| `--lp-c0` / `--color-accent` | marca, links, foco, série do foco | `#1B5FD0` | 5,84 / 5,39 | `#5C9DFF` | 6,57 / 7,07 |
| `--lp-c1` | desligado · ondemand | `#00796B` | 5,32 / 4,90 | `#45D0B8` | 9,34 / 10,04 |
| `--lp-c2` | ligado · ondemand | `#7A2A8F` | 8,22 / 7,58 | `#D46AC0` | 5,64 / 6,06 |
| `--lp-c3` | registrador ao lado | `#6B6B00` | 5,63 / 5,19 | `#C9C45A` | 9,81 / 10,56 |
| `--cds-chart-muted` | kernel antigo, referências | `#5F6B78` | 5,44 / 5,01 | `#8A97A6` | 6,01 / 6,46 |
| `--color-bad` | chamada lenta | `#C42B1C` | 5,66 / 5,22 | `#FF6B5C` | 6,39 / 6,88 |
| `--color-warn` | ressalvas (borda, ícone) | `#B26B00` | 3,88 sobre `#FFF5E1` | `#E8B23E` | 9,25 sobre `#1C1708` |
| `--color-warn-fg` | título das ressalvas | `#8A4F00` | 6,06 sobre `#FFF5E1` | `#F0C462` | 10,87 sobre `#1C1708` |
| `--color-ok` | indicador "Aplicada" | `#1F7A3E` | 5,37 / 4,95 | `#4CC27A` | 7,92 / 8,52 |

Superfícies: fundo `#F3F6F9` / `#0A0F15`, painel `#FFFFFF` / `#101821`, painel 2 `#EEF2F6` / `#0D141C`, borda `#CED7E1` / `#24313F`, cantos `#A9B6C4` / `#3A4D62`.

Daltonismo: a menor distância ΔE (CAM02-UCS) entre as cinco cores de série foi medida em simulação. Em deuteranopia ela fica em 4,9 no tema claro e 7,4 no escuro, e o par mais próximo é verde-azulado × cinza. Em protanopia fica entre 11 e 12,7, e em tritanopia entre 9,2 e 12,1. Nos gráficos, todo grupo tem rótulo de texto, então a cor nunca é a única pista. Azul × vermelho, os dois do histograma, fica acima de 43 em todos os casos.
