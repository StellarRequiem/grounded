# AI-output verification: the 2026 landscape

_A cited research report produced by a multi-agent deep-research run (107 agents · 25 sources · 25 claims adversarially 3-vote verified → 23 confirmed, 2 killed), then independently audited by `grounded` against each claim's source._

## Open-source layer

DeepEval, an open-source LLM-evaluation framework, has roughly 15.9k GitHub stars and 1.5k forks, and ships dedicated hallucination, faithfulness, and agent-evaluation metrics ([repo](https://github.com/confident-ai/deepeval)).

Ragas, an Apache-2.0 RAG and LLM-output evaluation toolkit, has about 14.2k GitHub stars ([repo](https://github.com/explodinggradients/ragas)).

Vectara's HHEM-2.1-Open, an Apache-2.0 hallucination-detection model, recorded 106,917 Hugging Face downloads in the last month ([model card](https://huggingface.co/vectara/hallucination_evaluation_model)).

LM-Polygraph, an MIT-licensed uncertainty-quantification framework, implements over 40 UQ methods ([repo](https://github.com/IINemo/lm-polygraph)).

## Commercial / market layer

Galileo raised a $45 million Series B in October 2024, led by Scale Venture Partners ([announcement](https://galileo.ai/blog/announcing-our-series-b)).

A wave of observability and evaluation vendors — LangChain, Braintrust, and Judgment Labs — is building the runtime observability layer for AI, per Menlo Ventures' 2025 enterprise report ([Menlo](https://menlovc.com/perspective/2025-the-state-of-generative-ai-in-the-enterprise/)).

## Academic layer

An October 2025 arXiv survey introduces a structured taxonomy of hallucination-detection approaches across five method families ([survey](https://arxiv.org/abs/2510.06265)).

A December 2025 Meta FAIR method trains linear probes on a reasoning judge's hidden states with a Brier-score loss to give calibrated uncertainty ([paper](https://arxiv.org/abs/2512.22245)).

## Refuted in verification (do not trust)

A claim that FaithJudge reaches 84% balanced accuracy on FaithBench was refuted (1 confirm, 2 refute).

A claim that the probe method delivers a 10x cost reduction was refuted (1 confirm, 2 refute).
