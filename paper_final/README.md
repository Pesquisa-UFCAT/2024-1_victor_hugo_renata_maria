# Paper final da dissertação — material de trabalho

Comece por aqui:

1. [tutorial_paper.md](tutorial_paper.md) — roteiro do paper: pergunta, contribuições, fases com checklist, seções, figuras e perguntas de revisor.
2. [tutorial_benchmark.md](tutorial_benchmark.md) — exemplo de referência passo a passo com o emulador de g(t).
3. [tutorial_benchmark_g.py](tutorial_benchmark_g.py) — script do benchmark. Na raiz do repositório: `python paper_final/tutorial_benchmark_g.py`. Requer os `.pkl` treinados em `durability/` (NNs de λ₁/λ₂, scaler, dataset_nn).

Pastas:

- `saida_referencia/` — saída esperada do script (log, CSVs, figura de trabalho), para conferir a execução.
- `apoio/` — documentos e resultados anteriores: plano de redação, revisão bibliográfica integrada, benchmark por MC direto (`bench_voi.py` e resultados) e protótipos E1–E4.
  Os scripts de `apoio/` (`bench_voi.py`, `e_common.py`, `e_sim.py`) usam `apoio/inputs/` (`possan_standalone.py` e a série de CO₂); para rodá-los, entre em `apoio/`. Servem como registro, não precisam ser rodados.
