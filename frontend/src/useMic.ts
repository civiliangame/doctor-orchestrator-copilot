// Mic capture -> /ws/audio?session_id= (upload-only, API_CONTRACT.md § WebSocket 1).
// All transcript display comes from the events socket — this hook only pushes audio.

import { useCallback, useRef, useState } from "react";

export type MicStatus = "idle" | "connecting" | "live" | "stopped" | "error";

export function useMic(sessionId: number | null) {
  const [status, setStatus] = useState<MicStatus>("idle");
  const [error, setError] = useState<string | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const recorderRef = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);

  const cleanup = useCallback(() => {
    if (recorderRef.current && recorderRef.current.state !== "inactive") {
      recorderRef.current.stop();
    }
    recorderRef.current = null;
    streamRef.current?.getTracks().forEach((t) => t.stop());
    streamRef.current = null;
  }, []);

  const start = useCallback(async () => {
    if (sessionId === null) return;
    setError(null);
    setStatus("connecting");

    let stream: MediaStream;
    try {
      stream = await navigator.mediaDevices.getUserMedia({
        audio: { channelCount: 1, echoCancellation: true, noiseSuppression: true },
      });
    } catch {
      setError("Microphone access denied. Allow mic access and try again.");
      setStatus("error");
      return;
    }
    streamRef.current = stream;

    const ws = new WebSocket(`ws://${location.hostname}:8000/ws/audio?session_id=${sessionId}`);
    wsRef.current = ws;

    ws.onopen = () => {
      const mimeType = MediaRecorder.isTypeSupported("audio/webm;codecs=opus")
        ? "audio/webm;codecs=opus"
        : undefined; // Safari picks; backend audio_format=auto copes
      const recorder = new MediaRecorder(stream, mimeType ? { mimeType } : undefined);
      recorderRef.current = recorder;
      recorder.ondataavailable = (e) => {
        if (e.data.size > 0 && ws.readyState === WebSocket.OPEN) ws.send(e.data);
      };
      recorder.start(250);
      setStatus("live");
    };

    ws.onmessage = (event) => {
      // Only fatal errors ever come down this socket.
      try {
        const msg = JSON.parse(event.data);
        if (msg?.error) {
          setError(msg.error.message ?? "audio pipeline error");
          setStatus("error");
          cleanup();
        }
      } catch {
        /* ignore */
      }
    };

    ws.onerror = () => {
      setError("Could not reach the audio socket. Is the backend running?");
      setStatus("error");
      cleanup();
    };

    ws.onclose = () => {
      setStatus((s) => (s === "live" || s === "connecting" ? "stopped" : s));
      cleanup();
    };
  }, [sessionId, cleanup]);

  const stop = useCallback(() => {
    cleanup();
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send("stop"); // backend flushes Soniox finals, then closes
    }
    setStatus("stopped");
  }, [cleanup]);

  return { status, error, start, stop };
}
