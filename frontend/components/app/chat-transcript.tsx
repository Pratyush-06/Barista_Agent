'use client';

import React, { useEffect, useState } from 'react';
import { AnimatePresence, motion } from 'motion/react';
import type { ReceivedChatMessage } from '@livekit/components-react';

const MotionContainer = motion.create('div');

export type ChatTranscriptProps = {
  messages: ReceivedChatMessage[];
  className?: string;
};

/** Safely extract plain text from the message */
function extractText(msg: ReceivedChatMessage): string {
  const m: any = msg as any;

  if (typeof m.text === 'string') return m.text;
  if (typeof m.message === 'string') return m.message;
  if (m.message && typeof m.message.text === 'string') return m.message.text;
  if (m.payload && typeof m.payload === 'string') return m.payload;

  return '';
}

/** Decide if this text should trigger a Solo Leveling System Window */
function isSystemWindow(text: string): boolean {
  const lower = text.toLowerCase();
  return (
    text.startsWith('Status Window') ||
    text.startsWith('System Check') ||
    lower.includes('status window —') ||
    lower.includes('hp:') ||
    lower.includes('system message')
  );
}

export function ChatTranscript({ messages, className }: ChatTranscriptProps) {
  const [popupText, setPopupText] = useState<string | null>(null);
  const [popupKey, setPopupKey] = useState(0);

  // Whenever a new assistant message looks like a System Window, show popup
  useEffect(() => {
    if (!messages.length) return;
    const last = messages[messages.length - 1];
    const isUser = last.from?.identity === 'user';
    if (isUser) return;

    const text = extractText(last);
    if (text && isSystemWindow(text)) {
      setPopupText(text);
      setPopupKey((prev) => prev + 1);
    }
  }, [messages]);

  // Auto-hide the popup after 4 seconds
  useEffect(() => {
    if (!popupText) return;
    const t = setTimeout(() => setPopupText(null), 4000);
    return () => clearTimeout(t);
  }, [popupText]);

  return (
    <div
      className={`w-full h-full flex flex-col gap-3 overflow-y-auto px-4 py-4 ${className ?? ''}`}
      style={{
        background:
          'radial-gradient(circle at top, #111827 0, #020617 45%, #000000 100%)',
      }}
    >
      {/* Main chat bubbles */}
      <AnimatePresence initial={false}>
        {messages.map((msg, idx) => {
          const isUser = msg.from?.identity === 'user';
          const key = `${msg.id}-${idx}`;
          const text = extractText(msg);

          return (
            <MotionContainer
              key={key}
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.22 }}
            >
              <div
                className={`rounded-2xl px-4 py-3 mb-2 border shadow-lg max-w-[80%] ${
                  isUser
                    ? 'ml-0 mr-auto border-emerald-400/60 bg-slate-900/80 text-emerald-100'
                    : 'ml-auto mr-0 border-cyan-400/70 bg-slate-950/90 text-cyan-50 shadow-cyan-500/40'
                }`}
                style={{ backdropFilter: 'blur(6px)' }}
              >
                <div
                  className={`text-[10px] uppercase tracking-[0.16em] mb-1 ${
                    isUser ? 'text-emerald-300' : 'text-cyan-300'
                  }`}
                >
                  {isUser ? 'Hunter' : 'System'}
                </div>

                <div className="text-sm leading-relaxed whitespace-pre-line">
                  {text}
                </div>

                <div
                  className="mt-3 h-[2px] w-full"
                  style={{
                    background: isUser
                      ? 'linear-gradient(to right, #34d399, transparent)'
                      : 'linear-gradient(to right, #22d3ee, transparent)',
                  }}
                />
              </div>
            </MotionContainer>
          );
        })}
      </AnimatePresence>

      {/* Solo Leveling floating System Window – SINGLE popup, auto-hides */}
      <AnimatePresence>
        {popupText && (
          <motion.div
            key={popupKey}
            initial={{ opacity: 0, y: -8, x: 8 }}
            animate={{ opacity: 1, y: 0, x: 0 }}
            exit={{ opacity: 0, y: -8, x: 8 }}
            transition={{ duration: 0.2 }}
            className="fixed top-4 right-4 z-50 max-w-sm animate-fade-in"
          >
            <div className="px-4 py-3 rounded-xl border border-cyan-300 bg-cyan-900/80 shadow-lg shadow-cyan-500/40 backdrop-blur-md">
              <div className="text-[10px] uppercase tracking-[0.18em] text-cyan-200 mb-1">
                System Window
              </div>
              <div className="text-sm text-cyan-50 whitespace-pre-line">
                {popupText}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default ChatTranscript;
