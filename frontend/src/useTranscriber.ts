import { useCallback, useRef, useState } from "react";

export type Turn = {
  speaker: string;
  text: string;
  endpointed: boolean; // Soniox emitted <end> after this turn
};

export type TranscriberStatus =
  | "idle"
  | "connecting"
  | "live"
  | "finishing"
  | "stopped"
  | "error";

type SonioxToken = {
  text: string;
  is_final: boolean;
  speaker?: string;
};

type SonioxMessage = {
  tokens?: SonioxToken[];
  finished?: boolean;
  error_code?: number;
  error_message?: string;
};

const WS_URL = `ws://${location.hostname}:8000/ws/transcribe`;

/** Group an ordered list of final tokens into consecutive same-speaker turns.
 * The <end> token (endpoint detection) closes the current turn. */
function buildTurns(tokens: SonioxToken[]): Turn[] {
  const turns: Turn[] = [];
  for (const tok of tokens) {
    if (tok.text === "<end>") {
      if (turns.length > 0) turns[turns.length - 1].endpointed = true;
      continue;
    }
    const speaker = tok.speaker ?? "?";
    const last = turns[turns.length - 1];
    if (last && last.speaker === speaker && !last.endpointed) {
      last.text += tok.text;
    } else {
      turns.push({ speaker, text: tok.text, endpointed: false });
    }
  }
  return turns;
}

export function useTranscriber() {
  const [status, setStatus] = useState<TranscriberStatus>("idle");
  const [error, setError] = useState<string | null>(null);
  const [turns, setTurns] = useState<Turn[]>([]);
  const [interim, setInterim] = useState<string>("");

  const wsRef = useRef<WebSocket | null>(null);
  const recorderRef = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const finalTokensRef = useRef<SonioxToken[]>([]);

  const cleanupMedia = useCallback(() => {
    if (recorderRef.current && recorderRef.current.state !== "inactive") {
      recorderRef.current.stop();
    }
    recorderRef.current = null;
    streamRef.current?.getTracks().forEach((t) => t.stop());
    streamRef.current = null;
  }, []);

  const start = useCallback(async () => {
    setError(null);
    setTurns([]);
    setInterim("");
    finalTokensRef.current = [];
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

    const ws = new WebSocket(WS_URL);
    wsRef.current = ws;

    ws.onopen = () => {
      const mimeType = MediaRecorder.isTypeSupported("audio/webm;codecs=opus")
        ? "audio/webm;codecs=opus"
        : undefined; // Safari: let the browser pick; Soniox audio_format=auto copes
      const recorder = new MediaRecorder(stream, mimeType ? { mimeType } : undefined);
      recorderRef.current = recorder;
      recorder.ondataavailable = (e) => {
        if (e.data.size > 0 && ws.readyState === WebSocket.OPEN) ws.send(e.data);
      };
      recorder.start(250); // 250ms chunks
      setStatus("live");
    };

    ws.onmessage = (event) => {
      let msg: SonioxMessage;
      try {
        msg = JSON.parse(event.data);
      } catch {
        return;
      }
      if (msg.error_code) {
        setError(`${msg.error_message ?? "Transcription error"} (code ${msg.error_code})`);
        setStatus("error");
        cleanupMedia();
        return;
      }
      if (msg.tokens && msg.tokens.length > 0) {
        const finals = msg.tokens.filter((t) => t.is_final);
        if (finals.length > 0) {
          finalTokensRef.current = [...finalTokensRef.current, ...finals];
          setTurns(buildTurns(finalTokensRef.current));
        }
        setInterim(
          msg.tokens
            .filter((t) => !t.is_final && t.text !== "<end>")
            .map((t) => t.text)
            .join(""),
        );
      }
      if (msg.finished) {
        setInterim("");
        setStatus("stopped");
        ws.close();
      }
    };

    ws.onerror = () => {
      setError("Could not reach the backend at " + WS_URL + ". Is uvicorn running?");
      setStatus("error");
      cleanupMedia();
    };

    ws.onclose = () => {
      setStatus((s) => (s === "live" || s === "connecting" || s === "finishing" ? "stopped" : s));
      cleanupMedia();
    };
  }, [cleanupMedia]);

  const stop = useCallback(() => {
    setStatus("finishing");
    cleanupMedia();
    // Tell the backend audio is done; keep the socket open so Soniox can
    // flush remaining final tokens, then the server sends finished:true.
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send("stop");
    }
  }, [cleanupMedia]);

  return { status, error, turns, interim, start, stop };
}
