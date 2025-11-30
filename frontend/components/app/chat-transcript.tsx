'use client';

import * as React from 'react';
import { useTranscriptions } from '@livekit/components-react';
import type { AppConfig } from '@/app-config';

interface ChatTranscriptProps {
  className?: string;
  appConfig?: AppConfig;
}

/**
 * Minimal transcript panel that:
 * - Shows assistant & user messages from LiveKit transcriptions
 * - Styles them like a shopping assistant chat
 */
export function ChatTranscript(props: ChatTranscriptProps) {
  const { className, appConfig } = props;
  const segments = useTranscriptions();
  const brand = appConfig?.companyName ?? 'Zepto';

  return (
    <div
      className={
        'flex h-full w-full flex-col rounded-3xl border border-slate-800 bg-slate-950/80 text-slate-50 ' +
        (className ?? '')
      }
    >
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 px-4 py-3">
        <div className="flex flex-col">
          <span className="text-xs font-semibold uppercase tracking-[0.18em] text-emerald-300">
            {brand} · Voice Commerce
          </span>
          <span className="text-[11px] text-slate-400">
            Ask for products, prices, or your last order.
          </span>
        </div>
        <div className="flex items-center gap-2 text-[11px] text-slate-400">
          <span className="h-2 w-2 rounded-full bg-emerald-400" />
          Live
        </div>
      </div>

      {/* Transcript body */}
      <div className="flex-1 space-y-2 overflow-y-auto px-4 py-3 text-sm scrollbar-thin scrollbar-track-slate-950 scrollbar-thumb-slate-700/70">
        {segments.length === 0 && (
          <p className="mt-4 text-xs text-slate-500">
            Your conversation with the shopping assistant will appear here — try saying
            <span className="ml-1 rounded-md bg-slate-900 px-1.5 py-0.5 font-mono text-[11px] text-emerald-300">
              “Show me black hoodies under 1500”
            </span>
            .
          </p>
        )}

        {segments.map((seg, index) => {
          // Coerce to any so we don't fight strict typings of TextStreamData
          const s: any = seg;
          const id = s.id ?? String(index);
          const senderIdentity: string =
            s.senderIdentity ||
            s.participantIdentity ||
            (s.isLocal ? 'user' : 'agent');

          const isAgent =
            typeof senderIdentity === 'string' &&
            (senderIdentity.startsWith('agent') ||
              senderIdentity === 'assistant' ||
              senderIdentity.includes('voice_assistant'));

          const bubbleBase =
            'max-w-[80%] rounded-2xl px-3 py-2 text-[13px] leading-relaxed';

          return (
            <div
              key={id}
              className={
                'flex w-full ' +
                (isAgent ? 'justify-start' : 'justify-end')
              }
            >
              <div className="flex max-w-full flex-col gap-0.5">
                <span className="text-[10px] uppercase tracking-[0.18em] text-slate-500">
                  {isAgent ? `${brand} · Assistant` : 'You'}
                </span>
                <div
                  className={
                    bubbleBase +
                    ' ' +
                    (isAgent
                      ? 'bg-slate-900 text-slate-50 border border-slate-800'
                      : 'bg-emerald-500 text-slate-950')
                  }
                >
                  {s.text}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Footer helper */}
      <div className="border-t border-slate-800 px-4 py-2 text-[11px] text-slate-500">
        Hint: you can ask things like{' '}
        <span className="font-mono text-emerald-300">
          “What did I just buy?”
        </span>{' '}
        or{' '}
        <span className="font-mono text-emerald-300">
          “Do you have any t-shirts under 1000?”
        </span>
        .
      </div>
    </div>
  );
}
