'use client';

import React, { useState } from 'react';
import { motion } from 'motion/react';
import { ShoppingBag, Mic, Clock, Sparkles, Truck, Users } from 'lucide-react';
import { Button } from '@/components/livekit/button';

interface WelcomeViewProps {
  startButtonText: string;
  onStartCall: (mode?: 'learning' | 'quiz' | 'teach-back') => void;
}

export const WelcomeView = ({ startButtonText, onStartCall, ref }: React.ComponentProps<'div'> & WelcomeViewProps) => {
  const [mode, setMode] = useState<'learning' | 'quiz' | 'teach-back'>('learning');

  const handleStart = () => {
    onStartCall(mode);
  };

  return (
    <div ref={ref} className="w-full min-h-screen bg-white overflow-y-auto">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-40 bg-white/80 backdrop-blur-md border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-4 md:px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 rounded-full bg-teal-500 flex items-center justify-center shadow-lg">
              <ShoppingBag className="w-6 h-6 text-white" />
            </div>
            <span className="font-bold text-xl text-teal-600">ZEPTO</span>
          </div>
          <a
            href="https://www.zepto.com/"
            target="_blank"
            rel="noopener noreferrer"
            className="px-4 py-2 rounded-lg bg-teal-500 text-white font-semibold hover:bg-teal-600 transition-colors text-sm"
          >
            Get App
          </a>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="min-h-screen flex flex-col items-center justify-center px-4 pt-32 pb-20">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center max-w-3xl"
        >
          {/* Main Headline */}
          <motion.h1 className="text-5xl md:text-7xl font-black mb-6 leading-tight">
            <span className="text-teal-600">Order Groceries</span>
            <br />
            <span className="text-gray-900">In 10 Minutes</span>
          </motion.h1>

          {/* Subheadline */}
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3, duration: 0.8 }}
            className="text-lg md:text-2xl text-gray-600 mb-8 leading-relaxed"
          >
            Use your voice to order fresh groceries, electronics, and everyday essentials. Fast, easy, delivered instantly.
          </motion.p>

          {/* Feature Pills */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5, duration: 0.8 }}
            className="flex flex-wrap justify-center gap-3 mb-10"
          >
            {[
              { icon: Clock, label: '10-min delivery' },
              { icon: Mic, label: 'Voice ordering' },
              { icon: Sparkles, label: 'AI-powered' },
            ].map((pill, i) => {
              const Icon = pill.icon;
              return (
                <div
                  key={i}
                  className="flex items-center gap-2 px-4 py-2 rounded-full bg-gradient-to-r from-teal-50 to-emerald-50 border border-teal-200"
                >
                  <Icon className="w-4 h-4 text-teal-600" />
                  <span className="text-sm font-semibold text-teal-700">{pill.label}</span>
                </div>
              );
            })}
          </motion.div>

          {/* Mode Selector */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.7, duration: 0.8 }}
            className="flex flex-wrap justify-center gap-3 mb-8"
          >
            {[
              { id: 'learning', label: 'Browse', icon: '🛍️' },
              { id: 'quiz', label: 'Order', icon: '📦' },
              { id: 'teach-back', label: 'Track', icon: '🚚' },
            ].map((m) => (
              <button
                key={m.id}
                onClick={() => setMode(m.id as 'learning' | 'quiz' | 'teach-back')}
                className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                  mode === m.id
                    ? 'bg-teal-500 text-white shadow-lg shadow-teal-500/30'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {m.icon} {m.label}
              </button>
            ))}
          </motion.div>

          {/* CTA Button */}
          <motion.button
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.9, duration: 0.8 }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleStart}
            className="px-10 py-4 rounded-xl bg-gradient-to-r from-teal-500 to-emerald-500 text-white font-bold text-lg hover:shadow-xl hover:shadow-teal-500/30 transition-all flex items-center gap-3 mx-auto mb-6"
          >
            <Mic className="w-5 h-5" />
            {startButtonText}
          </motion.button>
        </motion.div>
      </div>

      {/* Stats Section */}
      <section className="py-20 px-4 md:px-6 bg-gradient-to-b from-gray-50 to-white">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-black mb-4 text-gray-900">Why Zepto?</h2>
            <p className="text-lg text-gray-600">Everything you need for instant grocery delivery</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8, staggerChildren: 0.1 }}
            className="grid md:grid-cols-3 gap-8"
          >
            {[
              {
                icon: Truck,
                title: '10-Minute Delivery',
                desc: 'Order placed. Delivered in minutes. Every time.',
              },
              {
                icon: ShoppingBag,
                title: '7000+ Products',
                desc: 'Groceries, fresh fruits, electronics, and more.',
              },
              {
                icon: Users,
                title: 'Trusted by Millions',
                desc: 'India\'s fastest growing grocery platform.',
              },
            ].map((stat, i) => {
              const Icon = stat.icon;
              return (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.2 }}
                  className="p-8 rounded-2xl bg-white border border-gray-200 hover:border-teal-300 hover:shadow-xl transition-all"
                >
                  <div className="w-14 h-14 rounded-full bg-teal-100 flex items-center justify-center mb-4">
                    <Icon className="w-7 h-7 text-teal-600" />
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 mb-2">{stat.title}</h3>
                  <p className="text-gray-600">{stat.desc}</p>
                </motion.div>
              );
            })}
          </motion.div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 px-4 md:px-6 bg-white">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-black mb-4 text-gray-900">How It Works</h2>
            <p className="text-lg text-gray-600">Four simple steps to your doorstep</p>
          </motion.div>

          <div className="grid md:grid-cols-4 gap-6">
            {[
              { step: '1', title: 'Speak', desc: 'Tell Zepto what you need' },
              { step: '2', title: 'Select', desc: 'AI shows best options' },
              { step: '3', title: 'Order', desc: 'Voice confirms purchase' },
              { step: '4', title: 'Receive', desc: 'Delivery in 10 mins' },
            ].map((item, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.15 }}
                className="relative"
              >
                <div className="text-center">
                  <div className="w-16 h-16 rounded-full bg-gradient-to-br from-teal-500 to-emerald-500 flex items-center justify-center mx-auto mb-4 text-2xl font-black text-white">
                    {item.step}
                  </div>
                  <h3 className="text-lg font-bold text-gray-900 mb-2">{item.title}</h3>
                  <p className="text-sm text-gray-600">{item.desc}</p>
                </div>
                {i < 3 && (
                  <div className="hidden md:block absolute top-8 -right-3 w-6 h-1 bg-gradient-to-r from-teal-500 to-transparent" />
                )}
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 md:px-6 bg-gradient-to-r from-teal-600 to-emerald-600">
        <div className="max-w-2xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl font-black mb-4 text-white">Ready to Order?</h2>
            <p className="text-lg text-white/90 mb-8">Start speaking to your personal shopping assistant now</p>
            <button
              onClick={handleStart}
              className="px-8 py-4 rounded-xl bg-white text-teal-600 font-bold text-lg hover:shadow-2xl transition-all flex items-center gap-2 mx-auto"
            >
              <Mic className="w-5 h-5" />
              Start Voice Ordering
            </button>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-4 md:px-6 bg-gray-900 text-white">
        <div className="max-w-6xl mx-auto text-center">
          <p className="text-gray-400 text-sm mb-2">© 2025 Zepto — Smart Order Voice Assistant</p>
          <p className="text-gray-500 text-xs">
            Powered by <span className="text-teal-400 font-semibold">Voice AI</span> • Fast
            <span className="text-teal-400 font-semibold">10-min Delivery</span>
          </p>
        </div>
      </footer>
    </div>
  );
};
