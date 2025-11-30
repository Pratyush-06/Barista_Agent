'use client';

import React from 'react';
import { motion } from 'motion/react';
import Link from 'next/link';

export default function WelcomeView({
  startButtonText = 'Start Voice Shopping',
  onStartCall,
  className = '',
}: {
  startButtonText?: string;
  onStartCall: () => void;
  className?: string;
}) {
  return (
    <div
      className={`flex flex-col items-center justify-center text-center px-6 py-12 w-full min-h-screen 
        bg-gradient-to-b from-[#0c0c0f] to-[#15151b] text-white ${className}`}
    >
      {/* Top Logo */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="mb-8"
      >
        <img
          src="/zepto-logo.svg"
          alt="Logo"
          className="h-12 opacity-90"
        />
      </motion.div>

      {/* Title */}
      <motion.h1
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.15 }}
        className="text-4xl md:text-5xl font-bold mb-4"
      >
        Voice Shopping Assistant
      </motion.h1>

      {/* Subtitle */}
      <motion.p
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.3 }}
        className="text-gray-300 text-lg max-w-xl mb-10"
      >
        Browse items, compare options, and place orders using your voice.  
        Powered by AI, built with Murf Falcon + LiveKit.
      </motion.p>

      {/* Main Start Button */}
      <motion.button
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.45, delay: 0.4 }}
        onClick={() => onStartCall()}
        className="px-8 py-3 rounded-xl text-lg font-semibold 
          bg-gradient-to-r from-[#FF2E63] to-[#FF6B81] 
          shadow-xl shadow-[#ff2e6355]
          hover:scale-105 transition-transform duration-200"
      >
        {startButtonText}
      </motion.button>

      {/* Optional: Transcript Page Link */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.9 }}
        className="mt-10"
      >
        <Link
          href="/transcripts"
          className="text-sm text-gray-400 hover:text-white underline"
        >
          View Previous Conversations →
        </Link>
      </motion.div>

      {/* Footer */}
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 0.5 }}
        transition={{ delay: 1.0 }}
        className="mt-12 text-xs text-gray-500"
      >
        A project for the Murf AI Voice Agents Challenge — #Day9
      </motion.p>
    </div>
  );
}
