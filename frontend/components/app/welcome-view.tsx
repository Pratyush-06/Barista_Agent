'use client';

import React, { useState, useEffect } from 'react';
import { motion } from 'motion/react';
import { Phone, MessageCircle, CheckCircle2, Zap, BarChart3, Clock } from 'lucide-react';
import { Button } from '@/components/livekit/button';
import { cn } from '@/lib/utils';

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.8, ease: 'easeOut' },
  },
};

const floatingVariants = {
  animate: {
    y: [0, -10, 0],
    transition: {
      duration: 3,
      repeat: Infinity,
      ease: 'easeInOut',
    },
  },
};

function AnimatedParticles() {
  const [particles, setParticles] = useState<Array<{ id: number; left: number; top: number; duration: number }>>([]);

  useEffect(() => {
    const particleArray = [...Array(6)].map((_, i) => ({
      id: i,
      left: Math.random() * 100,
      top: Math.random() * 100,
      duration: 8 + i,
    }));
    setParticles(particleArray);
  }, []);

  if (particles.length === 0) return null;

  return (
    <div className="absolute inset-0 overflow-hidden">
      {particles.map((particle) => (
        <motion.div
          key={particle.id}
          className="absolute w-1 h-1 bg-red-400 rounded-full opacity-20"
          animate={{
            x: Math.random() * 400 - 200,
            y: Math.random() * 400 - 200,
            opacity: [0.2, 0.5, 0.2],
          }}
          transition={{
            duration: particle.duration,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
          style={{
            left: `${particle.left}%`,
            top: `${particle.top}%`,
          }}
        />
      ))}
    </div>
  );
}

function HowItWorksCard({
  icon: Icon,
  step,
  title,
  description,
}: {
  icon: React.ComponentType<{ className?: string }>;
  step: number;
  title: string;
  description: string;
}) {
  return (
    <motion.div
      variants={itemVariants}
      className="group relative bg-gradient-to-br from-gray-900 to-black rounded-2xl p-8 border border-gray-800 hover:border-red-500/50 transition-all duration-300 overflow-hidden"
    >
      <div className="absolute inset-0 bg-gradient-to-br from-red-500/0 to-red-500/0 group-hover:from-red-500/5 group-hover:to-red-500/10 transition-all duration-300" />
      <div className="relative z-10">
        <div className="flex items-center gap-4 mb-4">
          <div className="w-12 h-12 rounded-full bg-gradient-to-br from-red-500 to-red-600 flex items-center justify-center">
            <Icon className="w-6 h-6 text-white" />
          </div>
          <span className="text-sm font-bold text-red-500">Step {step}</span>
        </div>
        <h3 className="text-lg font-bold text-white mb-2">{title}</h3>
        <p className="text-gray-400 text-sm leading-relaxed">{description}</p>
      </div>
    </motion.div>
  );
}

function FeatureCard({
  icon: Icon,
  title,
  description,
}: {
  icon: React.ComponentType<{ className?: string }>;
  title: string;
  description: string;
}) {
  return (
    <motion.div
      variants={itemVariants}
      className="group relative bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 border border-gray-800 hover:border-red-500/50 transition-all duration-300"
    >
      <div className="absolute inset-0 bg-gradient-to-br from-red-500/0 to-red-500/0 group-hover:from-red-500/5 group-hover:to-red-500/10 transition-all duration-300" />
      <div className="relative z-10 flex flex-col items-center text-center">
        <div className="w-14 h-14 rounded-full bg-gradient-to-br from-red-500 to-red-600 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
          <Icon className="w-7 h-7 text-white" />
        </div>
        <h3 className="text-base font-bold text-white mb-2">{title}</h3>
        <p className="text-gray-400 text-sm leading-relaxed">{description}</p>
      </div>
    </motion.div>
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
    <div ref={ref} className="w-full min-h-screen bg-black text-white overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-b from-gray-950 via-black to-black" />
      <AnimatedParticles />

      <div className="relative z-10">
        {/* Hero Section */}
        <div className="min-h-screen flex flex-col items-center justify-center px-4 md:px-6 pt-12 pb-20">
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="mb-6 inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-gray-900 border border-gray-800"
          >
            <Zap className="w-3.5 h-3.5 text-red-500" />
            <span className="text-xs font-medium text-gray-300">Built with LiveKit Agents</span>
          </motion.div>

          <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="flex flex-col items-center gap-8 max-w-4xl"
          >
            <motion.div
              variants={floatingVariants}
              animate="animate"
              className="w-24 h-24 rounded-full bg-gradient-to-br from-red-500 to-red-600 flex items-center justify-center shadow-2xl"
            >
              <img src="/zomato-logo.svg" alt="Zomato" className="w-16 h-16" />
            </motion.div>

            <motion.div variants={itemVariants} className="text-center">
              <h1 className="text-5xl md:text-6xl font-black tracking-tight mb-4 bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
                Zomato — Voice SDR
              </h1>
              <p className="text-lg md:text-xl text-gray-400 max-w-2xl mx-auto leading-relaxed">
                Connect with restaurant partners through intelligent voice conversations. Qualify leads, answer questions, and close deals faster with AI-powered sales automation.
              </p>
            </motion.div>

            <motion.div variants={itemVariants} className="flex flex-col items-center gap-6 w-full">
              <div className="flex flex-wrap gap-3 justify-center">
                {[
                  { id: 'learning', label: 'Qualify', color: 'from-red-500 to-red-600' },
                  { id: 'quiz', label: 'Demo', color: 'from-orange-500 to-red-500' },
                  { id: 'teach-back', label: 'Close', color: 'from-green-500 to-emerald-600' },
                ].map((m) => (
                  <motion.button
                    key={m.id}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => setMode(m.id as 'learning' | 'quiz' | 'teach-back')}
                    className={`px-6 py-2 rounded-full font-semibold text-sm transition-all duration-300 ${
                      mode === m.id
                        ? `bg-gradient-to-r ${m.color} text-white shadow-lg`
                        : 'bg-gray-900 text-gray-400 border border-gray-800 hover:border-gray-700'
                    }`}
                  >
                    {m.label}
                  </motion.button>
                ))}
              </div>

              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={handleStart}
                className="mt-4 px-8 py-4 rounded-full bg-gradient-to-r from-red-500 to-red-600 text-white font-bold text-lg hover:shadow-xl hover:shadow-red-500/30 transition-all duration-300 flex items-center gap-2"
              >
                <Phone className="w-5 h-5" />
                {startButtonText}
              </motion.button>

              <motion.a
                whileHover={{ scale: 1.05 }}
                href="https://www.zomato.com/business"
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-red-400 hover:text-red-300 underline"
              >
                Zomato Business →
              </motion.a>
            </motion.div>
          </motion.div>
        </div>

        {/* How It Works Section */}
        <section className="relative py-24 px-4 md:px-6 bg-gradient-to-b from-black via-gray-950 to-black">
          <div className="max-w-6xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8 }}
              className="text-center mb-16"
            >
              <h2 className="text-4xl md:text-5xl font-black mb-4">How It Works</h2>
              <p className="text-gray-400 text-lg">Three simple steps to qualify restaurant partners</p>
            </motion.div>

            <motion.div
              variants={containerVariants}
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true }}
              className="grid md:grid-cols-3 gap-8"
            >
              <HowItWorksCard
                icon={MessageCircle}
                step={1}
                title="Partner Connects"
                description="Restaurant partner initiates a voice call through Zomato's SDR platform."
              />
              <HowItWorksCard
                icon={Zap}
                step={2}
                title="AI Qualifies"
                description="AI answers questions, matches against Zomato partner FAQs, and qualifies the prospect in real-time."
              />
              <HowItWorksCard
                icon={CheckCircle2}
                step={3}
                title="Leads Captured"
                description="Automatically captures prospect info, summarizes conversation, and saves qualified lead to JSON."
              />
            </motion.div>
          </div>
        </section>

        {/* Features Section */}
        <section className="relative py-24 px-4 md:px-6">
          <div className="max-w-6xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8 }}
              className="text-center mb-16"
            >
              <h2 className="text-4xl md:text-5xl font-black mb-4">Powerful Features</h2>
              <p className="text-gray-400 text-lg">Everything you need for voice-first sales</p>
            </motion.div>

            <motion.div
              variants={containerVariants}
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true }}
              className="grid md:grid-cols-3 gap-6"
            >
              <FeatureCard
                icon={Phone}
                title="Voice-First Qualification"
                description="Natural conversations that guide prospects through your sales funnel."
              />
              <FeatureCard
                icon={BarChart3}
                title="Auto-Lead Capture"
                description="Automatically extract and structure prospect information from conversations."
              />
              <FeatureCard
                icon={MessageCircle}
                title="Smart FAQ Matching"
                description="AI instantly matches questions to your Zomato partner FAQs for consistent answers."
              />
              <FeatureCard
                icon={Zap}
                title="Personalized Responses"
                description="Generate contextual replies tailored to each prospect's specific needs."
              />
              <FeatureCard
                icon={Clock}
                title="Real-Time Summaries"
                description="Get instant conversation summaries and lead scoring for your sales team."
              />
              <FeatureCard
                icon={CheckCircle2}
                title="Multi-Mode Selling"
                description="Switch between Qualify, Demo, and Close modes based on the conversation stage."
              />
            </motion.div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="relative py-20 px-4 md:px-6 border-t border-gray-800">
          <div className="max-w-2xl mx-auto text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8 }}
            >
              <h2 className="text-3xl md:text-4xl font-black mb-6">Ready to grow your restaurant partnerships?</h2>
              <motion.a
                whileHover={{ scale: 1.05 }}
                href="https://www.zomato.com/business"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block px-8 py-4 rounded-full bg-gradient-to-r from-red-500 to-red-600 text-white font-bold hover:shadow-xl hover:shadow-red-500/30 transition-all duration-300"
              >
                Explore Zomato Business
              </motion.a>
            </motion.div>
          </div>
        </section>

        {/* Footer */}
        <footer className="relative border-t border-gray-800 py-12 px-4 md:px-6">
          <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6 text-center md:text-left">
            <div className="text-gray-500 text-sm">
              © 2025 Zomato — Voice SDR. All rights reserved.
            </div>
            <div className="text-gray-500 text-sm">
              Powered by <span className="text-red-400">LiveKit Agents</span> + <span className="text-red-400">Murf Falcon TTS</span>
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
};
