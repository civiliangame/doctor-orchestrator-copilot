"""G.711 μ-law 8 kHz <-> PCM16 transcoding (SPEC.md § Telnyx transport).

Telnyx media frames are ~20ms of base64 μ-law @ 8 kHz mono. Soniox wants
PCM16 @ 16 kHz; the TTS returns PCM16 at whatever rate we asked for.
Stateful ratecv converters avoid clicks at chunk boundaries.
"""

import audioop  # deprecated in 3.13 — requirements pin audioop-lts there


class UlawDecoder:
    """Inbound: μ-law 8 kHz -> PCM16 @ target_rate (stateful resampler)."""

    def __init__(self, target_rate: int = 16000) -> None:
        self.target_rate = target_rate
        self._state = None

    def decode(self, ulaw: bytes) -> bytes:
        pcm = audioop.ulaw2lin(ulaw, 2)
        if self.target_rate != 8000:
            pcm, self._state = audioop.ratecv(
                pcm, 2, 1, 8000, self.target_rate, self._state
            )
        return pcm


class UlawEncoder:
    """Outbound: PCM16 @ source_rate -> μ-law 8 kHz (stateful resampler)."""

    def __init__(self, source_rate: int) -> None:
        self.source_rate = source_rate
        self._state = None

    def encode(self, pcm: bytes) -> bytes:
        if self.source_rate != 8000:
            pcm, self._state = audioop.ratecv(
                pcm, 2, 1, self.source_rate, 8000, self._state
            )
        return audioop.lin2ulaw(pcm, 2)
