/*
  Linha do tempo do acompanhamento, em ordem cronológica.
  Para acrescentar uma etapa: crie a pasta etapas/<id>/ com um index.html
  (copie uma etapa do mesmo tipo) e acrescente um item no fim desta lista.

  tipo:   "medicao" (bateria de medição, com gráficos) ou "nota" (decisão ou mudança, só texto)
  status: texto curto livre, por exemplo "Exploratória", "Validada", "Aplicada", "Descartada"
*/
window.ETAPAS = [
  {
    id: '2026-11-11-reinicio-cgroup-psi',
    data: '2026-11-11',
    tipo: 'nota',
    status: 'Aplicada',
    titulo: 'Reinício com o controlador de memória do cgroup e o PSI ligados',
    resumo: 'Mudança de configuração do sistema feita entre a primeira execução (c0) e as seguintes.'
  },
  {
    id: '2026-11-11-lote2-ordem-sem-registrador',
    data: '2026-11-11',
    tipo: 'nota',
    status: 'Aplicada',
    titulo: 'Lote2: sem registrador ao lado, ordem A B C C B A e memória de todas as repetições',
    resumo: 'Ajustes no método depois do lote1, para tirar o efeito do observador e compensar o aquecimento do Pi.'
  },
  {
    id: '2026-11-11-lote1-lote2',
    data: '2026-11-11',
    tipo: 'medicao',
    status: 'Exploratória',
    titulo: 'Primeiras medições: lote1 e lote2',
    resumo: 'Latência em processo e memória da árvore de decisão LowVariance em 11 execuções, com foco no governor performance.'
  },
  {
    id: '2026-11-12-bateria-modelos',
    data: '2026-11-12',
    tipo: 'medicao',
    status: 'Exploratória',
    titulo: 'Bateria de referência: 7 modelos em 11 configurações',
    resumo: 'Latência em processo e memória de 7 modelos (11 configurações com os seletores) na condição de referência: desktop desligado e governor performance.'
  }
];
