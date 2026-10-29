#!/usr/bin/env python3
"""Add ElevenLabs music (and optional voice-over) to rendered Reel visuals.

For every reels/<week>/<reel>/spec.json without a final.mp4 next to it:
  1. read visual.mp4 duration
  2. generate instrumental music with the ElevenLabs Music API
  3. optionally generate a voice-over with ElevenLabs Text to Speech
  4. mix with ffmpeg into final.mp4 (H.264 video copied, AAC audio)
A spec may also ask for a short voice sample (voice-sample.mp3) so a voice can be approved.

Needs the ELEVENLABS_API_KEY environment variable. Standard library only.
"""
import json
import math
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.elevenlabs.io/v1"
KEY = os.environ.get("ELEVENLABS_API_KEY", "").strip()
ROOT = Path(__file__).resolve().parent.parent
FALLBACK_VOICES = ["George", "Daniel", "Brian"]
_voice_cache = None


def call(method, path, body=None, query=None, accept="audio/mpeg"):
    url = API + path + ("?" + urllib.parse.urlencode(query) if query else "")
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("xi-api-key", KEY)
    req.add_header("Accept", accept)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        detail = e.read()[:600].decode("utf-8", "replace")
        raise SystemExit(f"ElevenLabs {method} {path} failed: HTTP {e.code} {detail}")


def voice_id(name):
    global _voice_cache
    if _voice_cache is None:
        raw = call("GET", "/voices", accept="application/json")
        _voice_cache = json.loads(raw).get("voices", [])
    wanted = [name] + [v for v in FALLBACK_VOICES if v != name]
    for w in wanted:
        for v in _voice_cache:
            if v.get("name", "").split(" ")[0].lower() == w.lower():
                print(f"  voice: {v['name']} ({v['voice_id']})")
                return v["voice_id"]
    if _voice_cache:
        v = _voice_cache[0]
        print(f"  voice '{name}' not found, using {v['name']}")
        return v["voice_id"]
    raise SystemExit("No ElevenLabs voices available on this account")


def tts(text, voice, out):
    audio = call(
        "POST", f"/text-to-speech/{voice_id(voice)}",
        body={"text": text, "model_id": "eleven_multilingual_v2",
              "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}},
        query={"output_format": "mp3_44100_128"},
    )
    out.write_bytes(audio)


def music(prompt, seconds, out):
    audio = call(
        "POST", "/music",
        body={"prompt": prompt, "music_length_ms": max(3000, int(math.ceil(seconds * 1000)) + 1500),
              "force_instrumental": True, "model_id": "music_v1"},
        query={"output_format": "mp3_44100_128"},
    )
    out.write_bytes(audio)


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=nw=1:nk=1", str(path)], capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def mix(folder, visual, dur, spec):
    music_vol = float(spec.get("music_volume", 0.9))
    fade_start = max(0.0, dur - 1.2)
    inputs = ["-i", str(visual), "-i", str(folder / "music.mp3")]
    if (folder / "voiceover.mp3").exists():
        inputs += ["-i", str(folder / "voiceover.mp3")]
        filt = (f"[1:a]atrim=0:{dur},volume={min(music_vol, 0.3)},afade=t=out:st={fade_start}:d=1.2[m];"
                f"[2:a]adelay={int(spec.get('voiceover_delay_ms', 300))}|{int(spec.get('voiceover_delay_ms', 300))},volume=1.0[v];"
                f"[m][v]amix=inputs=2:duration=first:normalize=0[a]")
    else:
        filt = f"[1:a]atrim=0:{dur},volume={music_vol},afade=t=in:st=0:d=0.4,afade=t=out:st={fade_start}:d=1.2[a]"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", filt,
           "-map", "0:v:0", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
           "-t", f"{dur:.3f}", "-movflags", "+faststart", str(folder / "final.mp4")]
    subprocess.run(cmd, check=True)


def main():
    if not KEY:
        raise SystemExit("ELEVENLABS_API_KEY is not set")
    specs = sorted(ROOT.glob("reels/*/*/spec.json"))
    built = 0
    for spec_path in specs:
        folder = spec_path.parent
        spec = json.loads(spec_path.read_text())
        visual = folder / spec.get("visual", "visual.mp4")
        if not visual.exists():
            print(f"skip {folder}: no {visual.name}")
            continue
        if (folder / "final.mp4").exists() and not spec.get("rebuild"):
            continue
        print(f"build {folder.relative_to(ROOT)}")
        dur = duration(visual)
        if spec.get("voice_sample"):
            vs = spec["voice_sample"]
            tts(vs["text"], vs.get("voice", "George"), folder / "voice-sample.mp3")
        music(spec["music"]["prompt"], dur, folder / "music.mp3")
        if spec.get("voiceover"):
            vo = spec["voiceover"]
            tts(vo["text"], vo.get("voice", "George"), folder / "voiceover.mp3")
        mix(folder, visual, dur, spec)
        print(f"  final.mp4 {duration(folder / 'final.mp4'):.1f}s")
        built += 1
    print(f"built {built} reel(s)")


if __name__ == "__main__":
    sys.exit(main())
