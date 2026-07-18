'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Send, 
  Sparkles, 
  TrendingUp, 
  Coins, 
  Target, 
  AlertTriangle, 
  RefreshCw, 
  FileText, 
  ChevronRight,
  ShieldAlert,
  Briefcase,
  Download
} from 'lucide-react';

const DEFAULT_BRIEF = `Brand: 'AeroVibe' — a premium sustainable consumer electronics brand targeting affluent tech professionals (ages 25-45) in metropolitan hubs who value eco-friendly status symbols but are immune to basic greenwashing. 
Campaign Requirements: 
1. Retail: Premium interactive display stands inside high-end tech boutiques (e.g., Apple Premium Resellers) showcasing raw recycled components.
2. Digital: Ultra-targeted geo-ads around major business centers driving traffic to a high-converting web gateway. 
3. CSR Integration: Direct, auditable funding to regional e-waste recycling facilities to build real solar-powered hubs, completely avoiding empty PR vanity projects.`;

interface CampaignMeta {
  brand_name: string;
  target_audience_analysis: string;
  total_budget_usd: number;
}

interface ChannelAllocation {
  channel_name: string;
  allocation_percentage: number;
  allocation_budget_usd: number;
  core_strategy: string;
  activations: string[];
  kpis: string[];
}

interface B2BPitch {
  partner_name: string;
  target_role: string;
  pitch_text: string;
}

interface FinancialStressTest {
  risk_score: number;
  burn_rate_verdict: string;
  estimated_roi_multiplier: number;
  margin_leak_percentage: number;
}

interface CampaignResponse {
  campaign_meta: CampaignMeta;
  channels: ChannelAllocation[];
  cmo_verdict: string;
  b2b_pitches: B2BPitch[];
  financial_stress_test: FinancialStressTest;
}

const LOADING_PHASES = [
  "DECONSTRUCTING CORPORATE BUZZWORDS...",
  "REMOVING INFLATED SMM PROJECTIONS...",
  "EXTRACTING GENUINE CONSUMER SKEPTICISM...",
  "STRIPPING FLUFFY CHARITY MARKETING TACTICS...",
  "CALCULATING COLD RETAIL MATH ($ LIMIT)...",
  "SYNTHESIZING CMO CYNICAL VERDICT..."
];

const BudgetTicker = ({ target }: { target: number }) => {
  const [count, setCount] = useState(0);

  useEffect(() => {
    let start = 0;
    const end = target;
    if (start === end) return;

    const totalDuration = 1200; // ms
    const incrementTime = 25; // ms
    const steps = totalDuration / incrementTime;
    const stepValue = Math.ceil(end / steps);

    const timer = setInterval(() => {
      start += stepValue;
      if (start >= end) {
        setCount(end);
        clearInterval(timer);
      } else {
        setCount(start);
      }
    }, incrementTime);

    return () => clearInterval(timer);
  }, [target]);

  return <span>${count.toLocaleString()}</span>;
};

const SkeletonLoader = () => (
  <div className="space-y-4 animate-pulse">
    {/* Meta Card Skeleton */}
    <div className="glass-panel rounded-xl p-4 border-cyberBorder bg-slate-900/40">
      <div className="flex justify-between items-center mb-2">
        <div className="h-4 w-1/3 bg-slate-800 rounded" />
        <div className="h-6 w-24 bg-slate-800 rounded" />
      </div>
      <div className="space-y-1.5">
        <div className="h-2.5 w-full bg-slate-800 rounded" />
        <div className="h-2.5 w-5/6 bg-slate-800 rounded" />
      </div>
    </div>

    {/* Top Row Skeleton */}
    <div className="grid grid-cols-2 gap-4">
      <div className="h-32 bg-slate-900/40 rounded-xl border border-cyberBorder p-4" />
      <div className="h-32 bg-slate-900/40 rounded-xl border border-cyberBorder p-4" />
    </div>

    {/* Bottom Tabs Skeleton */}
    <div className="h-48 bg-slate-900/40 rounded-xl border border-cyberBorder p-4" />
  </div>
);

export default function Dashboard() {
  const [brief, setBrief] = useState(DEFAULT_BRIEF);
  const [cynicismLevel, setCynicismLevel] = useState<"realistic" | "hardcore" | "ruthless">("hardcore");
  const [totalBudget, setTotalBudget] = useState<number>(50000);
  const [isLoading, setIsLoading] = useState(false);
  const [loadingPhase, setLoadingPhase] = useState(0);
  const [strategyData, setStrategyData] = useState<CampaignResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [hoveredChannel, setHoveredChannel] = useState<string | null>(null);
  
  // Slider allocations state ($ amounts)
  const [allocations, setAllocations] = useState<Record<string, number>>({
    "HoReCa": 20000,
    "Digital": 10000,
    "Retail": 12500,
    "CSR": 7500
  });

  // Dynamic tabs selectors state
  const [activeBottomTab, setActiveBottomTab] = useState<'strategy' | 'b2b'>('strategy');
  const [activeChannelIdx, setActiveChannelIdx] = useState(0);
  const [activePitchIdx, setActivePitchIdx] = useState(0);

  // Negotiation Simulator States
  const [messages, setMessages] = useState<Array<{ sender: 'buyer' | 'user'; text: string }>>([]);
  const [userArg, setUserArg] = useState('');
  const [dealProbability, setDealProbability] = useState<number | null>(null);
  const [criticismPoint, setCriticismPoint] = useState<string | null>(null);
  const [isNegotiating, setIsNegotiating] = useState(false);
  const [isInitializingNegotiation, setIsInitializingNegotiation] = useState(false);

  // Sync allocations and tabs when strategyData resolves
  useEffect(() => {
    if (strategyData) {
      const initialAllocations: Record<string, number> = {};
      strategyData.channels.forEach(ch => {
        initialAllocations[ch.channel_name] = ch.allocation_budget_usd;
      });
      setAllocations(initialAllocations);
      setTotalBudget(strategyData.campaign_meta.total_budget_usd);
      setActiveBottomTab('strategy');
      setActiveChannelIdx(0);
      setActivePitchIdx(0);
      
      // Clear negotiations logs
      setMessages([]);
      setDealProbability(null);
      setCriticismPoint(null);
      setUserArg('');
    }
  }, [strategyData]);

  // Cycle loading phrases
  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isLoading) {
      interval = setInterval(() => {
        setLoadingPhase((prev) => (prev + 1) % LOADING_PHASES.length);
      }, 2000);
    } else {
      setLoadingPhase(0);
    }
    return () => clearInterval(interval);
  }, [isLoading]);

  // Recalculate allocations when total budget input changes to keep ratios locked
  const handleBudgetChange = (newBudget: number) => {
    const clampedBudget = Math.max(newBudget, 0);
    setTotalBudget(clampedBudget);
    
    const nextAllocations = { ...allocations };
    const channels = Object.keys(allocations);
    const prevTotal = Object.values(allocations).reduce((sum, val) => sum + val, 0) || clampedBudget || 1;
    
    let distributedSum = 0;
    channels.forEach((name, idx) => {
      if (idx === channels.length - 1) {
        nextAllocations[name] = clampedBudget - distributedSum;
      } else {
        const percentage = allocations[name] / prevTotal;
        const newChannelVal = Math.round(percentage * clampedBudget);
        nextAllocations[name] = newChannelVal;
        distributedSum += newChannelVal;
      }
    });
    setAllocations(nextAllocations);
  };

  // Proportional balance function adjusting sliders dynamically within dynamic total budget ranges
  const handleSliderChange = (targetName: string, newValue: number) => {
    const totalLimit = totalBudget;
    const step = totalLimit / 100;
    const clampedNewValue = Math.round(newValue / step) * step;

    if (clampedNewValue === allocations[targetName]) return;

    const remainingBudget = totalLimit - clampedNewValue;
    const otherChannels = Object.keys(allocations).filter(name => name !== targetName);
    const otherSum = otherChannels.reduce((sum, name) => sum + allocations[name], 0);

    let nextAllocations = { ...allocations };
    nextAllocations[targetName] = clampedNewValue;

    if (otherSum === 0) {
      const equalShare = Math.round((remainingBudget / otherChannels.length) / step) * step;
      otherChannels.forEach((name, idx) => {
        if (idx === otherChannels.length - 1) {
          nextAllocations[name] = remainingBudget - equalShare * (otherChannels.length - 1);
        } else {
          nextAllocations[name] = equalShare;
        }
      });
    } else {
      let distributedSum = 0;
      otherChannels.forEach((name, idx) => {
        if (idx === otherChannels.length - 1) {
          nextAllocations[name] = remainingBudget - distributedSum;
        } else {
          const share = Math.round(((allocations[name] / otherSum) * remainingBudget) / step) * step;
          nextAllocations[name] = share;
          distributedSum += share;
        }
      });
    }

    setAllocations(nextAllocations);
  };

  // Estimate risk indices locally
  const calculateLocalRisk = () => {
    if (totalBudget === 0) return 0;
    const horecaPct = (allocations["HoReCa"] || 0) / (totalBudget / 100);
    const retailPct = (allocations["Retail"] || 0) / (totalBudget / 100);
    const digitalPct = (allocations["Digital"] || 0) / (totalBudget / 100);
    
    let score = 30 + (horecaPct > 40 ? (horecaPct - 40) * 1.5 : 0) + (retailPct > 35 ? (retailPct - 35) * 1.5 : 0);
    if (digitalPct < 15) score += (15 - digitalPct) * 2;
    return Math.min(Math.round(score), 100);
  };

  const currentRiskScore = strategyData?.financial_stress_test 
    ? strategyData.financial_stress_test.risk_score 
    : calculateLocalRisk();

  const getProgressBarColor = (score: number) => {
    if (score > 70) return "bg-red-500 shadow-[0_0_8px_rgba(239,68,68,0.4)]";
    if (score > 40) return "bg-amber-500 shadow-[0_0_8px_rgba(245,158,11,0.4)]";
    return "bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.4)]";
  };

  const handleCompile = async (overrideAllocations: Record<string, number> | null = null) => {
    setIsLoading(true);
    setError(null);
    
    if (!overrideAllocations) {
      setStrategyData(null);
    }

    try {
      const res = await fetch('http://127.0.0.1:8000/campaign/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          raw_brief: brief,
          cynicism_level: cynicismLevel,
          total_budget_usd: totalBudget,
          custom_allocations: overrideAllocations
        }),
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || `Server responded with ${res.status}`);
      }

      const data: CampaignResponse = await res.json();
      setStrategyData(data);
    } catch (err: any) {
      console.error(err);
      setError(err.message || "Failed to communicate with the CMO compiler server.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleExportPDF = async () => {
    if (!strategyData) return;
    try {
      const res = await fetch('http://127.0.0.1:8000/campaign/export', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(strategyData),
      });

      if (!res.ok) {
        throw new Error("Failed to export PDF brief.");
      }

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${strategyData.campaign_meta.brand_name.replace(/\s+/g, '_')}_executive_brief.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err: any) {
      console.error(err);
      alert(err.message || "Failed to download PDF brief.");
    }
  };

  const handleInitializeNegotiation = () => {
    if (!strategyData) return;
    setIsInitializingNegotiation(true);
    try {
      const initialBuyerMsg = {
        sender: 'buyer' as const,
        text: `Your budget allocations look highly inflated. Specifically, allocating $${(allocations["HoReCa"] || 0).toLocaleString()} to Retail sounds like marketing vanity. Why should we list your brand with these display installation overhead costs instead of listing accessories brands that offer cold, hard margin rebates?`
      };
      
      setMessages([initialBuyerMsg]);
      setDealProbability(25);
      setCriticismPoint("High capital burn on retail endcaps.");
    } catch (err: any) {
      console.error(err);
      setError("Failed to initialize negotiation.");
    } finally {
      setIsInitializingNegotiation(false);
    }
  };

  const handleSendCounterArgument = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!strategyData || !userArg.trim() || isNegotiating) return;

    const userMessage = userArg;
    setUserArg('');

    const updatedMessages = [...messages, { sender: 'user' as const, text: userMessage }];
    setMessages(updatedMessages);
    setIsNegotiating(true);

    try {
      const res = await fetch('http://127.0.0.1:8000/campaign/negotiate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          strategy_context: strategyData,
          chat_history: updatedMessages,
          user_message: userMessage
        }),
      });

      if (!res.ok) {
        throw new Error("Category Buyer negotiation failed.");
      }

      const data = await res.json();
      setMessages(prev => [...prev, { sender: 'buyer' as const, text: data.buyer_response }]);
      setDealProbability(data.deal_probability);
      setCriticismPoint(data.criticism_point);
    } catch (err: any) {
      console.error(err);
      setMessages(prev => [...prev, { sender: 'buyer' as const, text: `[ERROR: Connection lost with Buyer Category Agent. Detail: ${err.message}]` }]);
    } finally {
      setIsNegotiating(false);
    }
  };

  return (
    <main className="h-screen overflow-hidden flex flex-col bg-slate-955 text-slate-100 p-4 font-sans relative">
      <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.01)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.01)_1px,transparent_1px)] bg-[size:40px_40px] pointer-events-none" />

      {/* Top Bar Navigation */}
      <header className="flex items-center justify-between border-b border-slate-800 pb-2.5 relative z-10">
        <div className="flex items-center space-x-2">
          <span className="h-2 w-2 rounded-full bg-cyan-500 animate-pulse" />
          <h1 className="text-xl font-bold tracking-tight text-white font-mono">
            BriefToLaunch
          </h1>
          <span className="text-xs text-gray-500 font-mono">| GLOBAL B2B CMO WORKSTATION</span>
        </div>
        
        <div className="flex items-center gap-3">
          {strategyData && (
            <button
              onClick={handleExportPDF}
              className="flex items-center gap-1.5 text-[10px] font-mono font-bold tracking-wider text-cyan-400 hover:text-cyan-300 bg-cyan-950/40 hover:bg-cyan-950/70 border border-cyan-500/30 hover:border-cyan-500/60 py-1 px-3 rounded shadow-sm transition-all duration-300"
            >
              <Download className="h-3 w-3" />
              <span>EXPORT BRIEF (PDF)</span>
            </button>
          )}
          <div className="flex items-center space-x-2 text-[10px] bg-slate-900/60 border border-slate-800 rounded-full py-1 px-3">
            <span className="flex h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse" />
            <span className="text-gray-400 font-mono">GLOBAL USD NODE ACTIVE</span>
          </div>
        </div>
      </header>

      {/* Grid workspace */}
      <div className="flex-1 grid grid-cols-12 gap-4 mt-4 overflow-hidden relative z-10">
        
        {/* Left Column Input Panel */}
        <div className="col-span-4 h-full flex flex-col space-y-4 overflow-hidden bg-slate-900/20 border border-slate-800 rounded-xl p-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-2">
            <h2 className="text-xs font-bold text-gray-300 uppercase tracking-wider font-mono flex items-center gap-1.5">
              <FileText className="h-3.5 w-3.5 text-cyan-400" />
              Brief Input Workspace
            </h2>
            <button 
              onClick={() => setBrief(DEFAULT_BRIEF)}
              className="text-[10px] font-mono text-cyan-400 hover:text-cyan-300 transition flex items-center gap-1 bg-cyan-955/20 border border-cyan-500/20 px-2 py-0.5 rounded"
            >
              <RefreshCw className="h-2.5 w-2.5" />
              Reset
            </button>
          </div>

          <textarea
            value={brief}
            onChange={(e) => setBrief(e.target.value)}
            placeholder="Paste your raw English brand briefing details here..."
            className="flex-1 w-full bg-slate-950/80 border border-slate-800 focus:border-cyan-500/50 rounded-lg p-3.5 font-mono text-[11px] text-gray-300 focus:outline-none focus:ring-1 focus:ring-cyan-500/50 resize-none transition-all duration-300"
          />

          {/* System Evaluation Mode selector */}
          <div className="space-y-1.5">
            <label className="text-[9px] text-cyan-400 font-mono tracking-widest uppercase block">
              SYSTEM EVALUATION MODE
            </label>
            <div className="grid grid-cols-3 gap-1.5 bg-slate-950 border border-slate-800 p-1 rounded-lg">
              {(["realistic", "hardcore", "ruthless"] as const).map((level) => (
                <button
                  key={level}
                  type="button"
                  onClick={() => setCynicismLevel(level)}
                  className={`py-1.5 text-[9px] font-mono font-bold tracking-wider rounded uppercase transition-all duration-300 ${
                    cynicismLevel === level
                      ? "border-cyan-500 bg-cyan-950/50 text-cyan-400 border shadow-[0_0_8px_rgba(6,182,212,0.15)] font-bold animate-pulse"
                      : "border-slate-800 bg-slate-950 text-slate-400 hover:text-slate-200 border"
                  }`}
                >
                  {level}
                </button>
              ))}
            </div>
          </div>

          <button
            onClick={() => handleCompile(null)}
            disabled={isLoading || !brief.trim()}
            className="w-full relative group overflow-hidden bg-gradient-to-r from-cyan-600 to-indigo-600 text-white rounded-lg py-2.5 px-4 font-semibold text-xs hover:from-cyan-500 hover:to-indigo-500 focus:outline-none focus:ring-2 focus:ring-cyan-400/50 disabled:opacity-50 disabled:cursor-not-allowed transition duration-300 shadow-md flex items-center justify-center gap-2 font-mono"
          >
            {isLoading ? (
              <>
                <RefreshCw className="h-3.5 w-3.5 animate-spin text-white" />
                <span>COMPILING...</span>
              </>
            ) : (
              <>
                <Sparkles className="h-3.5 w-3.5 text-cyan-200 group-hover:animate-bounce" />
                <span>COMPILE CAMPAIGN STRATEGY</span>
              </>
            )}
          </button>
        </div>

        {/* Right Column Strategic Output Panel */}
        <div className="col-span-8 h-full overflow-y-auto pr-2 space-y-4 scrollbar-thin flex flex-col">
          <AnimatePresence mode="wait">
            {isLoading && (
              <motion.div
                key="loading-overlay"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="space-y-4 flex-1 flex flex-col justify-center"
              >
                <div className="glass-panel rounded-xl p-4 flex items-center justify-center space-x-3 border-cyan-500/20 bg-slate-900/40">
                  <RefreshCw className="h-4 w-4 text-cyan-400 animate-spin" />
                  <span className="text-xs font-mono font-bold text-cyan-400 tracking-wider">
                    {LOADING_PHASES[loadingPhase]}
                  </span>
                </div>
                <SkeletonLoader />
              </motion.div>
            )}

            {error && !isLoading && (
              <motion.div
                key="error"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="glass-panel rounded-xl p-6 flex flex-col items-center justify-center space-y-4 flex-1 border-red-500/20 text-center bg-slate-900/20"
              >
                <div className="h-10 w-10 rounded-full bg-red-500/10 flex items-center justify-center">
                  <ShieldAlert className="h-5 w-5 text-red-500" />
                </div>
                <div className="space-y-1">
                  <h3 className="text-xs font-bold font-mono text-red-400">CMO COMPILATION FAILED</h3>
                  <p className="text-[11px] font-mono text-gray-400 max-w-md mx-auto">
                    {error}
                  </p>
                </div>
                <button
                  onClick={() => handleCompile(null)}
                  className="flex items-center gap-1 text-[10px] font-mono bg-red-500/10 hover:bg-red-500/20 border border-red-500/30 text-red-400 py-1 px-3 rounded-full transition"
                >
                  <RefreshCw className="h-2.5 w-2.5" /> RETRY COMPILATION
                </button>
              </motion.div>
            )}

            {!strategyData && !isLoading && !error && (
              <motion.div
                key="placeholder"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="glass-panel rounded-xl p-8 flex flex-col items-center justify-center text-center space-y-4 flex-1 border-dashed border-slate-800 bg-slate-900/10"
              >
                <div className="h-10 w-10 rounded-full bg-cyan-500/5 flex items-center justify-center border border-cyan-500/25">
                  <Send className="h-4.5 w-4.5 text-cyan-400" />
                </div>
                <div className="space-y-1">
                  <h3 className="text-xs font-bold font-mono text-gray-300">AWAITING SYSTEM PARAMETERS</h3>
                  <p className="text-[11px] font-mono text-gray-500 max-w-xs mx-auto">
                    Configure brief parameters and edit total budgets on the left workstation, and compile to synthesize.
                  </p>
                </div>
              </motion.div>
            )}

            {strategyData && !isLoading && !error && (
              <motion.div
                key="content"
                initial={{ opacity: 0, scale: 0.99 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.99 }}
                transition={{ duration: 0.3 }}
                className="space-y-4 flex-1 flex flex-col"
              >
                {/* Brand Profile Metadata Card */}
                <div className="glass-panel rounded-xl p-4 shadow-cyber-glass border-cyan-500/10 relative overflow-hidden bg-gradient-to-r from-slate-950 to-slate-900">
                  <div className="flex items-center justify-between mb-2">
                    <div className="space-y-0.5">
                      <span className="text-[9px] text-cyan-400 font-mono tracking-widest uppercase">BRAND PROFILE</span>
                      <h2 className="text-md font-bold text-gray-200 font-mono">
                        {strategyData.campaign_meta.brand_name}
                      </h2>
                    </div>
                    <div className="bg-slate-900 border border-slate-800 px-2.5 py-1 rounded flex items-center gap-1.5 shadow-[0_0_10px_rgba(6,182,212,0.05)] font-mono">
                      <Coins className="h-3 w-3 text-cyan-400" />
                      <span className="text-[11px] font-bold text-white">
                        <BudgetTicker target={strategyData.campaign_meta.total_budget_usd} />
                      </span>
                    </div>
                  </div>
                  <p className="text-[11px] text-gray-300 font-mono leading-relaxed border-l border-cyan-500/40 pl-2.5 italic">
                    &ldquo;{strategyData.campaign_meta.target_audience_analysis}&rdquo;
                  </p>
                </div>

                {/* Top Section Layout: side-by-side indicators */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  
                  {/* Left panel: Budget Breakdown (Interactive sliders) */}
                  <div className="glass-panel rounded-xl p-4 shadow-cyber-glass border-slate-800 flex flex-col justify-between">
                    <div className="border-b border-slate-800 pb-2 mb-3 flex items-center justify-between gap-4">
                      <h3 className="text-xs font-bold text-gray-200 font-mono flex items-center gap-1.5 uppercase">
                        <TrendingUp className="h-3.5 w-3.5 text-indigo-400" />
                        Budget Breakdown
                      </h3>
                      
                      {/* Dynamic budget input */}
                      <div className="flex items-center gap-1.5 bg-slate-950 px-2 py-1 rounded border border-slate-850">
                        <span className="text-[9px] font-mono text-gray-500 uppercase">BUDGET ($):</span>
                        <input
                          type="number"
                          value={totalBudget}
                          onChange={(e) => handleBudgetChange(parseInt(e.target.value) || 0)}
                          className="bg-transparent border-none outline-none w-16 text-[10px] font-mono font-bold text-cyan-400 text-right"
                        />
                      </div>
                    </div>

                    {/* Compact Visual bar chart */}
                    <div className="h-2 w-full bg-slate-950 rounded-full overflow-hidden flex mb-4">
                      {strategyData.channels.map((ch, idx) => {
                        const colors = ['bg-cyan-500', 'bg-indigo-500', 'bg-violet-600', 'bg-fuchsia-600'];
                        const colorClass = colors[idx % colors.length];
                        return (
                          <div 
                            key={ch.channel_name}
                            style={{ width: `${((allocations[ch.channel_name] || 0) / (totalBudget / 100))}%` }}
                            className={`${colorClass} h-full relative cursor-pointer transition-all duration-300 hover:brightness-110`}
                            onMouseEnter={() => setHoveredChannel(ch.channel_name)}
                            onMouseLeave={() => setHoveredChannel(null)}
                          />
                        );
                      })}
                    </div>

                    {/* Interactive legend with responsive sliders */}
                    <div className="space-y-2">
                      {strategyData.channels.map((ch, idx) => {
                        const textColors = ['text-cyan-400', 'text-indigo-400', 'text-violet-400', 'text-fuchsia-400'];
                        const txtColor = textColors[idx % textColors.length];
                        const isHovered = hoveredChannel === ch.channel_name;

                        return (
                          <div 
                            key={ch.channel_name}
                            className={`p-1.5 border border-slate-900 rounded bg-slate-950/40 transition-all duration-300 ${
                              isHovered ? 'border-slate-800 bg-slate-950 ring-1 ring-cyan-500/10' : ''
                            }`}
                          >
                            <div className="flex justify-between items-center text-[10px] font-mono mb-1">
                              <span className="text-gray-400 uppercase">{ch.channel_name}</span>
                              <span className={`${txtColor} font-bold`}>
                                ${(allocations[ch.channel_name] || 0).toLocaleString()} ({(((allocations[ch.channel_name] || 0) / (totalBudget / 100))).toFixed(0)}%)
                              </span>
                            </div>
                            <input
                              type="range"
                              min="0"
                              max={totalBudget}
                              step={totalBudget / 100}
                              value={allocations[ch.channel_name] || 0}
                              onChange={(e) => handleSliderChange(ch.channel_name, parseInt(e.target.value))}
                              className="w-full h-1 bg-slate-950 rounded-lg appearance-none cursor-pointer accent-cyan-500"
                            />
                          </div>
                        );
                      })}
                    </div>

                    <div className="mt-3 flex justify-end">
                      <button
                        onClick={() => handleCompile(allocations)}
                        disabled={isLoading}
                        className="flex items-center gap-1.5 text-[9px] font-mono font-bold tracking-wider text-slate-300 hover:text-cyan-400 bg-slate-950 hover:bg-slate-900 border border-slate-800 hover:border-cyan-500/30 py-1.5 px-3 rounded shadow-sm transition-all duration-300"
                      >
                        <RefreshCw className="h-2.5 w-2.5" />
                        <span>RE-OPTIMIZE ACTIVATIONS</span>
                      </button>
                    </div>
                  </div>

                  {/* Right panel: Stress Test */}
                  <div className="glass-panel rounded-xl p-4 shadow-cyber-glass border-slate-800 flex flex-col justify-between">
                    <div className="border-b border-slate-800 pb-1.5 mb-3 flex items-center justify-between gap-4">
                      <h3 className="text-xs font-bold text-gray-200 font-mono flex items-center gap-1.5 uppercase">
                        <ShieldAlert className="h-3.5 w-3.5 text-red-400" />
                        CMO Capital Stress Test
                      </h3>
                      
                      {/* Margin Leakage Detector */}
                      {strategyData.financial_stress_test && (
                        <div className="inline-flex items-center gap-1.5 bg-cyan-950/30 border border-cyan-500/30 rounded px-2 py-0.5 text-[9px] font-mono text-cyan-400">
                          <span>LEAK DETECTOR: {strategyData.financial_stress_test.margin_leak_percentage}%</span>
                        </div>
                      )}
                    </div>

                    <div className="space-y-3 flex-1 flex flex-col justify-between">
                      {/* Risk Score */}
                      <div className="space-y-1">
                        <div className="flex justify-between items-center text-[10px] font-mono">
                          <span className="text-gray-400">STRUCTURAL RISK INDEX</span>
                          <span className={`font-bold ${
                            currentRiskScore > 70 ? 'text-red-400' : (currentRiskScore > 40 ? 'text-amber-400' : 'text-emerald-400')
                          }`}>
                            {currentRiskScore}/100
                          </span>
                        </div>
                        <div className="h-1.5 w-full bg-slate-950 rounded-full overflow-hidden">
                          <div 
                            className={`h-full rounded-full transition-all duration-500 ${getProgressBarColor(currentRiskScore)}`}
                            style={{ width: `${currentRiskScore}%` }}
                          />
                        </div>
                      </div>

                      {/* Burn Rate Verdict */}
                      <div className="bg-slate-950 border border-slate-800 rounded p-2.5 font-mono text-[10px] text-gray-300 relative overflow-hidden flex-1 mt-2">
                        <div className="text-[9px] text-gray-500 font-bold uppercase tracking-wider border-b border-slate-800/60 pb-1 mb-1.5">
                          CAPITAL BURN RATE VERDICT
                        </div>
                        <p className="leading-normal">
                          {strategyData.financial_stress_test?.burn_rate_verdict || 
                            "Drag budget sliders to calculate real-time capital allocation stress metrics."}
                        </p>
                      </div>

                      {/* ROI Multiplier */}
                      {strategyData.financial_stress_test && (
                        <div className="flex justify-between items-center text-[10px] bg-slate-950/40 border border-slate-800 rounded p-2 mt-2">
                          <span className="text-gray-400 font-mono uppercase">ESTIMATED ROI MULTIPLIER</span>
                          <span className="text-cyan-400 font-mono font-bold text-xs">
                            {strategyData.financial_stress_test.estimated_roi_multiplier.toFixed(2)}x
                          </span>
                        </div>
                      )}
                    </div>
                  </div>

                </div>

                {/* Bottom Section: Tabs system */}
                <div className="glass-panel rounded-xl p-4 shadow-cyber-glass border-slate-800 flex-1 flex flex-col overflow-hidden">
                  
                  {/* Main Tab Controls */}
                  <div className="flex border-b border-slate-800 pb-2 mb-3">
                    <button
                      onClick={() => setActiveBottomTab('strategy')}
                      className={`px-4 py-1 text-xs font-mono font-bold tracking-wider border-b-2 transition-all duration-300 uppercase mr-4 ${
                        activeBottomTab === 'strategy'
                          ? "border-cyan-500 text-cyan-400"
                          : "border-transparent text-gray-400 hover:text-gray-200"
                      }`}
                    >
                      [ Tactical Strategy & KPIs ]
                    </button>
                    <button
                      onClick={() => {
                        setActiveBottomTab('b2b');
                        if (messages.length === 0) {
                          handleInitializeNegotiation();
                        }
                      }}
                      className={`px-4 py-1 text-xs font-mono font-bold tracking-wider border-b-2 transition-all duration-300 uppercase ${
                        activeBottomTab === 'b2b'
                          ? "border-cyan-500 text-cyan-400"
                          : "border-transparent text-gray-400 hover:text-gray-200"
                      }`}
                    >
                      [ B2B Pitch Matrix & War Room ]
                    </button>
                  </div>

                  {/* Tab A: Tactical Strategy */}
                  {activeBottomTab === 'strategy' && (
                    <div className="flex-1 flex flex-col overflow-hidden">
                      {/* Horizontal Sub-tabs */}
                      <div className="flex gap-1 bg-slate-950 p-0.5 rounded border border-slate-850 self-start mb-3">
                        {strategyData.channels.map((ch, idx) => (
                          <button
                            key={ch.channel_name}
                            onClick={() => setActiveChannelIdx(idx)}
                            className={`px-3 py-1 text-[9px] font-mono font-bold tracking-wide rounded uppercase transition-all duration-300 ${
                              activeChannelIdx === idx
                                ? "bg-slate-800 text-cyan-400 border border-cyan-500/20"
                                : "text-gray-400 hover:text-gray-200"
                            }`}
                          >
                            {ch.channel_name}
                          </button>
                        ))}
                      </div>

                      {/* Single dynamic channel detail card */}
                      {strategyData.channels[activeChannelIdx] && (
                        <div className="bg-slate-950/60 border border-slate-800 rounded p-4 font-mono text-[11px] text-gray-300 flex-1 overflow-y-auto space-y-3 scrollbar-thin">
                          <div>
                            <span className="text-[8px] text-cyan-400 font-bold block uppercase tracking-wider mb-1">
                              CORE STRATEGY
                            </span>
                            <p className="leading-relaxed border-l-2 border-cyan-500/20 pl-2.5">
                              {strategyData.channels[activeChannelIdx].core_strategy}
                            </p>
                          </div>

                          <div className="grid grid-cols-2 gap-4 pt-2">
                            <div>
                              <span className="text-[8px] text-indigo-400 font-bold block uppercase tracking-wider mb-1.5">
                                ACTIVATIONS
                              </span>
                              <ul className="space-y-1.5">
                                {strategyData.channels[activeChannelIdx].activations.map((act, actIdx) => (
                                  <li key={actIdx} className="text-[10px] text-gray-300 flex items-start gap-1.5 leading-relaxed">
                                    <ChevronRight className="h-3 w-3 mt-0.5 text-gray-500 flex-shrink-0" />
                                    <span>{act}</span>
                                  </li>
                                ))}
                              </ul>
                            </div>

                            <div>
                              <span className="text-[8px] text-violet-400 font-bold block uppercase tracking-wider mb-1.5">
                                TARGET CONVERSION KPIS
                              </span>
                              <div className="flex flex-wrap gap-1">
                                {strategyData.channels[activeChannelIdx].kpis.map((kpi, kpiIdx) => (
                                  <span 
                                    key={kpiIdx} 
                                    className="text-[9px] bg-slate-900 border border-slate-800 rounded py-0.5 px-2 font-mono text-gray-400 block"
                                  >
                                    {kpi}
                                  </span>
                                ))}
                              </div>
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  )}

                  {/* Tab B: B2B Pitch & Negotiation Simulator */}
                  {activeBottomTab === 'b2b' && (
                    <div className="flex-1 flex flex-col overflow-hidden space-y-3">
                      
                      {/* Dynamic B2B tab headers */}
                      {strategyData.b2b_pitches && strategyData.b2b_pitches.length > 0 && (
                        <div className="flex flex-col md:flex-row md:items-center justify-between border-b border-slate-800 pb-2 gap-2">
                          <span className="text-[10px] text-gray-400 font-mono tracking-wide uppercase">
                            DYNAMIC B2B COMMERCIAL PITCH MATRIX:
                          </span>
                          <div className="flex flex-wrap gap-1 bg-slate-950 p-0.5 rounded border border-slate-850">
                            {strategyData.b2b_pitches.map((pitch, idx) => (
                              <button
                                key={idx}
                                onClick={() => setActivePitchIdx(idx)}
                                className={`px-2 py-1 text-[9px] font-mono font-bold tracking-wide rounded uppercase transition-all duration-300 ${
                                  activePitchIdx === idx
                                    ? "bg-slate-800 text-cyan-400 border border-cyan-500/20"
                                    : "text-gray-400 hover:text-gray-200"
                                }`}
                              >
                                {pitch.partner_name}
                              </button>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Display pitch content card */}
                      {strategyData.b2b_pitches[activePitchIdx] && (
                        <div className="bg-slate-950/60 border border-slate-850 rounded p-3 font-mono text-[10px] text-gray-300 relative overflow-hidden space-y-1 bg-gradient-to-br from-indigo-950/5 to-transparent">
                          <div className="text-[8px] text-indigo-400 font-bold uppercase tracking-wider border-b border-slate-900 pb-1 mb-1">
                            TARGET CATEGORY: {strategyData.b2b_pitches[activePitchIdx].target_role}
                          </div>
                          <p className="leading-relaxed whitespace-pre-line text-slate-300">
                            {strategyData.b2b_pitches[activePitchIdx].pitch_text}
                          </p>
                        </div>
                      )}

                      {/* Appended War Room chat */}
                      <div className="bg-slate-950/80 border border-slate-855 rounded p-3 flex-1 flex flex-col overflow-hidden min-h-[160px]">
                        <div className="flex justify-between items-center border-b border-slate-900 pb-1.5 mb-2 text-[9px] font-mono">
                          <span className="text-red-400 font-bold tracking-wider uppercase flex items-center gap-1">
                            <span className="h-1.5 w-1.5 rounded-full bg-red-500 animate-ping" />
                            🖲️ SYSTEM WAR ROOM: BUYER NEGOTIATION SIMULATION
                          </span>
                          {dealProbability !== null && (
                            <div className="flex items-center gap-2">
                              <span className="text-gray-500">DEAL SUCCESS INDEX:</span>
                              <span className={`font-bold ${dealProbability > 60 ? 'text-emerald-400' : 'text-red-400'}`}>
                                {dealProbability}%
                              </span>
                              {criticismPoint && (
                                <span className="bg-red-950/30 border border-red-500/30 px-1.5 rounded text-[8px] text-red-400 uppercase">
                                  {criticismPoint}
                                </span>
                              )}
                            </div>
                          )}
                        </div>

                        {messages.length > 0 ? (
                          <div className="flex-1 flex flex-col overflow-hidden space-y-2">
                            <div className="flex-1 bg-slate-950 border border-slate-900 rounded p-2.5 font-mono text-[10px] overflow-y-auto space-y-2 flex flex-col scrollbar-thin">
                              {messages.map((msg, idx) => (
                                <div 
                                  key={idx} 
                                  className={`p-2 rounded max-w-[90%] leading-relaxed ${
                                    msg.sender === 'buyer' 
                                      ? 'bg-slate-900 border border-slate-800 self-start text-gray-300' 
                                      : 'bg-indigo-950/20 border border-indigo-500/10 self-end text-indigo-300'
                                  }`}
                                >
                                  <span className={`text-[8px] font-bold block uppercase tracking-wider mb-0.5 ${
                                    msg.sender === 'buyer' ? 'text-red-400' : 'text-indigo-400'
                                  }`}>
                                    {msg.sender === 'buyer' ? 'Buyer Category Agent' : 'User Presents'}
                                  </span>
                                  <p className="whitespace-pre-line">{msg.text}</p>
                                </div>
                              ))}
                              {isNegotiating && (
                                <div className="text-cyan-400 animate-pulse text-[9px] font-mono">
                                  Category Buyer drafts objections...
                                </div>
                              )}
                            </div>

                            <form onSubmit={handleSendCounterArgument} className="flex gap-1.5">
                              <input
                                type="text"
                                value={userArg}
                                onChange={(e) => setUserArg(e.target.value)}
                                placeholder="Enter margin counter-argument or allocation defense..."
                                disabled={isNegotiating}
                                className="flex-1 bg-slate-950 border border-slate-800 focus:border-cyan-500/50 rounded px-3 py-1.5 text-[10px] font-mono text-gray-300 focus:outline-none transition-all duration-300"
                              />
                              <button
                                type="submit"
                                disabled={isNegotiating || !userArg.trim()}
                                className="bg-slate-900 border border-slate-800 hover:border-cyan-500/30 text-slate-300 hover:text-cyan-400 rounded px-4 font-mono font-bold text-[10px] transition duration-300"
                              >
                                [ SEND ]
                              </button>
                            </form>
                          </div>
                        ) : (
                          <div className="flex-1 flex items-center justify-center border border-dashed border-slate-900">
                            <button
                              onClick={handleInitializeNegotiation}
                              className="text-[10px] font-mono bg-cyan-955/20 border border-cyan-500/30 text-cyan-400 py-1.5 px-4 rounded hover:bg-cyan-950/40 transition duration-300"
                            >
                              INITIALIZE NEGOTIATION INTERFACE
                            </button>
                          </div>
                        )}
                      </div>

                    </div>
                  )}

                </div>

                {/* CMO Verdict Panel */}
                <div className="bg-slate-950/80 rounded-xl p-3 border border-slate-800 shadow-cyber-glass relative overflow-hidden font-mono text-[10px]">
                  <div className="flex justify-between items-center border-b border-slate-900 pb-1.5 mb-2">
                    <span className="text-[9px] text-gray-500 font-bold tracking-wider uppercase flex items-center gap-1">
                      <AlertTriangle className="h-3 w-3 text-cyan-400" />
                      CMO EVALUATION FEEDBACK
                    </span>
                    <span className="text-[8px] text-cyan-400 bg-cyan-950/30 border border-cyan-500/30 px-1.5 py-0.5 rounded animate-pulse">
                      [ NODE STATUS: COMPLIANT ]
                    </span>
                  </div>
                  <p className="text-gray-300 leading-relaxed italic">&ldquo;{strategyData.cmo_verdict}&rdquo;</p>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </main>
  );
}
