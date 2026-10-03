# demos

Short clips that show a zoo model doing the thing its card claims. Every frame is produced by
running the models, not illustrated — if a number or a transcript is on screen, it came out of a
real run on the machine named beside it.

## `clef-flash-mac.mp4` (13 s)

A customer email fills an 8-field support ticket at once on a Mac Studio (M4 Max, 128 GB): team,
priority, customer mood, next step, needed-by date and three yes/no flags. The model is
[clef-flash](https://github.com/john-rocky/coreai-model-zoo/blob/main/models/clef-flash/README.md),
Cloudflare's Qwen3.5-9B decision model, converted to Core AI. It reads the email and the eight
questions once (934 tokens, 15 decoder calls on the GPU, fp16 weights) and returns a probability for
every option. The screen is the samples app
[CoreAIDecisionFormMac](https://github.com/john-rocky/coreai-samples/tree/main/CoreAIDecisionFormMac);
the email and its sender are invented.

"2.47 s" on screen is the app's own clock around that one decision, loading not counted. The run:
2026-10-03 23:32 JST, macOS 27.0 (26A428), Release build, the `.aimodel` files specialized for this Mac
by the runtime (JIT, read from the app's cache), the app relaunched and warmed up with one short
decision before the press, no other GPU job running (the GPU at 0 % just before the press). The clip
is a window recording of that run (`screencapture -l`, the title bar cut), normal speed, no audio;
sha256 `3f98f0541118ede899fd7a85ca6425d257ebd597b98e5f2f25da6f78bc477f5a`.

Rebuild it: `CoreAIDecisionFormMac -autoplay form -modelsFolder <dir> -trigger <file> -log 1` (the app's
README) presses Sample email once the model is ready; record the window with
`screencapture -l <window id> -V 16 -x`.

## `nemotron-3-diarization-iphone.mp4` (86 s) and `nemotron-3-diarization-iphone-still.png`

A synthetic 8-person meeting (74 s, voices from the zoo's Kokoro TTS port, a fictional company and
fictional names) plays on an iPhone 17 Pro while
[Nemotron-3-Diarization](https://github.com/john-rocky/coreai-model-zoo/blob/main/models/nemotron-3-diarization/README.md)
labels who is speaking, streaming, about 1 s behind the audio (the model's 1.04 s look-ahead plus
0.05 s of compute per 0.72 s chunk on the phone's GPU). The screen is coreai-audio's Diarize live view;
the recording is QuickTime's mirror of the phone with the phone's own audio. Numbers on screen come
from that run (2026-09-25 01:02, iOS 27.0). Posted on X on 2026-09-25.

Rebuild it: `apps/coreai-audio/record-demo.sh n3d_meeting_16k` in the zoo (the app installed with the
`N3DAssets` sideload; `--captions` adds the two caption lines).

## `pocket-tts-vs-kokoro.mp4` (15 s)

One sentence — *"The bass player from Vyrantha read the lead sheet."* — read by two on-device
Core AI text-to-speech models, with a third reading back what each one said.

- **Kokoro-82M**, through CoreAIKit's dictionary G2P, cannot look up the invented name and spells
  it out: Parakeet transcribes *"The bass player from V Y R A N T H A Read the Lead Sheet"*.
  The spelling is that G2P's design, not the model's: misaki's full pipeline has a seq2seq
  fallback for out-of-dictionary words, and it needs Python, so the on-device port ships the
  dictionary core alone. The clip says so on its last card.
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
