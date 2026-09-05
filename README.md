# coreai-assets

Core AI is Apple's on-device ML runtime in iOS 27 / macOS 27 and the successor to Core ML: PyTorch models are exported with Apple's `coreai-torch` (LLMs: `coreai.llm.export`) into `.aimodel` bundles that run on the GPU or the Neural Engine, e.g. Qwen3-8B 4-bit decodes at 94 tok/s on an M4 Max GPU, MLX 90 under the same protocol ([apple-silicon-llm-bench](https://github.com/john-rocky/apple-silicon-llm-bench), macOS 27 beta, 2026-06).

Demo media (GIFs / screenshots) referenced by the READMEs of
[coreai-kit](https://github.com/john-rocky/coreai-kit) and
[coreai-model-zoo](https://github.com/john-rocky/coreai-model-zoo).
Kept in a separate repo so the code repos stay small to clone.

All captures are real devices (iPhone 17 Pro / M4 Max), models running fully on-device.
