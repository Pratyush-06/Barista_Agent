import React from 'react';
import { Button } from '@/components/livekit/button';
import { cn } from '@/lib/utils';

function WelcomeImage() {
  return (
    <div className="w-20 h-20 rounded-full bg-gradient-to-br from-[#00c853] to-[#00e676] flex items-center justify-center text-black font-extrabold text-2xl shadow-2xl">
      PW
    </div>
  );
}

interface WelcomeViewProps {
  startButtonText: string;
  onStartCall: (mode?: 'learning' | 'quiz' | 'teach-back') => void;
}

export const WelcomeView = ({ startButtonText, onStartCall, ref }: React.ComponentProps<'div'> & WelcomeViewProps) => {
  const [mode, setMode] = React.useState<'learning' | 'quiz' | 'teach-back'>('learning');

  function handleStart() {
    onStartCall(mode);
  }

  return (
    <div ref={ref} className="w-full">
      <section className="min-h-[60vh] flex flex-col items-center justify-center text-center px-6">
        <div className="mb-6">
          <WelcomeImage />
        </div>

        <h1 className={cn('text-3xl md:text-4xl font-extrabold tracking-tight')}>Physics Wallah — Voice Tutor</h1>

        <p className="text-sm text-white/80 max-w-xl mt-3">
          Practice concepts aloud, take spoken quizzes, or explain ideas back to the assistant. The voice tutor
          listens and gives friendly, actionable feedback.
        </p>

        <div className="mt-6 flex flex-col items-center gap-4">
          <div className="flex gap-3">
            <button
              className={cn('px-3 py-2 rounded-full text-sm font-medium', mode === 'learning' ? 'bg-[#ffd600] text-black' : 'bg-white/5')}
              onClick={() => setMode('learning')}
            >
              Learning
            </button>
            <button
              className={cn('px-3 py-2 rounded-full text-sm font-medium', mode === 'quiz' ? 'bg-[#00e676] text-black' : 'bg-white/5')}
              onClick={() => setMode('quiz')}
            >
              Quiz
            </button>
            <button
              className={cn('px-3 py-2 rounded-full text-sm font-medium', mode === 'teach-back' ? 'bg-[#81d4fa] text-black' : 'bg-white/5')}
              onClick={() => setMode('teach-back')}
            >
              Teach-Back
            </button>
          </div>

          <div className="mt-4 flex items-center gap-4">
            <Button variant="primary" size="lg" onClick={handleStart} className="font-mono">
              {startButtonText}
            </Button>

            <a
              className="ml-2 inline-block text-sm text-white/70 underline"
              href="https://physicstutor.example.com"
              target="_blank"
              rel="noreferrer"
            >
              Learn more
            </a>
          </div>
        </div>
      </section>

      <div className="fixed bottom-5 left-0 flex w-full items-center justify-center">
        <p className="text-muted-foreground max-w-prose pt-1 text-xs leading-5 font-normal md:text-sm">
          Need help getting set up? Check out the{' '}
          <a
            target="_blank"
            rel="noopener noreferrer"
            href="https://docs.livekit.io/agents/start/voice-ai/"
            className="underline"
          >
            Voice AI quickstart
          </a>
          .
        </p>
      </div>
    </div>
  );
};
