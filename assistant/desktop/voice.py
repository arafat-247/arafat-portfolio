"""Bounded push-to-talk audio capture. Nothing is recorded before start()."""
from __future__ import annotations
import io
import threading
import wave


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
