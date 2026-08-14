# demos

Short clips that show a zoo model doing the thing its card claims. Every frame is produced by
running the models, not illustrated — if a number or a transcript is on screen, it came out of a
real run on the machine named beside it.

## `pocket-tts-vs-kokoro.mp4` (15 s)

One sentence — *"The bass player from Vyrantha read the lead sheet."* — read by two on-device
Core AI text-to-speech models, with a third reading back what each one said.

- **Kokoro-82M** reaches its dictionary G2P, cannot look up the invented name, and spells it out:
  Parakeet transcribes *"The bass player from V Y R A N T H A Read the Lead Sheet"*.
- **pocket-tts** takes the text itself and has no G2P layer to miss with:
  *"The bass player from Virantha read the lead sheet."*

Both TTS models ran through their published Core AI bundles on an M4 Max; the transcripts are
[Parakeet-TDT-0.6B](https://github.com/john-rocky/coreai-model-zoo/blob/main/models/parakeet/README.md)
on the same machine. The speed figure at the end is pocket-tts's own, generation-only —
Kokoro's is deliberately absent, because the number available here is process wall time
including model load and the two protocols do not match.

pocket-tts was ported by [Rahul Rachuri](https://github.com/RahulRachuri)
([zoo PR #12](https://github.com/john-rocky/coreai-model-zoo/pull/12)), and the G2P argument the
clip demonstrates is his, from the request thread that started the port.

Rebuild it: `make_compare_video2.py` in the zoo's scratch tooling renders every frame from the
wavs, so the waveform is the real envelope and the transcript types at the playhead.
