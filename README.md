# OptiChat Appendix C prompts on Qwen 2.5 and Llama 3.1

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Priyanshi8806/optichat-colab/blob/main/notebooks/optichat_appendixC_colab.ipynb)

This is a Colab notebook where I try the agent prompts from Appendix C of *OptiChat: Bridging Optimization Models and Practitioners with LLMs*
(Chen et al., INFORMS Journal on Data Science, 2026, [doi:10.1287/ijds.2025.0074](https://doi.org/10.1287/ijds.2025.0074)) on two open models:
Qwen2.5-7B-Instruct and Llama-3.1-8B-Instruct. No other models are supported.

The notebook goes through every Appendix C item: component interpretation, model illustration, IIS inference, coordinator, explainer, syntax reminder, operator,
code reminder, the programmer (with its two worked examples) and the evaluator. After that it runs the whole coordinator, engineer and explainer loop
and finishes with a small scoreboard comparing the two models.

## How to run it

1. Click the Colab badge above, then go to Runtime > Change runtime type and pick a **T4 GPU**.
2. Qwen works as is. Llama 3.1 is gated, so you need to accept Meta's license on the
   [model page](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct), make a Hugging Face token with read access, and save it in Colab Secrets
   as `HF_TOKEN` (turn on notebook access for it). If you skip Llama, change `USE` to `["qwen"]` in the second code cell.
3. Run all cells. On a free T4 this takes roughly 25 to 40 minutes. Set `FAST = True` if you want to skip the last end-to-end section.

Please don't paste your token into the notebook or commit it to the repo.

## What this is and isn't

- The prompts are written in my own words, based on the roles the paper describes. They are not the paper's exact text, since that belongs to the publisher.
  If you want the original wording, there is an empty `EXACT` cell where you can paste it from your own copy.
- The models being optimized are two small toy Pyomo examples (one MILP, one LP), not the 24 models from the paper. The test sets are tiny too,
  so treat the scoreboard as a quick check of where each model breaks, not as a proper benchmark.
- The solver tools (IIS, feasibility restoration, sensitivity from LP duals, what-if, and the counterfactual runner) don't use an LLM at all. I checked them against an
  independent LP solve, finite differences and a known IIS. The counterfactual code runner limits builtins, but it is not a real sandbox, so don't run untrusted code in it.
- `tests/test_notebook_stub.py` runs the notebook with a fake LLM to make sure the plumbing and scoring work. It tells you nothing about how good Qwen or Llama are.

## Licenses

- The code here is MIT licensed (see `LICENSE`).
- Built with Llama. Llama 3.1 is used under the Llama 3.1 Community License, and you have to accept Meta's license to download it.
- Qwen2.5-7B-Instruct is Apache-2.0.
- The paper itself isn't included. Please cite it using the details in `NOTICE.md`.
