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
    titulo: 'Lote2: sem registrador ao lado, ordem espelhada e memória de todas as repetições',
    resumo: 'Ajustes no método depois do lote1, para tirar o efeito do observador e compensar o aquecimento do rasp.'
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
  },
  {
    id: '2026-11-13-latencia-http-loopback',
    data: '2026-11-13',
    tipo: 'medicao',
    status: 'Exploratória',
    titulo: 'Latência via HTTP em loopback no rasp',
    resumo: 'Latência do serviço de inferência chamado por HTTP no próprio rasp (loopback, sem rede real), com 7 modelos em 5 rodadas: p95 com intervalo de confiança ao lado do p95 em processo, custo do HTTP e do JSON e deriva com a temperatura.'
  },
  {
    id: '2026-11-14-pareto-exploratorio',
    data: '2026-11-14',
    tipo: 'medicao',
    status: 'Exploratória',
    titulo: 'Pareto exploratório de três eixos: MCC, p95 e ΔPSS',
    resumo: 'Rascunho da fronteira de Pareto de 7 modelos com as medições que já existem, em processo e via HTTP em loopback. O Pareto final usa os dados da rodada de 16/11.'
  },
  {
    id: '2026-11-15-validacao-do-metodo-de-medicao',
    data: '2026-11-15',
    tipo: 'medicao',
    status: 'Validada',
    titulo: 'Validação do método de medição',
    resumo: 'Seis experimentos que testam a régua, não os modelos: mesmo processo × processo novo, custo do medidor de memória, pico amostrado × contador, zerar o contador de pico, SVM com 1 × 4 threads e repetições necessárias para o IC (decisão: R = 6).'
  },
  {
    id: '2026-11-16-rodada-final-sem-estresse',
    data: '2026-11-16',
    tipo: 'medicao',
    status: 'Validada',
    titulo: 'Rodada final sem estresse: latência e memória de 7 modelos',
    resumo: 'Latência em processo e via HTTP em loopback e memória dos 7 modelos LowVariance, com o método validado: as 14 meias-larguras do p95 ficaram dentro de 1,0%. Os números alimentam o Pareto final e seguem exploratórios até ele.'
  }
];
