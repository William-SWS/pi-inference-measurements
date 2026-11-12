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
