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
sha256 `3f98f0541118ede899fd7a85ca6425d257ebd597b98e5f2f25da6f78bc477f5a`. Posted on X on 2026-10-04.

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

## `eg2-transcribe-coreai-mac-20261014.mp4` (12 s)

An 8.6 s LibriVox clip becomes text on a Mac Studio (M4 Max, 128 GB): the opening clause of *The Adventure of the
Speckled Band* (read by Kirsten Ferreri, public domain) goes into EG2 Transcribe and its 27 words appear, all of them
the words of the reference transcript. The app is `ios/` of
[eg2-transcribe](https://github.com/john-rocky/eg2-transcribe) (SwiftUI); the models are the EmbeddingGemma 2 audio
encoder and the eg2-transcribe reader v1 converted to Core AI
([mlboydaisuke/EmbeddingGemma-2-Transcribe-CoreAI](https://huggingface.co/mlboydaisuke/EmbeddingGemma-2-Transcribe-CoreAI)),
the encoder on the GPU and the reader with the Neural Engine preferred, the app's default on a Mac.

"109 ms · ×79" on screen is the app's own clock from the file to the words (decode, log-mel, one 30 s window through
both bundles), loading not counted. The run: 2026-10-14 13:26 JST, macOS 27.0 (26A428), Release build, the model folder
= the published files, the Core AI cache warm (the same folder had transcribed this clip once before the take), the GPU
idle (≤ 5 % for 10 s) before the take. The clip is a window recording of that run (`screencapture -l`, the toolbar cut),
normal speed, no audio; sha256 `b264751be9ad54b2e68e9caf16ede17ab43caa9e5e1ffbefd93cb2579b600524`.

Rebuild it: with the model folder in place (downloaded by the app, or copied to the folder its empty state names),
`EG2Transcribe.app/Contents/MacOS/EG2Transcribe -autoplay <wav> -textSize 44` (the app's README) opens the file the way
*Choose audio* does once the model is loaded; record the window with `screencapture -l <window id> -V 18 -x`.

## `eg2-transcribe-coreai-mac-20261015.mp4` (12 s)

The same clip with reader v2 (6 layers, trained on LibriSpeech 960 h; reader v1 above was trained on train-clean-100):
the 8.6 s opening clause of *The Adventure of the Speckled Band* goes into EG2 Transcribe on the Mac Studio (M4 Max,
128 GB) and its 27 words appear, 26 of them the words of the reference transcript (the first comes out as "i'm" for
"on"; the clip starts at a pause in the middle of the sentence). The models are the published folder of
[mlboydaisuke/EmbeddingGemma-2-Transcribe-CoreAI](https://huggingface.co/mlboydaisuke/EmbeddingGemma-2-Transcribe-CoreAI)
at revision `76865ae4`, the encoder on the GPU and reader v2 with the Neural Engine preferred, the app's default on a Mac.

"105 ms · ×82" on screen is the app's own clock from the file to the words (decode, log-mel, one 30 s window through
both bundles), loading not counted. The run: 2026-10-15 23:02 JST, macOS 27.0 (26A428), Release build, the Core AI cache
warm (the same folder had transcribed this clip once before the take), the GPU idle (≤ 5 % for 10 s) before the take.
The clip is a window recording of that run (`screencapture -l`, the toolbar cut), normal speed, no audio; sha256
`8ff948d65876a174915750e58a04284f8b7c0ab33dc59688cc5dfa5899057b2e`. Rebuild it as above.

## `eg2-transcribe-coreai-iphone-20261016.mp4` (12 s)

A 3.1 s sentence of the same LibriVox chapter ("my dear fellow i would not miss it for anything", read by Kirsten
Ferreri, public domain) becomes text on an iPhone 18 Pro (iOS 27.2): EG2 Transcribe opens the file the way *Choose
audio* does and its 10 words appear, all of them the words of the reference transcript. The models are the published
folder of
[mlboydaisuke/EmbeddingGemma-2-Transcribe-CoreAI](https://huggingface.co/mlboydaisuke/EmbeddingGemma-2-Transcribe-CoreAI)
at revision `76865ae4` (`ios-h19p/`: the encoder and reader v2 compiled for the iPhone 18 Pro), the encoder and the
reader on the GPU one window at a time, the app's default on an iPhone.

"156 ms · ×20" on screen is the app's own clock from the file to the words (decode, log-mel, one 30 s window through
both bundles), loading not counted; it is the first call after the launch, so slower per second of audio than the
54-minute recording (12.0 s, ×271). The run: 2026-10-16 02:09 JST, Release build, thermal nominal, USB power. The clip is
a capture of the phone's screen mirrored to the Mac over USB (the status bar's 9:41 is the mirror's own), the whole
screen at 874 × 1900, normal speed, no audio; sha256
`57d1749282b7665442692aeaf8c65087a294a4a0db8e554560557928410e79b5`.

Rebuild it: with the model folder in the app's container, launch the app with `-autoplay <wav> -textSize 44` (devicectl,
the app's README) and record the mirrored screen.

## `minicpm-v-4.7-1b-watch-iphone-20261024.mp4` (40.7 s, with audio)

Three rules typed as sentences — *water rushing over rows of stones* → Ripple, *a road bridge crossing over the river* →
Spotlight (sound: horn), *a church with a tall spire* → Zoom (sound: bells) — and a drone clip (CC0, Wikimedia Commons: a
river running over rows of stones, a road bridge, then a church with a spire among houses; no face, text or logo can be
read in it) playing on an iPhone 18 Pro (iOS 27.2). Start, and the model checks one frame at a time with one yes / no
line per rule; when a rule's answer turns yes, the app asks the model where the thing is in the model's own grounding
form ("Detect <condition> in the picture and output its bounding box."), reads the first box of the answer, then holds
the frame the model answered — the crop it saw, with a thin blue border — for 3 s while it edits that frame at the box
(Core Image on the frame itself) and plays a short sound: Ripple spreads a circular wave from the box's middle and tints
the wake blue, Spotlight keeps the box as it was (with a soft edge) and dims and desaturates the rest, Zoom enlarges
the picture into a window around the box. The video is paused during a hold and goes on from where it stopped; the row
turns YES; no words or symbols appear for a fire. The model is MiniCPM-V 4.7 1B converted to Core AI
([mlboydaisuke/MiniCPM-V-4.7-1B-CoreAI](https://huggingface.co/mlboydaisuke/MiniCPM-V-4.7-1B-CoreAI) at revision
`51278afd`, the `gpu-pipelined/` bundles: the decoder and the vision tower on the GPU). The screen is the Watch screen of
the kit example [Examples/Look](https://github.com/john-rocky/coreai-kit/tree/main/Examples/Look): rules in words, one
reaction each (a sound, a buzz, a spoken line, a timer, a count, a log line, or an effect = an edit of the held frame
with a sound of its choice), and the camera, a picked video or the example photos as the source. The three sounds are
CC0 recordings from Wikimedia Commons cut to 2.3–3.0 s (running water, a car horn, a church bell; the example's README
lists the source pages).

"first token 1.38 s · total 1.49 s" on screen is the app's own clock for the last frame: from the frame's call to the
model to its first streamed text, and from taking the frame to its answer read; loading not counted (the model loads
before READY), the box question and the hold not counted (they come after the answer). Over the run: 15 frames, the
run 35.6 s (the 26 s video and three holds of 3 s), a median of 1,500 ms per frame (the first token after 1,383 ms),
131 tokens in and 11–14 out per frame; each box question took 1,278–1,340 ms more (24–29 answer tokens). The rules
fired on the frames taken 0.02 s, 5.78 s and 16.11 s into the video — each within about a second of the seconds where
the same model on a Mac, given one frame a second with the same prompt, first answers yes (0, 5 and 15 s) — and nothing
else fired. The boxes the model returned (per mille of the frame: left, top, right, bottom): `238 0 688 998` for the
water (the river band; the box's middle on the water), `588 0 1000 181` for the bridge (the deck and abutment at the top
right; the middle on the deck), `505 0 575 308` for the church (a strip beside the tower: its middle 8 ‰ of the width
left of the tower and nave as drawn by eye; the zoom's window, 2.16×, holds the tower, the chapel and the trees beside
them). Each hold started 2.76–2.84 s after its frame was taken (the yes / no answer, then the box question), its sound
15–30 ms after that, and held the frame 3,015–3,032 ms. The run: 2026-10-24 02:46 JST, Release build (Look 1.0 from
commit 1fb9943 of the example), a new process after a warm-up run, thermal nominal before and after, memory footprint
344–414 MB, USB power, Wi-Fi on (so the line says `on-device`, not `offline`). The clip is the phone's screen mirrored
to the Mac over USB with the phone's audio (AAC, 48 kHz), the app's 9:16 take layout cut to 1080 × 1920 at 30 fps (the
status bar cut), from 3 s before Start to 2 s after the app's DONE, nothing in between cut, normal speed; sha256
`81186cfc56a0aacf7428a67771b31a9fb15db40d18c1834efe89cebcc9531989` (23,646,961 bytes).

Rebuild it: `tools/fetch_examples.sh` in the example fetches the video and the three sounds and cuts the 26 s clip and
the sound clips; build the app with the sounds in `Sounds/`, copy the clip into the app's container and launch the app
with `-watch 1 -source video -file Documents/flyover.mp4 -seconds 45 -delay 2 -trigger <file> -take 1 -frames 1 -log 1
-quit 0 -cells box -rules "water rushing over rows of stones=effect:ripple|a road bridge crossing over the
river=effect:spotlight/horn|a church with a tall spire=effect:zoom/bells"` (the example's README), push the trigger file
once READY and VIDEO are in the app's log, and record the mirrored screen with its audio.
