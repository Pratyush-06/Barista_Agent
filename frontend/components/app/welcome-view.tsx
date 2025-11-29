'use client';

import React from 'react';
import { motion } from 'motion/react';

type WelcomeViewProps = {
  startButtonText?: string;
  onStartCall?: () => void;
  className?: string;
};

const MotionButton = motion.button;

function WelcomeViewInner({
  startButtonText = 'Enter the Gate',
  onStartCall,
  className,
}: WelcomeViewProps) {
  const handleEnterGate = () => {
    if (onStartCall) {
      onStartCall(); // this calls startSession from useSession()
    } else {
      console.warn('WelcomeView.onStartCall is not defined');
    }
  };

  return (
    <div
      className={`min-h-screen flex items-center justify-center px-4 text-solo-text ${className ?? ''}`}
      style={{
        background:
          'radial-gradient(circle at top, #1f2937 0, #020617 45%, #000000 100%)',
      }}
    >
      <div className="max-w-3xl w-full text-center">
        {/* Title */}
        <motion.h1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: 'easeOut' }}
          className="text-4xl md:text-5xl font-extrabold tracking-tight text-solo-title drop-shadow-lg"
        >
          Solo Leveling – Dungeon Run
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.15, ease: 'easeOut' }}
          className="mt-4 text-base md:text-lg text-solo-subtitle max-w-2xl mx-auto"
        >
          Enter the Gate as a low-rank Hunter. The System will narrate your fate,
          track your HP & inventory, and roll the dice on every risky choice.
        </motion.p>

        {/* System panel */}
        <motion.div
          initial={{ opacity: 0, scale: 0.96 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.25, ease: 'easeOut' }}
          className="mt-8 mx-auto max-w-xl rounded-2xl border border-solo-panel/40 bg-solo-panel/60 backdrop-blur-md shadow-2xl shadow-solo-accent/20 p-5 text-left"
        >
          <div className="text-xs font-mono text-solo-accent mb-1">
            ▸ SYSTEM NOTICE
          </div>
          <p className="text-sm text-solo-text/90 leading-relaxed">
            This is a voice-controlled dungeon. Speak your actions like:
            <br />
            <span className="text-solo-accent/90">
              “Inspect the surroundings”, “Open the status window”, “Attack the
              goblin”, “Drink a potion”…
            </span>
            <br />
            The System will roll the dice, resolve outcomes, and update your HP
            and inventory in real time.
          </p>
        </motion.div>

        {/* Enter button */}
        <MotionButton
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45, delay: 0.4, ease: 'easeOut' }}
          onClick={handleEnterGate}
          className="mt-10 inline-flex items-center justify-center rounded-full px-10 py-3.5 text-sm md:text-base font-semibold
                     bg-solo-btn from-solo-btn to-solo-btn/80 bg-gradient-to-r text-white shadow-lg shadow-solo-accent/40
                     hover:shadow-solo-accent/60 hover:-translate-y-0.5 active:translate-y-0 transition-all duration-200
                     border border-solo-btn-border"
        >
          {startButtonText}
        </MotionButton>

        {/* Footer text */}
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.6 }}
          className="mt-6 text-xs md:text-sm text-solo-subtitle/80"
        >
          A Day 8 project for the Murf AI Voice Agent Challenge · Powered by Murf
          Falcon (Hugo · Narration) &amp; LiveKit Agents
        </motion.p>
      </div>
    </div>
  );
}

// default + named export so ViewController can use { WelcomeView }
export default function WelcomeView(props: WelcomeViewProps) {
  return <WelcomeViewInner {...props} />;
}

export { WelcomeView };
