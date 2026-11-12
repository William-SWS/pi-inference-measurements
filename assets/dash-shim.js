/* Substitui a API do dashboard do Claude para a página rodar sozinha: lê os CSVs embutidos na própria página. */
(function () {
  const parsed = {}, calcs = {}, calcCache = {}, draws = {}, onDataFns = [];
  function raw(id) {
    if (!(id in parsed)) {
      const el = document.getElementById('csv-' + id);
      parsed[id] = el ? d3.csvParse(el.textContent.trim()) : null;
    }
    return parsed[id];
  }
  function data(id) {
    if (calcs[id]) {
      if (!(id in calcCache)) {
        const c = calcs[id];
        calcCache[id] = c.fn(...c.inputs.map((i) => data(i).data));
      }
      return { status: 'ok', data: calcCache[id], meta: [] };
    }
    const r = raw(id);
    return r ? { status: 'ok', data: r, columns: r.columns, meta: [] } : { status: 'missing', data: [] };
  }
  function runDraw(name) {
    const d = draws[name]; if (!d) return;
    document.querySelectorAll('[data-draw="' + name + '"]').forEach((el) => {
      if (el.closest('[hidden]')) return;
      try { d(el); } catch (e) { console.error('desenho ' + name, e); }
    });
  }
  window.dash = {
    colors: ['var(--lp-c0)', 'var(--lp-c1)', 'var(--lp-c2)', 'var(--lp-c3)'],
    data,
    calc(id, def) { calcs[id] = def; },
    loader() {},
    onData(fn) { onDataFns.push(fn); try { fn(); } catch (e) { console.error(e); } },
    draw(name, fn) {
      if (typeof fn === 'function') { draws[name] = fn; if (window.__lpPronto) runDraw(name); }
      else runDraw(name);
    },
    refresh() {}, params: () => ({}), setParams() {}, resetParams() {}, setLink() {},
    _runAll() {
      window.__lpPronto = true;
      onDataFns.forEach((f) => { try { f(); } catch (e) { console.error(e); } });
      Object.keys(draws).forEach(runDraw);
    }
  };
  let largura = 0, timer = null;
  window.addEventListener('resize', () => {
    clearTimeout(timer);
    timer = setTimeout(() => {
      if (window.innerWidth === largura) return;
      largura = window.innerWidth;
      onDataFns.forEach((f) => f());
      Object.keys(draws).forEach(runDraw);
    }, 150);
  });
  largura = window.innerWidth;
})();
