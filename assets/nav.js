/*
  Navegação do site. Cada página declara no <body>:
    data-raiz="../../"   caminho relativo até a raiz do site ("" na página inicial)
    data-etapa="<id>"    id da etapa (vazio na página inicial)
  e tem, se quiser, <nav id="site-nav"></nav>, <nav id="site-pager"></nav> e <ol id="linha-do-tempo"></ol>.
*/
(function () {
  const etapas = (window.ETAPAS || []).slice();
  const corpo = document.body;
  const raiz = corpo.dataset.raiz || '';
  const atual = corpo.dataset.etapa || '';
  const idx = etapas.findIndex((e) => e.id === atual);
  const meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez'];
  const fmtData = (iso) => { const [a, m, d] = iso.split('-'); return +d + ' ' + meses[+m - 1] + ' ' + a; };
  const tipoRot = { medicao: 'Medição', nota: 'Nota' };
  const href = (e) => raiz + 'etapas/' + e.id + '/';
  const el = (tag, cls, txt) => { const n = document.createElement(tag); if (cls) n.className = cls; if (txt != null) n.textContent = txt; return n; };

  // Barra do topo
  document.querySelectorAll('#site-nav').forEach((nav) => {
    const a = el('a', 'site-marca', 'Medições no Raspberry Pi');
    a.href = raiz || './';
    const sel = el('select', 'site-ir');
    sel.setAttribute('aria-label', 'Ir para a etapa');
    const op0 = new Option(idx < 0 ? 'Ir para uma etapa…' : 'Linha do tempo', raiz || './');
    sel.appendChild(op0);
    etapas.forEach((e, i) => {
      const o = new Option((i + 1) + '. ' + fmtData(e.data) + ' · ' + (tipoRot[e.tipo] || e.tipo) + ' · ' + e.titulo, href(e));
      if (i === idx) o.selected = true;
      sel.appendChild(o);
    });
    sel.addEventListener('change', () => { location.href = sel.value; });
    const pos = el('span', 'site-pos', idx >= 0 ? 'Etapa ' + (idx + 1) + ' de ' + etapas.length : etapas.length + ' etapas');
    nav.replaceChildren(a, pos, sel);
  });

  // Anterior / próxima
  document.querySelectorAll('#site-pager').forEach((nav) => {
    if (idx < 0) { nav.hidden = true; return; }
    const lado = (e, rot, cls) => {
      if (!e) return el('span', 'site-vazio');
      const a = el('a', 'site-pag ' + cls);
      a.href = href(e);
      a.append(el('span', 'site-pag-rot', rot), el('span', 'site-pag-tit', fmtData(e.data) + ' · ' + e.titulo));
      return a;
    };
    nav.replaceChildren(lado(etapas[idx - 1], '← Anterior', 'site-ant'), lado(etapas[idx + 1], 'Próxima →', 'site-prox'));
  });

  // Cabeçalho da etapa (data, tipo, status)
  document.querySelectorAll('#etapa-meta').forEach((p) => {
    if (idx < 0) return;
    const e = etapas[idx];
    p.replaceChildren(
      el('span', 'site-data', fmtData(e.data)),
      el('span', 'site-tipo site-tipo-' + e.tipo, tipoRot[e.tipo] || e.tipo),
      el('span', 'site-status', e.status)
    );
  });

  // Linha do tempo (página inicial)
  document.querySelectorAll('#linha-do-tempo').forEach((ol) => {
    ol.replaceChildren(...etapas.map((e, i) => {
      const li = el('li', 'lt-item lt-' + e.tipo + (i === etapas.length - 1 ? ' lt-ultima' : ''));
      const meta = el('div', 'lt-meta');
      meta.append(el('span', 'site-data', fmtData(e.data)), el('span', 'site-tipo site-tipo-' + e.tipo, tipoRot[e.tipo] || e.tipo), el('span', 'site-status', e.status));
      const a = el('a', 'lt-titulo', e.titulo); a.href = href(e);
      li.append(el('span', 'lt-ponto'), meta, a, el('p', 'lt-resumo', e.resumo));
      return li;
    }));
  });
})();
