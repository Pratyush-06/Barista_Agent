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
    const particleArray = [...Array(12)].map((_, i) => ({
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
          className={`absolute w-1.5 h-1.5 rounded-full opacity-30 ${
            particle.id % 2 === 0 ? 'bg-yellow-300' : 'bg-blue-400'
          }`}
          animate={{
            x: Math.random() * 600 - 300,
            y: Math.random() * 600 - 300,
            opacity: [0.2, 0.6, 0.2],
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
      className="group relative bg-gradient-to-br from-blue-900/40 to-blue-950/60 rounded-2xl p-8 border border-blue-500/30 hover:border-yellow-400/60 transition-all duration-300 overflow-hidden"
    >
      <div className="absolute inset-0 bg-gradient-to-br from-yellow-400/0 to-yellow-400/0 group-hover:from-yellow-400/5 group-hover:to-yellow-400/10 transition-all duration-300" />
      <div className="relative z-10">
        <div className="flex items-center gap-4 mb-4">
          <div className="w-12 h-12 rounded-full bg-gradient-to-br from-yellow-300 to-yellow-400 flex items-center justify-center shadow-lg shadow-yellow-400/20">
            <Icon className="w-6 h-6 text-blue-950" />
          </div>
          <span className="text-sm font-bold text-yellow-300">Step {step}</span>
        </div>
        <h3 className="text-lg font-bold text-white mb-2">{title}</h3>
        <p className="text-blue-100/70 text-sm leading-relaxed">{description}</p>
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
      className="group relative bg-gradient-to-br from-blue-900/30 to-blue-950/50 rounded-2xl p-6 border border-blue-500/30 hover:border-yellow-400/60 transition-all duration-300"
    >
      <div className="absolute inset-0 bg-gradient-to-br from-yellow-400/0 to-yellow-400/0 group-hover:from-yellow-400/5 group-hover:to-yellow-400/10 transition-all duration-300 rounded-2xl" />
      <div className="relative z-10 flex flex-col items-center text-center">
        <div className="w-14 h-14 rounded-full bg-gradient-to-br from-yellow-300 to-yellow-400 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300 shadow-lg shadow-yellow-400/20">
          <Icon className="w-7 h-7 text-blue-950" />
        </div>
        <h3 className="text-base font-bold text-white mb-2">{title}</h3>
        <p className="text-blue-100/70 text-sm leading-relaxed">{description}</p>
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
    <div ref={ref} className="w-full min-h-screen text-white overflow-y-auto">
      <div className="fixed inset-0 bg-gradient-to-br from-blue-950 via-blue-900 to-slate-900 -z-20" />
      <AnimatedParticles />

      <div className="relative z-10">
        {/* Navigation Header */}
        <nav className="fixed top-0 left-0 right-0 z-40 bg-gradient-to-b from-blue-950/95 to-blue-950/50 backdrop-blur-md border-b border-blue-500/20">
          <div className="max-w-7xl mx-auto px-4 md:px-6 py-4 flex items-center justify-between">
            <a href="https://slice.bank.in/" target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
              <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-yellow-300 to-yellow-400 flex items-center justify-center shadow-lg">
                <span className="text-lg font-black text-blue-950">S</span>
              </div>
              <span className="font-black text-lg bg-gradient-to-r from-yellow-300 to-yellow-200 bg-clip-text text-transparent">SLICE</span>
            </a>
            <div className="flex items-center gap-4">
              <a href="https://slice.bank.in/" target="_blank" rel="noopener noreferrer" className="text-sm text-blue-100 hover:text-yellow-300 transition-colors">
                About
              </a>
              <a href="https://slice.bank.in/" target="_blank" rel="noopener noreferrer" className="text-sm px-4 py-2 rounded-full bg-gradient-to-r from-yellow-300 to-yellow-400 text-blue-950 font-bold hover:shadow-lg hover:shadow-yellow-400/50 transition-all">
                Visit Slice Bank
              </a>
            </div>
          </div>
        </nav>

        {/* Hero Section */}
        <div className="min-h-screen flex flex-col items-center justify-center px-4 md:px-6 pt-32 pb-20">
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="mb-6 inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-900/50 border border-blue-500/50 backdrop-blur-sm"
          >
            <Zap className="w-4 h-4 text-yellow-300" />
            <span className="text-xs font-medium text-yellow-200">Slice Bank Fraud Detection</span>
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
              className="w-28 h-28 rounded-2xl bg-gradient-to-br from-yellow-300 to-yellow-400 flex items-center justify-center shadow-2xl shadow-yellow-400/40"
            >
              <span className="text-5xl font-black text-blue-950">S</span>
            </motion.div>

            <motion.div variants={itemVariants} className="text-center">
              <h1 className="text-6xl md:text-7xl font-black tracking-tighter mb-4">
                <span className="bg-gradient-to-r from-yellow-200 via-yellow-300 to-yellow-200 bg-clip-text text-transparent">
                  SLICE THE WAY
                </span>
              </h1>
              <h1 className="text-6xl md:text-7xl font-black tracking-tighter mb-6">
                <span className="bg-gradient-to-r from-white via-blue-100 to-white bg-clip-text text-transparent">
                  YOU BANK
                </span>
              </h1>
              <p className="text-xl md:text-2xl font-bold text-yellow-300 mb-2">THE FINE-PRINT ENDS TODAY</p>
              <p className="text-lg md:text-xl text-blue-100/80 max-w-2xl mx-auto leading-relaxed">
                Take control of your money and time. Voice-powered fraud detection that keeps your account secure 24/7 with intelligent real-time verification.
              </p>
            </motion.div>

            <motion.div variants={itemVariants} className="flex flex-col items-center gap-6 w-full">
              <div className="flex flex-wrap gap-3 justify-center">
                {[
                  { id: 'learning', label: 'Verify', color: 'from-yellow-300 to-yellow-400' },
                  { id: 'quiz', label: 'Detect', color: 'from-blue-400 to-blue-500' },
                  { id: 'teach-back', label: 'Secure', color: 'from-emerald-400 to-emerald-500' },
                ].map((m) => (
                  <motion.button
                    key={m.id}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => setMode(m.id as 'learning' | 'quiz' | 'teach-back')}
                    className={`px-6 py-3 rounded-full font-bold text-sm transition-all duration-300 ${
                      mode === m.id
                        ? `bg-gradient-to-r ${m.color} text-blue-950 shadow-lg shadow-yellow-400/40`
                        : 'bg-blue-900/40 text-blue-100 border border-blue-500/40 hover:border-yellow-400/60 hover:bg-blue-900/60'
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
                className="mt-4 px-8 py-4 rounded-full bg-gradient-to-r from-yellow-300 to-yellow-400 text-blue-950 font-bold text-lg hover:shadow-xl hover:shadow-yellow-400/50 transition-all duration-300 flex items-center gap-2"
              >
                <Phone className="w-5 h-5" />
                {startButtonText}
              </motion.button>

              <motion.a
                whileHover={{ scale: 1.05 }}
                href="https://slice.bank.in/"
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-yellow-300 hover:text-yellow-200 underline font-semibold"
              >
                Learn more about Slice Bank →
              </motion.a>
            </motion.div>
          </motion.div>
        </div>

        {/* How It Works Section */}
        <section className="relative py-24 px-4 md:px-6 bg-gradient-to-b from-blue-950 via-blue-900/50 to-blue-950">
          <div className="max-w-6xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8 }}
              className="text-center mb-16"
            >
              <h2 className="text-4xl md:text-5xl font-black mb-4">
                <span className="bg-gradient-to-r from-yellow-300 to-yellow-200 bg-clip-text text-transparent">
                  How It Works
                </span>
              </h2>
              <p className="text-blue-100/70 text-lg">Real-time fraud detection powered by voice AI</p>
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
                title="Voice Verification"
                description="Customer initiates transaction. AI voice system verifies identity through natural conversation."
              />
              <HowItWorksCard
                icon={Zap}
                step={2}
                title="Real-Time Detection"
                description="Advanced ML models instantly analyze patterns, anomalies, and behavioral data for fraud detection."
              />
              <HowItWorksCard
                icon={CheckCircle2}
                step={3}
                title="Instant Authorization"
                description="Secure transactions approved or flagged. Customer gets immediate confirmation with detailed summary."
              />
            </motion.div>
          </div>
        </section>

        {/* Features Section */}
        <section className="relative py-24 px-4 md:px-6 bg-gradient-to-b from-blue-950 to-slate-900">
          <div className="max-w-6xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8 }}
              className="text-center mb-16"
            >
              <h2 className="text-4xl md:text-5xl font-black mb-4">
                <span className="bg-gradient-to-r from-yellow-300 to-yellow-200 bg-clip-text text-transparent">
                  Banking Features
                </span>
              </h2>
              <p className="text-blue-100/70 text-lg">Everything you need for safe, transparent banking</p>
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
                title="Voice-First Security"
                description="Natural conversations for identity verification and transaction authorization."
              />
              <FeatureCard
                icon={BarChart3}
                title="Real-Time Monitoring"
                description="Continuous analysis of transaction patterns to detect and prevent fraud instantly."
              />
              <FeatureCard
                icon={MessageCircle}
                title="Smart Alerts"
                description="Intelligent notifications about suspicious activity with instant verification options."
              />
              <FeatureCard
                icon={Zap}
                title="Instant Response"
                description="Approve or block transactions in real-time through secure voice channel."
              />
              <FeatureCard
                icon={Clock}
                title="24/7 Protection"
                description="Round-the-clock monitoring and fraud detection for every transaction."
              />
              <FeatureCard
                icon={CheckCircle2}
                title="Transparent Banking"
                description="No hidden fees or complex terms. Just clear, honest banking at 100% RBI repo rate."
              />
            </motion.div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="relative py-20 px-4 md:px-6 border-t border-blue-500/20 bg-gradient-to-r from-blue-950 to-slate-900">
          <div className="max-w-2xl mx-auto text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8 }}
            >
              <h2 className="text-3xl md:text-4xl font-black mb-2">
                <span className="bg-gradient-to-r from-yellow-300 to-yellow-200 bg-clip-text text-transparent">
                  Take Control of Your Money
                </span>
              </h2>
              <p className="text-blue-100/70 mb-6">Banking the way you want it. No fine print. No hidden fees.</p>
              <motion.a
                whileHover={{ scale: 1.05 }}
                href="https://slice.bank.in/"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block px-8 py-4 rounded-full bg-gradient-to-r from-yellow-300 to-yellow-400 text-blue-950 font-bold hover:shadow-xl hover:shadow-yellow-400/50 transition-all duration-300"
              >
                Start Your Banking Journey
              </motion.a>
            </motion.div>
          </div>
        </section>

        {/* Footer */}
        <footer className="relative border-t border-blue-500/20 py-12 px-4 md:px-6 bg-blue-950/40">
          <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6 text-center md:text-left">
            <div className="text-blue-100/60 text-sm">
              © 2025 Slice Bank — Voice Fraud Detection. All rights reserved.
            </div>
            <div className="text-blue-100/60 text-sm">
              Secured with <span className="text-yellow-300 font-semibold">Advanced ML</span> + <span className="text-yellow-300 font-semibold">Voice AI</span>
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
};
