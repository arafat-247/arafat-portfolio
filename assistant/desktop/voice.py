"""Bounded push-to-talk audio capture. Nothing is recorded before start()."""
from __future__ import annotations
import io
import threading
import wave

from core import check_cancel


class LocalTranscriber:
    """Use a multilingual CPU model. Audio never goes to a transcription API."""
    def __init__(self, directory):
        self.directory = directory
        self.model = None

    def transcribe(self, wav, languages, cancel, notify=lambda *args: None):
        check_cancel(cancel)
        if self.model is None:
            notify("Status", "Preparing local speech model · first use downloads several hundred MB from Hugging Face")
            try:
                import os
                os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
                os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
                from faster_whisper import WhisperModel
                self.model = WhisperModel("small", device="cpu", compute_type="int8",
                                          download_root=str(self.directory), cpu_threads=min(4, os.cpu_count() or 2))
            except Exception:
                raise RuntimeError("The local speech model could not be loaded or downloaded. Check internet access and free disk space; typed instructions still work.") from None
        check_cancel(cancel)
        notify("Status", "Transcribing on your computer · no recording is sent to OpenAI")
        language = languages[0] if len(languages) == 1 else None
        segments, _ = self.model.transcribe(io.BytesIO(wav), language=language, beam_size=3, vad_filter=True)
        parts = []
        for segment in segments:
            check_cancel(cancel)
            parts.append(segment.text)
        text = "".join(parts).strip()
        if not text:
            raise ValueError("No speech was recognised. Try again or type your instruction.")
        return text


class Recorder:
    def __init__(self, seconds=60, sample_rate=16_000):
        self.seconds, self.sample_rate = seconds, sample_rate
        self.stream = None
        self.blocks = []
        self.samples = 0
        self.problem = None
        self.lock = threading.Lock()

    def start(self):
        import sounddevice as sd
        self.blocks, self.samples, self.problem = [], 0, None

        def callback(data, frames, timing, status):
            if status:
                self.problem = str(status)
            with self.lock:
                remaining = self.seconds * self.sample_rate - self.samples
                if remaining <= 0:
                    raise sd.CallbackStop()
                count = min(frames, remaining)
                self.blocks.append(bytes(data)[:count * 2])
                self.samples += count
                if count < frames:
                    raise sd.CallbackStop()

        self.stream = sd.RawInputStream(samplerate=self.sample_rate, channels=1,
                                       dtype="int16", callback=callback)
        try:
            self.stream.start()
        except Exception:
            self.discard()
            raise

    def discard(self):
        stream, self.stream = self.stream, None
        if stream:
            try:
                stream.stop()
            finally:
                stream.close()
        with self.lock:
            self.blocks.clear()

    def finish(self) -> bytes:
        stream, self.stream = self.stream, None
        if stream:
            try:
                stream.stop()
            finally:
                stream.close()
        with self.lock:
            pcm = b"".join(self.blocks)
            self.blocks.clear()
        if self.problem:
            raise ValueError("Audio capture was interrupted. Check the microphone and record again.")
        if len(pcm) < self.sample_rate:  # At least half a second.
            raise ValueError("The recording was too short. Speak for at least half a second.")
        # RMS catches an unplugged/silent microphone before speech hallucination.
        import array
        samples = array.array("h", pcm)
        rms = (sum(int(x) ** 2 for x in samples) / max(1, len(samples))) ** 0.5
        if rms < 35:
            raise ValueError("The microphone captured silence. Check its volume or type your instruction.")
        output = io.BytesIO()
        with wave.open(output, "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(self.sample_rate)
            wav.writeframes(pcm)
        return output.getvalue()
