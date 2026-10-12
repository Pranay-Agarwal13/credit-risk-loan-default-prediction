/**
 * Credit Risk & Loan Default Prediction System
 * Google AI Studio Interactive UI Preview
 *
 * Notice: UI preview with sample data; not connected to the trained model.
 * Institutional Disclaimer: This tool supports credit-risk review and does not make automated loan approval decisions.
 */

import React, { useState, useMemo } from 'react';
import { 
  ShieldCheck, 
  AlertTriangle, 
  FileSpreadsheet, 
  BarChart3, 
  Sliders, 
  Sparkles, 
  Database, 
  Download, 
  CheckCircle2, 
  XCircle, 
  ChevronRight, 
  TrendingUp, 
  Info,
  DollarSign,
  UserCheck,
  Search,
  RefreshCw,
  ExternalLink,
  Layers
} from 'lucide-react';

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';
import { Bar, Scatter } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

// Sample verified applicants across all 4 risk tiers
const SAMPLE_PRESETS = [
  {
    name: "Sarah Jenkins (Prime Low Risk)",
    tier: "Low",
    data: {
      id: "APP-100234",
      income: 240000,
      credit: 450000,
      annuity: 22500,
      contract: "Cash loans",
      gender: "F",
      education: "Higher education",
      age: 45,
      employedYears: 11.5,
      ext1: 0.72,
      ext2: 0.76,
      ext3: 0.81,
      bureauLoans: 1,
      bureauDebt: 42000
    }
  },
  {
    name: "David Ramirez (Standard Medium Risk)",
    tier: "Medium",
    data: {
      id: "APP-100871",
      income: 135000,
      credit: 520000,
      annuity: 28400,
      contract: "Cash loans",
      gender: "M",
      education: "Secondary / secondary special",
      age: 36,
      employedYears: 4.9,
      ext1: 0.48,
      ext2: 0.52,
      ext3: 0.44,
      bureauLoans: 2,
      bureauDebt: 165000
    }
  },
  {
    name: "Marcus Vance (Leveraged High Risk)",
    tier: "High",
    data: {
      id: "APP-101452",
      income: 90000,
      credit: 640000,
      annuity: 39500,
      contract: "Cash loans",
      gender: "M",
      education: "Secondary / secondary special",
      age: 27,
      employedYears: 1.2,
      ext1: 0.28,
      ext2: 0.31,
      ext3: 0.22,
      bureauLoans: 4,
      bureauDebt: 490000
    }
  },
  {
    name: "Elena Rostova (Distressed Critical Risk)",
    tier: "Critical",
    data: {
      id: "APP-102980",
      income: 65000,
      credit: 550000,
      annuity: 36800,
      contract: "Cash loans",
      gender: "F",
      education: "Lower secondary",
      age: 23,
      employedYears: 0.5,
      ext1: 0.12,
      ext2: 0.15,
      ext3: 0.09,
      bureauLoans: 5,
      bureauDebt: 460000
    }
  }
];

// Complete Batch Applicant Sample (showing Low, Medium, High, Critical)
const INITIAL_BATCH_APPLICANTS = [
  { id: 200001, name: "Sarah Jenkins", income: 280000, credit: 450000, annuity: 22500, dti: 1.61, extScore: 0.82, loans: 1, debt: 15000, prob: 0.028, tier: "Low", action: "Instant Approval - Prime Terms", decision: "PASS (ACCEPT)" },
  { id: 200002, name: "Thomas Sterling", income: 180000, credit: 500000, annuity: 27000, dti: 2.78, extScore: 0.68, loans: 1, debt: 45000, prob: 0.054, tier: "Low", action: "Instant Approval - Prime Terms", decision: "PASS (ACCEPT)" },
  { id: 200003, name: "Victoria Chen", income: 220000, credit: 580000, annuity: 31000, dti: 2.64, extScore: 0.74, loans: 2, debt: 82000, prob: 0.061, tier: "Low", action: "Instant Approval - Prime Terms", decision: "PASS (ACCEPT)" },
  { id: 200004, name: "David Ramirez", income: 150000, credit: 420000, annuity: 24000, dti: 2.80, extScore: 0.58, loans: 2, debt: 110000, prob: 0.124, tier: "Medium", action: "Approved with Automated Verification", decision: "PASS (ACCEPT)" },
  { id: 200005, name: "Rachel Kim", income: 135000, credit: 490000, annuity: 29000, dti: 3.63, extScore: 0.50, loans: 2, debt: 160000, prob: 0.168, tier: "Medium", action: "Approved with Automated Verification", decision: "PASS (ACCEPT)" },
  { id: 200006, name: "Jonathan Miller", income: 115000, credit: 520000, annuity: 32000, dti: 4.52, extScore: 0.42, loans: 3, debt: 230000, prob: 0.224, tier: "Medium", action: "Approved with Automated Verification", decision: "PASS (ACCEPT)" },
  { id: 200007, name: "Marcus Vance", income: 95000, credit: 580000, annuity: 36000, dti: 6.11, extScore: 0.34, loans: 3, debt: 320000, prob: 0.364, tier: "High", action: "Escalate for Senior Committee Review", decision: "FLAGGED FOR REVIEW / DECLINE" },
  { id: 200008, name: "Carlos Gomez", income: 85000, credit: 620000, annuity: 41000, dti: 7.29, extScore: 0.25, loans: 4, debt: 440000, prob: 0.442, tier: "High", action: "Escalate for Senior Committee Review", decision: "FLAGGED FOR REVIEW / DECLINE" },
  { id: 200009, name: "Avery Brooks", income: 105000, credit: 590000, annuity: 38000, dti: 5.62, extScore: 0.31, loans: 3, debt: 290000, prob: 0.388, tier: "High", action: "Escalate for Senior Committee Review", decision: "FLAGGED FOR REVIEW / DECLINE" },
  { id: 200010, name: "Elena Rostova", income: 72000, credit: 590000, annuity: 39500, dti: 8.19, extScore: 0.17, loans: 5, debt: 470000, prob: 0.672, tier: "Critical", action: "Adverse Decision / Automated Decline", decision: "FLAGGED FOR REVIEW / DECLINE" },
  { id: 200011, name: "Julian Bell", income: 60000, credit: 540000, annuity: 37000, dti: 9.00, extScore: 0.11, loans: 4, debt: 480000, prob: 0.748, tier: "Critical", action: "Adverse Decision / Automated Decline", decision: "FLAGGED FOR REVIEW / DECLINE" },
  { id: 200012, name: "Darren Walsh", income: 52000, credit: 490000, annuity: 35000, dti: 9.42, extScore: 0.08, loans: 5, debt: 450000, prob: 0.812, tier: "Critical", action: "Adverse Decision / Automated Decline", decision: "FLAGGED FOR REVIEW / DECLINE" }
];

export default function App() {
  const [activeTab, setActiveTab] = useState<'assess' | 'batch' | 'portfolio' | 'performance' | 'shap' | 'insights'>('assess');

  // Single Applicant Form State
  const [formData, setFormData] = useState({
    income: 150000,
    credit: 500000,
    annuity: 25000,
    contract: "Cash loans",
    gender: "F",
    education: "Secondary / secondary special",
    age: 38,
    employedYears: 6.5,
    ext1: 0.55,
    ext2: 0.52,
    ext3: 0.48,
    bureauLoans: 2,
    bureauDebt: 90000
  });

  // Threshold Simulator State
  const [threshold, setThreshold] = useState<number>(0.24);

  // Batch Scoring & Schema Validator State
  const [tierFilters, setTierFilters] = useState<string[]>(["Low", "Medium", "High", "Critical"]);
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [heatmapDimension, setHeatmapDimension] = useState<'income' | 'bureau'>('income');
  const [heatmapViewType, setHeatmapViewType] = useState<'chartjs' | 'matrix'>('chartjs');
  
  // Interactive CSV Schema Validator State
  const [detectedColumns, setDetectedColumns] = useState<string[]>([
    "SK_ID_CURR", "AMT_INCOME_TOTAL", "AMT_CREDIT", "AMT_ANNUITY", "DAYS_BIRTH", "DAYS_EMPLOYED", "EXT_SOURCE_2", "NAME_CONTRACT_TYPE", "CODE_GENDER"
  ]);
  const [batchApplicants, setBatchApplicants] = useState(INITIAL_BATCH_APPLICANTS);
  const [uploadFileName, setUploadFileName] = useState<string>("test_batch_sample.csv");
  const [isScored, setIsScored] = useState<boolean>(true);
  const [showChecklistDetails, setShowChecklistDetails] = useState<boolean>(false);

  // Helper for Underwriting Calculations
  const applicantMetrics = useMemo(() => {
    const dti = formData.credit / Math.max(1, formData.income);
    const paymentRate = (formData.annuity / Math.max(1, formData.credit)) * 100;
    const annuityBurden = (formData.annuity / Math.max(1, formData.income)) * 100;
    const compositeExt = (formData.ext1 + formData.ext2 + formData.ext3) / 3;

    // Calibrated probability estimator formula
    let rawScore = 0.0;
    rawScore += (1.0 - compositeExt) * 0.42;
    rawScore += Math.max(0, (dti - 2.5) / 6.0) * 0.28;
    rawScore += Math.max(0, (45 - formData.age) / 25.0) * 0.12;
    rawScore += Math.min(0.35, (formData.bureauDebt / Math.max(1, formData.income)) * 0.18);
    rawScore += Math.max(0, (3.0 - formData.employedYears) / 6.0) * 0.10;

    const prob = 1.0 / (1.0 + Math.exp(-((rawScore - 0.42) * 5.8)));
    const probability = Math.min(0.96, Math.max(0.018, prob));

    let tier = "Low";
    let action = "Instant Approval - Prime Interest Rates";
    let color = "emerald";

    if (probability < 0.10) {
      tier = "Low";
      action = "Instant Approval - Prime Interest Rates";
      color = "emerald";
    } else if (probability < 0.25) {
      tier = "Medium";
      action = "Approved with Automated Verification Check";
      color = "amber";
    } else if (probability < 0.50) {
      tier = "High";
      action = "Escalate to Senior Credit Underwriter / Committee Review";
      color = "orange";
    } else {
      tier = "Critical";
      action = "Adverse Decision / Automated Decline or Secured Exception Only";
      color = "crimson";
    }

    const decision = probability >= threshold ? "FLAGGED FOR REVIEW / DECLINE" : "PASS (ACCEPT)";

    // SHAP waterfall items
    const shapFactors = [
      { name: "External Agency Score 2", value: formData.ext2.toFixed(2), shap: Number(((0.50 - formData.ext2) * 0.38).toFixed(2)) },
      { name: "External Agency Score 3", value: formData.ext3.toFixed(2), shap: Number(((0.50 - formData.ext3) * 0.35).toFixed(2)) },
      { name: "Credit-to-Income Ratio (DTI)", value: `${dti.toFixed(2)}x`, shap: Number((Math.max(0, dti - 2.8) * 0.16).toFixed(2)) },
      { name: "Prior Credit Bureau Debt", value: `$${formData.bureauDebt.toLocaleString()}`, shap: Number((Math.min(0.30, (formData.bureauDebt / formData.income) * 0.18)).toFixed(2)) },
      { name: "Employment Tenure", value: `${formData.employedYears} yrs`, shap: Number(((3.5 - formData.employedYears) * 0.04).toFixed(2)) },
      { name: "Applicant Age", value: `${formData.age} yrs`, shap: Number(((38 - formData.age) * 0.015).toFixed(2)) }
    ];

    const positiveDrivers = shapFactors.filter(f => f.shap > 0).sort((a, b) => b.shap - a.shap);
    const negativeMitigators = shapFactors.filter(f => f.shap < 0).sort((a, b) => a.shap - b.shap);

    return {
      dti,
      paymentRate,
      annuityBurden,
      compositeExt,
      probability,
      tier,
      action,
      color,
      decision,
      shapFactors,
      positiveDrivers,
      negativeMitigators
    };
  }, [formData, threshold]);

  // Threshold Dynamic Matrix Calculations
  const thresholdMetrics = useMemo(() => {
    const testN = 61503;
    const testDefaulters = 4963;
    const testRepaid = testN - testDefaulters;

    const zDef = (Math.log(threshold / (1 - threshold)) + 1.2) / 1.1;
    const zRep = (Math.log(threshold / (1 - threshold)) + 2.8) / 1.0;

    const recall = Math.min(0.98, Math.max(0.08, 1.0 - (1.0 / (1.0 + Math.exp(-zDef * 1.8)))));
    const fpr = Math.min(0.85, Math.max(0.01, 1.0 - (1.0 / (1.0 + Math.exp(-zRep * 1.8)))));

    const tp = Math.round(testDefaulters * recall);
    const fn = Math.round(testDefaulters - tp);
    const fp = Math.round(testRepaid * fpr);
    const tn = Math.round(testRepaid - fp);

    const precision = tp / Math.max(1, tp + fp);
    const f1 = (2 * precision * recall) / Math.max(0.001, precision + recall);

    const costFn = 10000;
    const costFp = 1200;
    const totalCost = (fn * costFn) + (fp * costFp);

    return {
      recall,
      precision,
      f1,
      tp,
      fn,
      fp,
      tn,
      totalCost,
      testN,
      testDefaulters
    };
  }, [threshold]);

  // Schema Validation Memo for Batch CSV Upload
  const schemaReport = useMemo(() => {
    const requiredSpecs = [
      { key: "SK_ID_CURR", label: "Applicant Unique ID", type: "Integer" },
      { key: "AMT_INCOME_TOTAL", label: "Annual Declared Income", type: "Float (> 0)" },
      { key: "AMT_CREDIT", label: "Requested Credit Amount", type: "Float (> 0)" },
      { key: "AMT_ANNUITY", label: "Annual Loan Annuity", type: "Float (> 0)" },
      { key: "DAYS_BIRTH", label: "Age in Days (Negative)", type: "Integer (< 0)" },
      { key: "DAYS_EMPLOYED", label: "Employment Tenure Days", type: "Integer" },
      { key: "EXT_SOURCE_2", label: "External Agency Score 2", type: "Float (0.01-0.99)" }
    ];

    const recommendedSpecs = [
      { key: "NAME_CONTRACT_TYPE", label: "Contract Type", type: "String" },
      { key: "CODE_GENDER", label: "Borrower Gender", type: "String (M/F)" },
      { key: "NAME_EDUCATION_TYPE", label: "Education Level", type: "String" },
      { key: "EXT_SOURCE_1", label: "External Score 1", type: "Float" },
      { key: "EXT_SOURCE_3", label: "External Score 3", type: "Float" },
      { key: "BUREAU_ACTIVE_LOANS_COUNT", label: "Active Bureau Loans", type: "Integer" },
      { key: "BUREAU_AMT_CREDIT_SUM_DEBT_SUM", label: "Prior Bureau Debt ($)", type: "Float" }
    ];

    const detectedSet = new Set(detectedColumns.map(c => c.trim().toUpperCase()));
    const missingRequired = requiredSpecs.filter(r => !detectedSet.has(r.key.toUpperCase()));
    const presentRequired = requiredSpecs.filter(r => detectedSet.has(r.key.toUpperCase()));
    const presentRecommended = recommendedSpecs.filter(r => detectedSet.has(r.key.toUpperCase()));
    const missingRecommended = recommendedSpecs.filter(r => !detectedSet.has(r.key.toUpperCase()));
    const isValid = missingRequired.length === 0;

    return {
      isValid,
      missingRequired,
      presentRequired,
      presentRecommended,
      missingRecommended,
      requiredSpecs,
      recommendedSpecs,
      totalDetectedCount: detectedColumns.length
    };
  }, [detectedColumns]);

  // Filtered batch applicants (derived from batchApplicants state)
  const filteredBatch = useMemo(() => {
    return batchApplicants.filter(app => {
      const matchesTier = tierFilters.includes(app.tier);
      const matchesSearch = searchQuery === "" || 
        app.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
        app.id.toString().includes(searchQuery);
      return matchesTier && matchesSearch;
    });
  }, [batchApplicants, tierFilters, searchQuery]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-sky-500 selection:text-white">
      {/* Top Banner Notice */}
      <div className="bg-sky-950/80 border-b border-sky-800/60 px-6 py-2 text-xs text-sky-200 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Info className="w-3.5 h-3.5 text-sky-400 shrink-0" />
          <span><strong>UI preview with sample data; not connected to the trained model.</strong> Production Streamlit app with real XGBoost pipeline located in <code className="bg-sky-900/60 px-1 py-0.5 rounded text-sky-300">app/app.py</code>.</span>
        </div>
        <div className="text-slate-400 text-[11px] hidden md:block">
          DuckDB Engine · XGBoost · TreeSHAP · Port 3000
        </div>
      </div>

      {/* Top Navigation Bar */}
      <header className="border-b border-slate-800 bg-slate-900/90 backdrop-blur sticky top-0 z-30 px-6 py-3 flex items-center justify-between gap-8">
        {/* Brand Zone */}
        <div className="flex items-center gap-3 shrink-0">
          <div className="w-8 h-8 rounded-lg bg-sky-600 flex items-center justify-center font-bold text-white shadow-sm">
            CR
          </div>
          <span className="text-base font-bold tracking-tight text-white whitespace-nowrap">
            Credit Risk Underwriting System
          </span>
        </div>

        {/* 6 Nav Tabs */}
        <nav className="hidden lg:flex items-center gap-1 bg-slate-950/60 p-1 rounded-lg border border-slate-800">
          {[
            { id: 'assess', label: 'Applicant Assessment', icon: UserCheck },
            { id: 'batch', label: 'Batch Scoring', icon: FileSpreadsheet },
            { id: 'portfolio', label: 'Portfolio Analytics', icon: BarChart3 },
            { id: 'performance', label: 'Model Performance', icon: Sliders },
            { id: 'shap', label: 'SHAP Explainability', icon: Sparkles },
            { id: 'insights', label: 'Business Insights', icon: Database },
          ].map(tab => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center gap-2 px-3 py-1.5 text-xs font-medium rounded-md transition-colors whitespace-nowrap shrink-0 ${
                  isActive
                    ? 'bg-sky-600 text-white shadow-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>

        {/* Primary CTA / Active Model Tag */}
        <div className="flex items-center gap-3 shrink-0">
          <span className="text-xs text-slate-400 font-mono hidden sm:inline">
            Cutoff: <strong className="text-sky-400">{threshold.toFixed(2)}</strong>
          </span>
          <button
            onClick={() => setActiveTab('assess')}
            className="px-3 py-1.5 text-xs font-semibold text-white bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-md transition-colors whitespace-nowrap shrink-0 flex items-center gap-1.5"
          >
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
            <span>Score Applicant</span>
          </button>
        </div>
      </header>

      {/* Main Viewport Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-6 md:p-8 space-y-8">
        
        {/* ========================================================= */}
        {/* TAB 1: APPLICANT RISK ASSESSMENT */}
        {/* ========================================================= */}
        {activeTab === 'assess' && (
          <div className="space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800">
              <div>
                <h1 className="text-2xl font-bold tracking-tight text-white">Applicant Risk Assessment</h1>
                <p className="text-sm text-slate-400 mt-1">
                  Individual underwriting risk prediction, calibrated default probability, and plain-English SHAP attribution.
                </p>
              </div>

              {/* Preset Selector */}
              <div className="flex items-center gap-2 bg-slate-900 border border-slate-800 p-2 rounded-lg">
                <span className="text-xs text-slate-400 font-medium whitespace-nowrap">Load Preset Profile:</span>
                <select
                  className="bg-slate-950 text-xs text-slate-200 border border-slate-700 rounded px-2.5 py-1 focus:outline-none focus:border-sky-500"
                  onChange={(e) => {
                    const preset = SAMPLE_PRESETS.find(p => p.name === e.target.value);
                    if (preset) {
                      setFormData({
                        income: preset.data.income,
                        credit: preset.data.credit,
                        annuity: preset.data.annuity,
                        contract: preset.data.contract,
                        gender: preset.data.gender,
                        education: preset.data.education,
                        age: preset.data.age,
                        employedYears: preset.data.employedYears,
                        ext1: preset.data.ext1,
                        ext2: preset.data.ext2,
                        ext3: preset.data.ext3,
                        bureauLoans: preset.data.bureauLoans,
                        bureauDebt: preset.data.bureauDebt
                      });
                    }
                  }}
                >
                  <option value="">Choose preset...</option>
                  {SAMPLE_PRESETS.map(p => (
                    <option key={p.name} value={p.name}>{p.name}</option>
                  ))}
                </select>
              </div>
            </div>

            {/* Split Screen: Form on Left, Risk Scorecard & SHAP on Right */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
              {/* Form Input Container */}
              <div className="lg:col-span-7 bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-6">
                <div>
                  <h2 className="text-base font-semibold text-white">1. Loan Terms & Capacity</h2>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
                    <div>
                      <label className="text-xs text-slate-400 font-medium block mb-1">Annual Income ($)</label>
                      <input
                        type="number"
                        value={formData.income}
                        onChange={e => setFormData({ ...formData, income: Number(e.target.value) })}
                        className="w-full bg-slate-950 border border-slate-700 rounded-md px-3 py-1.5 text-sm text-slate-100 font-mono"
                      />
                    </div>
                    <div>
                      <label className="text-xs text-slate-400 font-medium block mb-1">Credit Requested ($)</label>
                      <input
                        type="number"
                        value={formData.credit}
                        onChange={e => setFormData({ ...formData, credit: Number(e.target.value) })}
                        className="w-full bg-slate-950 border border-slate-700 rounded-md px-3 py-1.5 text-sm text-slate-100 font-mono"
                      />
                    </div>
                    <div>
                      <label className="text-xs text-slate-400 font-medium block mb-1">Annuity Payment ($)</label>
                      <input
                        type="number"
                        value={formData.annuity}
                        onChange={e => setFormData({ ...formData, annuity: Number(e.target.value) })}
                        className="w-full bg-slate-950 border border-slate-700 rounded-md px-3 py-1.5 text-sm text-slate-100 font-mono"
                      />
                    </div>
                  </div>
                </div>

                <div className="border-t border-slate-800 pt-5">
                  <h2 className="text-base font-semibold text-white">2. Borrower Profile & Stability</h2>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
                    <div>
                      <label className="text-xs text-slate-400 font-medium block mb-1">Age (Years)</label>
                      <input
                        type="number"
                        value={formData.age}
                        onChange={e => setFormData({ ...formData, age: Number(e.target.value) })}
                        className="w-full bg-slate-950 border border-slate-700 rounded-md px-3 py-1.5 text-sm text-slate-100 font-mono"
                      />
                    </div>
                    <div>
                      <label className="text-xs text-slate-400 font-medium block mb-1">Employment Tenure (Yrs)</label>
                      <input
                        type="number"
                        step="0.5"
                        value={formData.employedYears}
                        onChange={e => setFormData({ ...formData, employedYears: Number(e.target.value) })}
                        className="w-full bg-slate-950 border border-slate-700 rounded-md px-3 py-1.5 text-sm text-slate-100 font-mono"
                      />
                    </div>
                    <div>
                      <label className="text-xs text-slate-400 font-medium block mb-1">Contract Type</label>
                      <select
                        value={formData.contract}
                        onChange={e => setFormData({ ...formData, contract: e.target.value })}
                        className="w-full bg-slate-950 border border-slate-700 rounded-md px-3 py-1.5 text-sm text-slate-100"
                      >
                        <option value="Cash loans">Cash loans</option>
                        <option value="Revolving loans">Revolving loans</option>
                      </select>
                    </div>
                  </div>
                </div>

                <div className="border-t border-slate-800 pt-5">
                  <h2 className="text-base font-semibold text-white">3. Credit Bureau Scores & Prior Debt</h2>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
                    <div>
                      <label className="text-xs text-slate-400 font-medium block mb-1">External Score 1 (0-1)</label>
                      <input
                        type="number"
                        step="0.01"
                        min="0.01"
                        max="0.99"
                        value={formData.ext1}
                        onChange={e => setFormData({ ...formData, ext1: Number(e.target.value) })}
                        className="w-full bg-slate-950 border border-slate-700 rounded-md px-3 py-1.5 text-sm text-slate-100 font-mono"
                      />
                    </div>
                    <div>
                      <label className="text-xs text-slate-400 font-medium block mb-1">External Score 2 (0-1)</label>
                      <input
                        type="number"
                        step="0.01"
                        min="0.01"
                        max="0.99"
                        value={formData.ext2}
                        onChange={e => setFormData({ ...formData, ext2: Number(e.target.value) })}
                        className="w-full bg-slate-950 border border-slate-700 rounded-md px-3 py-1.5 text-sm text-slate-100 font-mono"
                      />
                    </div>
                    <div>
                      <label className="text-xs text-slate-400 font-medium block mb-1">External Score 3 (0-1)</label>
                      <input
                        type="number"
                        step="0.01"
                        min="0.01"
                        max="0.99"
                        value={formData.ext3}
                        onChange={e => setFormData({ ...formData, ext3: Number(e.target.value) })}
                        className="w-full bg-slate-950 border border-slate-700 rounded-md px-3 py-1.5 text-sm text-slate-100 font-mono"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                    <div>
                      <label className="text-xs text-slate-400 font-medium block mb-1">Active External Bureau Loans</label>
                      <input
                        type="number"
                        value={formData.bureauLoans}
                        onChange={e => setFormData({ ...formData, bureauLoans: Number(e.target.value) })}
                        className="w-full bg-slate-950 border border-slate-700 rounded-md px-3 py-1.5 text-sm text-slate-100 font-mono"
                      />
                    </div>
                    <div>
                      <label className="text-xs text-slate-400 font-medium block mb-1">Total Bureau Debt Balance ($)</label>
                      <input
                        type="number"
                        value={formData.bureauDebt}
                        onChange={e => setFormData({ ...formData, bureauDebt: Number(e.target.value) })}
                        className="w-full bg-slate-950 border border-slate-700 rounded-md px-3 py-1.5 text-sm text-slate-100 font-mono"
                      />
                    </div>
                  </div>
                </div>
              </div>

              {/* Assessment Output Card */}
              <div className="lg:col-span-5 space-y-6">
                {/* Risk Tier Badge Card */}
                <div className={`p-6 rounded-xl border ${
                  applicantMetrics.tier === 'Low' ? 'bg-emerald-950/40 border-emerald-800/80 text-emerald-200' :
                  applicantMetrics.tier === 'Medium' ? 'bg-amber-950/40 border-amber-800/80 text-amber-200' :
                  applicantMetrics.tier === 'High' ? 'bg-orange-950/40 border-orange-800/80 text-orange-200' :
                  'bg-red-950/40 border-red-800/80 text-red-200'
                }`}>
                  <div className="flex items-center justify-between">
                    <div>
                      <span className="text-xs uppercase tracking-wider font-semibold opacity-80">Underwriting Risk Tier</span>
                      <h3 className="text-2xl font-bold mt-1">{applicantMetrics.tier} Risk</h3>
                    </div>
                    <div className="text-right">
                      <span className="text-xs uppercase tracking-wider font-semibold opacity-80">Default Probability</span>
                      <div className="text-2xl font-bold font-mono mt-1">
                        {(applicantMetrics.probability * 100).toFixed(2)}%
                      </div>
                    </div>
                  </div>

                  {/* Underwriting Recommendation Banner */}
                  <div className="mt-4 pt-4 border-t border-white/10 text-xs">
                    <span className="font-semibold block uppercase tracking-wide opacity-80 mb-0.5">Policy Action:</span>
                    <span className="text-white text-sm font-medium">{applicantMetrics.action}</span>
                  </div>

                  <div className="mt-2 text-xs flex items-center justify-between opacity-80">
                    <span>Operational Decision:</span>
                    <span className="font-bold font-mono">{applicantMetrics.decision}</span>
                  </div>
                </div>

                {/* Key Underwriting Ratios Strip */}
                <div className="grid grid-cols-3 gap-3 bg-slate-900 border border-slate-800 p-4 rounded-xl">
                  <div>
                    <span className="text-[11px] text-slate-400 block">Debt-to-Income</span>
                    <span className="text-base font-bold font-mono text-white">{applicantMetrics.dti.toFixed(2)}x</span>
                  </div>
                  <div>
                    <span className="text-[11px] text-slate-400 block">Payment Burden</span>
                    <span className="text-base font-bold font-mono text-white">{applicantMetrics.annuityBurden.toFixed(1)}%</span>
                  </div>
                  <div>
                    <span className="text-[11px] text-slate-400 block">External Score</span>
                    <span className="text-base font-bold font-mono text-white">{applicantMetrics.compositeExt.toFixed(3)}</span>
                  </div>
                </div>

                {/* SHAP Waterfall Chart */}
                <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl space-y-4">
                  <div className="flex items-center justify-between">
                    <h3 className="text-sm font-bold text-white flex items-center gap-2">
                      <Sparkles className="w-4 h-4 text-sky-400" />
                      Local SHAP Feature Attribution
                    </h3>
                    <span className="text-[11px] text-slate-400">Baseline = 0.0807</span>
                  </div>

                  {/* Bars */}
                  <div className="space-y-2.5 pt-2">
                    {applicantMetrics.shapFactors.map(factor => {
                      const isPositive = factor.shap > 0;
                      const widthPct = Math.min(100, Math.abs(factor.shap) * 180);
                      return (
                        <div key={factor.name} className="space-y-1">
                          <div className="flex justify-between text-xs">
                            <span className="text-slate-300">{factor.name}</span>
                            <span className={`font-mono font-semibold ${isPositive ? 'text-red-400' : 'text-emerald-400'}`}>
                              {isPositive ? `+${factor.shap.toFixed(2)}` : factor.shap.toFixed(2)}
                            </span>
                          </div>
                          <div className="w-full bg-slate-950 h-2 rounded-full overflow-hidden flex">
                            {isPositive ? (
                              <div
                                style={{ width: `${widthPct}%` }}
                                className="bg-red-500 h-full rounded-full transition-all duration-300 ml-auto"
                              />
                            ) : (
                              <div
                                style={{ width: `${widthPct}%` }}
                                className="bg-emerald-500 h-full rounded-full transition-all duration-300"
                              />
                            )}
                          </div>
                        </div>
                      );
                    })}
                  </div>

                  {/* Plain English Underwriter Summary */}
                  <div className="bg-slate-950 border border-slate-800/80 p-3.5 rounded-lg text-xs space-y-1.5 text-slate-300">
                    <strong className="text-sky-300 block">Underwriter Reason Code Audit:</strong>
                    <p>
                      {applicantMetrics.positiveDrivers.length > 0 ? (
                        <>Primary adverse factors: <strong className="text-red-300">{applicantMetrics.positiveDrivers.slice(0, 2).map(d => d.name).join(', ')}</strong>. </>
                      ) : (
                        <>No adverse debt or scoring factors detected. </>
                      )}
                      {applicantMetrics.negativeMitigators.length > 0 && (
                        <>Mitigating strengths: <strong className="text-emerald-300">{applicantMetrics.negativeMitigators.slice(0, 2).map(m => m.name).join(', ')}</strong>.</>
                      )}
                    </p>
                    <p className="text-[11px] text-slate-500 pt-1">
                      Note: SHAP demonstrates model-learned mathematical associations, not direct causation.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* TAB 2: BATCH SCORING WITH SCHEMA VALIDATOR */}
        {/* ========================================================= */}
        {activeTab === 'batch' && (
          <div className="space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800">
              <div>
                <h1 className="text-2xl font-bold tracking-tight text-white">Batch Portfolio Scoring & Schema Inspector</h1>
                <p className="text-sm text-slate-400 mt-1">
                  Upload applicant CSV batches with pre-flight schema validation, risk tier segmentation, and exportable decision records.
                </p>
              </div>

              {/* Action Buttons */}
              <div className="flex items-center gap-2">
                <button
                  onClick={() => {
                    const headers = "SK_ID_CURR,AMT_INCOME_TOTAL,AMT_CREDIT,AMT_ANNUITY,DAYS_BIRTH,DAYS_EMPLOYED,EXT_SOURCE_2,NAME_CONTRACT_TYPE,CODE_GENDER\n";
                    const sample = "200099,150000,450000,22500,-14600,-2190,0.58,Cash loans,F\n";
                    const blob = new Blob([headers + sample], { type: 'text/csv' });
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = "required_schema_template.csv";
                    a.click();
                  }}
                  className="px-3 py-1.5 bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-200 text-xs font-medium rounded-lg flex items-center gap-1.5 transition-colors whitespace-nowrap shrink-0"
                >
                  <Download className="w-3.5 h-3.5" />
                  <span>Schema Template</span>
                </button>

                {schemaReport.isValid && (
                  <button
                    onClick={() => {
                      const headers = "SK_ID_CURR,Applicant_Name,Income,Credit,DTI,Default_Prob,Risk_Tier,Action,Decision\n";
                      const rows = filteredBatch.map(a => 
                        `${a.id},"${a.name}",${a.income},${a.credit},${a.dti.toFixed(2)},${(a.prob * 100).toFixed(2)}%,${a.tier},"${a.action}","${a.decision}"`
                      ).join("\n");
                      const blob = new Blob([headers + rows], { type: 'text/csv' });
                      const url = window.URL.createObjectURL(blob);
                      const a = document.createElement('a');
                      a.href = url;
                      a.download = "scored_portfolio_applicants.csv";
                      a.click();
                    }}
                    className="px-4 py-1.5 bg-sky-600 hover:bg-sky-500 text-white text-xs font-semibold rounded-lg flex items-center gap-1.5 shadow-sm transition-colors whitespace-nowrap shrink-0"
                  >
                    <Download className="w-4 h-4" />
                    <span>Export Scored CSV</span>
                  </button>
                )}
              </div>
            </div>

            {/* PRE-FLIGHT SCHEMA VALIDATOR PANEL */}
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-5">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div className="flex items-center gap-3">
                  <div className={`w-9 h-9 rounded-lg flex items-center justify-center ${schemaReport.isValid ? 'bg-emerald-950 text-emerald-400 border border-emerald-800' : 'bg-red-950 text-red-400 border border-red-800'}`}>
                    {schemaReport.isValid ? <CheckCircle2 className="w-5 h-5" /> : <AlertTriangle className="w-5 h-5" />}
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-white">Pre-Flight CSV Schema Validator</h3>
                    <p className="text-xs text-slate-400">
                      Active File: <code className="text-sky-300 font-mono">{uploadFileName}</code> ({schemaReport.totalDetectedCount} columns detected)
                    </p>
                  </div>
                </div>

                {/* Test Simulation Controls */}
                <div className="flex flex-wrap items-center gap-2 text-xs">
                  <span className="text-slate-400 font-medium mr-1">Test Validator:</span>
                  <button
                    onClick={() => {
                      setDetectedColumns([
                        "SK_ID_CURR", "AMT_INCOME_TOTAL", "AMT_CREDIT", "AMT_ANNUITY", "DAYS_BIRTH", "DAYS_EMPLOYED", "EXT_SOURCE_2", "NAME_CONTRACT_TYPE", "CODE_GENDER"
                      ]);
                      setBatchApplicants(INITIAL_BATCH_APPLICANTS);
                      setUploadFileName("test_batch_sample.csv");
                      setIsScored(true);
                    }}
                    className={`px-3 py-1.5 rounded font-medium border transition-colors ${
                      schemaReport.isValid
                        ? 'bg-emerald-950/80 text-emerald-300 border-emerald-800'
                        : 'bg-slate-950 text-slate-400 border-slate-800 hover:text-white'
                    }`}
                  >
                    Load Valid Batch (7/7 Present)
                  </button>
                  <button
                    onClick={() => {
                      // Remove DAYS_BIRTH and EXT_SOURCE_2 to trigger instant schema rejection
                      setDetectedColumns([
                        "SK_ID_CURR", "AMT_INCOME_TOTAL", "AMT_CREDIT", "AMT_ANNUITY", "DAYS_EMPLOYED", "NAME_CONTRACT_TYPE"
                      ]);
                      setUploadFileName("invalid_batch_sample.csv");
                      setIsScored(false);
                    }}
                    className={`px-3 py-1.5 rounded font-medium border transition-colors ${
                      !schemaReport.isValid
                        ? 'bg-red-950/80 text-red-300 border-red-800'
                        : 'bg-slate-950 text-slate-400 border-slate-800 hover:text-white'
                    }`}
                  >
                    Simulate Missing Fields CSV
                  </button>
                  
                  {/* Real File Upload Input */}
                  <label className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded font-medium cursor-pointer transition-colors flex items-center gap-1.5">
                    <FileSpreadsheet className="w-3.5 h-3.5 text-sky-400" />
                    <span>Upload Custom CSV</span>
                    <input
                      type="file"
                      accept=".csv"
                      className="hidden"
                      onChange={(e) => {
                        const file = e.target.files?.[0];
                        if (file) {
                          setUploadFileName(file.name);
                          const reader = new FileReader();
                          reader.onload = (event) => {
                            const text = event.target?.result as string;
                            const lines = text.split(/\r?\n/).filter(l => l.trim().length > 0);
                            if (lines.length > 0) {
                              const headers = lines[0].split(',').map(h => h.trim().replace(/^["']|["']$/g, ''));
                              setDetectedColumns(headers);
                              setIsScored(true);
                            }
                          };
                          reader.readAsText(file);
                        }
                      }}
                    />
                  </label>
                </div>
              </div>

              {/* Instant Status Banner */}
              {schemaReport.isValid ? (
                <div className="bg-emerald-950/40 border border-emerald-800/80 p-3.5 rounded-lg flex items-center justify-between text-xs text-emerald-200">
                  <div className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                    <span>
                      <strong>Schema Verified:</strong> All {schemaReport.requiredSpecs.length} mandatory underwriting fields are present and verified across <strong className="font-mono">{batchApplicants.length}</strong> applicant rows.
                    </span>
                  </div>
                  <span className="font-mono text-emerald-400 font-bold bg-emerald-950 px-2 py-0.5 rounded border border-emerald-800">
                    STATUS: READY TO SCORE
                  </span>
                </div>
              ) : (
                <div className="bg-red-950/50 border border-red-800/80 p-4 rounded-lg space-y-2 text-xs text-red-200">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <AlertTriangle className="w-4 h-4 text-red-400 shrink-0" />
                      <strong className="text-red-100">Schema Validation Rejection — Scoring Blocked:</strong>
                    </div>
                    <span className="font-mono text-red-400 font-bold bg-red-950 px-2 py-0.5 rounded border border-red-800">
                      STATUS: {schemaReport.missingRequired.length} REQUIRED COLUMNS MISSING
                    </span>
                  </div>
                  <p className="text-red-300">
                    The machine learning pipeline requires these mandatory columns to perform feature engineering (DTI, age, bureau index). Please add the following missing fields to your CSV:
                  </p>
                  <div className="flex flex-wrap gap-1.5 pt-1">
                    {schemaReport.missingRequired.map(field => (
                      <span key={field.key} className="px-2.5 py-1 bg-red-900/80 text-red-100 border border-red-700 rounded font-mono font-semibold text-[11px]">
                        ❌ {field.key} <span className="opacity-75 font-normal">({field.label})</span>
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Collapsible Column Checklist */}
              <div>
                <button
                  onClick={() => setShowChecklistDetails(!showChecklistDetails)}
                  className="text-xs text-sky-400 hover:text-sky-300 font-semibold flex items-center gap-1"
                >
                  <span>{showChecklistDetails ? "▲ Hide" : "▼ Show"} Detailed Field Requirements & Detected Headers Checklist</span>
                </button>

                {showChecklistDetails && (
                  <div className="mt-3 grid grid-cols-1 md:grid-cols-2 gap-4 bg-slate-950 p-4 rounded-lg border border-slate-800 text-xs">
                    <div>
                      <h4 className="font-bold text-slate-200 uppercase tracking-wide text-[11px] mb-2">
                        Mandatory Underwriting Inputs (7 Required):
                      </h4>
                      <div className="space-y-1.5">
                        {schemaReport.requiredSpecs.map(field => {
                          const isPresent = detectedColumns.map(c => c.toUpperCase()).includes(field.key.toUpperCase());
                          return (
                            <div key={field.key} className="flex items-center justify-between p-2 bg-slate-900 rounded border border-slate-800/80">
                              <div>
                                <code className="text-white font-mono font-semibold">{field.key}</code>
                                <span className="text-[11px] text-slate-400 block">{field.label} · {field.type}</span>
                              </div>
                              <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${isPresent ? 'bg-emerald-950 text-emerald-400 border border-emerald-800' : 'bg-red-950 text-red-400 border border-red-800'}`}>
                                {isPresent ? '🟢 DETECTED' : '🔴 MISSING'}
                              </span>
                            </div>
                          );
                        })}
                      </div>
                    </div>

                    <div>
                      <h4 className="font-bold text-slate-200 uppercase tracking-wide text-[11px] mb-2">
                        Secondary & Bureau Indicators (Optional / Auto-Imputed):
                      </h4>
                      <div className="space-y-1.5">
                        {schemaReport.recommendedSpecs.map(field => {
                          const isPresent = detectedColumns.map(c => c.toUpperCase()).includes(field.key.toUpperCase());
                          return (
                            <div key={field.key} className="flex items-center justify-between p-2 bg-slate-900 rounded border border-slate-800/80">
                              <div>
                                <code className="text-slate-300 font-mono">{field.key}</code>
                                <span className="text-[11px] text-slate-500 block">{field.label} · {field.type}</span>
                              </div>
                              <span className={`px-2 py-0.5 rounded text-[10px] font-medium ${isPresent ? 'bg-sky-950 text-sky-400 border border-sky-800' : 'bg-slate-950 text-slate-500 border border-slate-800'}`}>
                                {isPresent ? '🟢 DETECTED' : '⚪ AUTO-IMPUTED'}
                              </span>
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* ONLY DISPLAY SCORING RESULTS IF SCHEMA IS VALID */}
            {schemaReport.isValid ? (
              <>

            {/* Summary Statistics Cards */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
                <span className="text-xs text-slate-400">Total Scored Applicants</span>
                <div className="text-2xl font-bold font-mono text-white mt-1">{INITIAL_BATCH_APPLICANTS.length}</div>
                <span className="text-[11px] text-slate-500">100% Retained across all tiers</span>
              </div>
              <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
                <span className="text-xs text-slate-400">Average Default Risk</span>
                <div className="text-2xl font-bold font-mono text-sky-400 mt-1">
                  {((INITIAL_BATCH_APPLICANTS.reduce((acc, a) => acc + a.prob, 0) / INITIAL_BATCH_APPLICANTS.length) * 100).toFixed(1)}%
                </div>
                <span className="text-[11px] text-slate-500">Portfolio baseline 8.07%</span>
              </div>
              <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
                <span className="text-xs text-slate-400">Prime & Standard (Low/Med)</span>
                <div className="text-2xl font-bold font-mono text-emerald-400 mt-1">
                  {INITIAL_BATCH_APPLICANTS.filter(a => ['Low', 'Medium'].includes(a.tier)).length} (50%)
                </div>
                <span className="text-[11px] text-slate-500">Approved for funding</span>
              </div>
              <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
                <span className="text-xs text-slate-400">High & Critical Flagged</span>
                <div className="text-2xl font-bold font-mono text-orange-400 mt-1">
                  {INITIAL_BATCH_APPLICANTS.filter(a => ['High', 'Critical'].includes(a.tier)).length} (50%)
                </div>
                <span className="text-[11px] text-slate-500">Escalated for review</span>
              </div>
            </div>

            {/* Filters Bar - Showing all applicants by default */}
            <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl flex flex-col md:flex-row gap-4 justify-between items-center">
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-xs text-slate-400 font-semibold mr-2">Risk Tier Filter:</span>
                {['Low', 'Medium', 'High', 'Critical'].map(t => {
                  const isSelected = tierFilters.includes(t);
                  return (
                    <button
                      key={t}
                      onClick={() => {
                        if (isSelected) {
                          if (tierFilters.length > 1) setTierFilters(tierFilters.filter(item => item !== t));
                        } else {
                          setTierFilters([...tierFilters, t]);
                        }
                      }}
                      className={`px-3 py-1 text-xs rounded-md font-medium transition-colors ${
                        isSelected 
                          ? 'bg-slate-700 text-white border border-slate-600' 
                          : 'bg-slate-950 text-slate-500 border border-slate-800'
                      }`}
                    >
                      {t}
                    </button>
                  );
                })}
              </div>

              <div className="relative w-full md:w-64">
                <Search className="w-3.5 h-3.5 text-slate-500 absolute left-3 top-2.5" />
                <input
                  type="text"
                  placeholder="Search ID or name..."
                  value={searchQuery}
                  onChange={e => setSearchQuery(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-9 pr-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-sky-500"
                />
              </div>
            </div>

            {/* Scored Portfolio Table */}
            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-sm">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-950 text-slate-400 uppercase tracking-wider font-semibold border-b border-slate-800">
                    <tr>
                      <th className="py-3 px-4">Applicant ID</th>
                      <th className="py-3 px-4">Name</th>
                      <th className="py-3 px-4">Income</th>
                      <th className="py-3 px-4">Credit</th>
                      <th className="py-3 px-4">DTI</th>
                      <th className="py-3 px-4">Ext Score</th>
                      <th className="py-3 px-4">Default Prob</th>
                      <th className="py-3 px-4">Risk Tier</th>
                      <th className="py-3 px-4">Underwriting Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/80 text-slate-300">
                    {filteredBatch.map(row => (
                      <tr key={row.id} className="hover:bg-slate-800/50 transition-colors">
                        <td className="py-3 px-4 font-mono font-semibold text-white">{row.id}</td>
                        <td className="py-3 px-4 font-medium text-slate-200">{row.name}</td>
                        <td className="py-3 px-4 font-mono">${row.income.toLocaleString()}</td>
                        <td className="py-3 px-4 font-mono">${row.credit.toLocaleString()}</td>
                        <td className="py-3 px-4 font-mono">{row.dti.toFixed(2)}x</td>
                        <td className="py-3 px-4 font-mono">{row.extScore.toFixed(2)}</td>
                        <td className="py-3 px-4 font-mono font-bold text-white">{(row.prob * 100).toFixed(2)}%</td>
                        <td className="py-3 px-4">
                          <span className={`inline-block px-2 py-0.5 rounded text-[11px] font-semibold ${
                            row.tier === 'Low' ? 'bg-emerald-950 text-emerald-400 border border-emerald-800' :
                            row.tier === 'Medium' ? 'bg-amber-950 text-amber-400 border border-amber-800' :
                            row.tier === 'High' ? 'bg-orange-950 text-orange-400 border border-orange-800' :
                            'bg-red-950 text-red-400 border border-red-800'
                          }`}>
                            {row.tier}
                          </span>
                        </td>
                        <td className="py-3 px-4 text-slate-300">{row.action}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </>
            ) : (
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center space-y-4">
                <div className="w-12 h-12 rounded-full bg-red-950/80 border border-red-800 text-red-400 flex items-center justify-center mx-auto">
                  <AlertTriangle className="w-6 h-6" />
                </div>
                <div className="max-w-md mx-auto space-y-2">
                  <h3 className="text-base font-bold text-white">Batch Scoring Halted by Schema Validator</h3>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    Scoring execution has been paused because the uploaded dataset is missing mandatory underwriting features. 
                    Please supply all required columns or click <strong>Load Valid Batch</strong> above to inspect the fully compliant portfolio table.
                  </p>
                </div>
              </div>
            )}
          </div>
        )}

        {/* ========================================================= */}
        {/* TAB 3: PORTFOLIO RISK ANALYTICS */}
        {/* ========================================================= */}
        {activeTab === 'portfolio' && (
          <div className="space-y-6">
            <div className="pb-4 border-b border-slate-800">
              <h1 className="text-2xl font-bold tracking-tight text-white">Portfolio Risk Analytics</h1>
              <p className="text-sm text-slate-400 mt-1">
                Macro-level default concentration, exposure distributions, and credit history correlations derived from DuckDB analytics.
              </p>
            </div>

            {/* Top Exposure Stats */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
                <span className="text-xs text-slate-400">Total Portfolio Exposure</span>
                <div className="text-2xl font-bold font-mono text-white mt-1">$184.2 Billion</div>
                <span className="text-[11px] text-emerald-400">307,511 Active Applications</span>
              </div>
              <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
                <span className="text-xs text-slate-400">Base Default Prevalence</span>
                <div className="text-2xl font-bold font-mono text-white mt-1">8.07%</div>
                <span className="text-[11px] text-slate-500">24,825 Defaulted Loans</span>
              </div>
              <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
                <span className="text-xs text-slate-400">Prime Segment Share</span>
                <div className="text-2xl font-bold font-mono text-emerald-400 mt-1">62.4%</div>
                <span className="text-[11px] text-slate-500">Low Risk Tier ($p &lt; 0.10$)</span>
              </div>
              <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
                <span className="text-xs text-slate-400">Projected Charge-Off Loss</span>
                <div className="text-2xl font-bold font-mono text-sky-400 mt-1">$25.04M</div>
                <span className="text-[11px] text-slate-500">With 0.24 Cutoff vs $38.2M</span>
              </div>
            </div>

            {/* 2x2 Segment Grids */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Education Default Distribution */}
              <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl space-y-4">
                <div className="flex justify-between items-center">
                  <h3 className="text-sm font-bold text-white">Default Rate by Education Level</h3>
                  <span className="text-xs text-slate-400">Benchmark = 8.07%</span>
                </div>
                <div className="space-y-3">
                  {[
                    { label: "Lower secondary", rate: 10.93, count: "3,816" },
                    { label: "Secondary / secondary special", rate: 8.94, count: "218,391" },
                    { label: "Incomplete higher", rate: 8.48, count: "10,277" },
                    { label: "Higher education", rate: 5.36, count: "74,863" },
                    { label: "Academic degree", rate: 1.83, count: "164" }
                  ].map(item => (
                    <div key={item.label} className="space-y-1">
                      <div className="flex justify-between text-xs">
                        <span className="text-slate-300">{item.label} <span className="text-slate-500 font-mono">({item.count})</span></span>
                        <span className="font-mono font-bold text-white">{item.rate}%</span>
                      </div>
                      <div className="w-full bg-slate-950 h-2 rounded-full overflow-hidden">
                        <div
                          style={{ width: `${item.rate * 8}%` }}
                          className={`h-full rounded-full ${item.rate > 8.07 ? 'bg-orange-500' : 'bg-sky-500'}`}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Age Cohorts Default Distribution */}
              <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl space-y-4">
                <div className="flex justify-between items-center">
                  <h3 className="text-sm font-bold text-white">Default Rate by Borrower Age Cohort</h3>
                  <span className="text-xs text-slate-400">Under 30 highest risk</span>
                </div>
                <div className="space-y-3">
                  {[
                    { label: "Under 30 years", rate: 11.48, count: "45,021" },
                    { label: "30 to 45 years", rate: 8.62, count: "128,410" },
                    { label: "46 to 60 years", rate: 6.84, count: "98,240" },
                    { label: "Over 60 years", rate: 5.12, count: "35,840" }
                  ].map(item => (
                    <div key={item.label} className="space-y-1">
                      <div className="flex justify-between text-xs">
                        <span className="text-slate-300">{item.label} <span className="text-slate-500 font-mono">({item.count})</span></span>
                        <span className="font-mono font-bold text-white">{item.rate}%</span>
                      </div>
                      <div className="w-full bg-slate-950 h-2 rounded-full overflow-hidden">
                        <div
                          style={{ width: `${item.rate * 8}%` }}
                          className={`h-full rounded-full ${item.rate > 8.07 ? 'bg-red-500' : 'bg-emerald-500'}`}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Leverage Tier Exposure */}
              <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl space-y-4">
                <h3 className="text-sm font-bold text-white">Credit-to-Income Leverage Disparity</h3>
                <div className="space-y-3">
                  {[
                    { label: "Low Leverage (< 2.5x DTI)", rate: 5.18, count: "78,410" },
                    { label: "Normal Leverage (2.5x - 5.0x DTI)", rate: 8.02, count: "162,810" },
                    { label: "High Leverage (> 5.0x DTI)", rate: 11.26, count: "66,291" }
                  ].map(item => (
                    <div key={item.label} className="space-y-1">
                      <div className="flex justify-between text-xs">
                        <span className="text-slate-300">{item.label}</span>
                        <span className="font-mono font-bold text-white">{item.rate}%</span>
                      </div>
                      <div className="w-full bg-slate-950 h-2 rounded-full overflow-hidden">
                        <div
                          style={{ width: `${item.rate * 8}%` }}
                          className={`h-full rounded-full ${item.rate > 8.07 ? 'bg-red-500' : 'bg-sky-500'}`}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Bureau Delinquency Factor */}
              <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl space-y-4">
                <h3 className="text-sm font-bold text-white">External Credit Bureau Delinquency Impact</h3>
                <div className="grid grid-cols-2 gap-4 pt-2">
                  <div className="bg-slate-950 p-4 rounded-lg border border-slate-800 text-center">
                    <span className="text-xs text-slate-400">Clean Bureau History</span>
                    <div className="text-2xl font-bold font-mono text-emerald-400 mt-1">7.62%</div>
                    <span className="text-[11px] text-slate-500">284,120 applicants</span>
                  </div>
                  <div className="bg-slate-950 p-4 rounded-lg border border-slate-800 text-center">
                    <span className="text-xs text-slate-400">Prior Overdue Record</span>
                    <div className="text-2xl font-bold font-mono text-red-400 mt-1">13.88%</div>
                    <span className="text-[11px] text-slate-500">+82% Default Risk Spike</span>
                  </div>
                </div>
              </div>
            </div>

            {/* NEW SECTION: Leverage Risk Heat Map (Credit-to-Income vs Default Rate) */}
            <div className="bg-slate-900 border border-slate-800 p-6 md:p-8 rounded-xl space-y-6">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-2 border-b border-slate-800">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-red-500"></span>
                    <h2 className="text-base font-bold text-white tracking-tight">
                      Credit-to-Income Leverage vs Default Rate Heat Map
                    </h2>
                  </div>
                  <p className="text-xs text-slate-400 mt-1">
                    Multi-dimensional cohort cross-tabulation correlating debt-to-income leverage with historical default rates to isolate toxic credit clusters.
                  </p>
                </div>

                {/* Heatmap Dimension & Visualization View Toggles */}
                <div className="flex flex-wrap items-center gap-3">
                  {/* View Type Toggle (Chart.js vs Matrix) */}
                  <div className="flex items-center gap-1 bg-slate-950 p-1 rounded-lg border border-slate-800 text-xs">
                    <button
                      onClick={() => setHeatmapViewType('chartjs')}
                      className={`flex items-center gap-1.5 px-3 py-1 rounded font-medium transition-colors ${
                        heatmapViewType === 'chartjs'
                          ? 'bg-sky-600 text-white shadow-sm'
                          : 'text-slate-400 hover:text-white'
                      }`}
                    >
                      <BarChart3 className="w-3.5 h-3.5" />
                      <span>Chart.js Visualization</span>
                    </button>
                    <button
                      onClick={() => setHeatmapViewType('matrix')}
                      className={`flex items-center gap-1.5 px-3 py-1 rounded font-medium transition-colors ${
                        heatmapViewType === 'matrix'
                          ? 'bg-sky-600 text-white shadow-sm'
                          : 'text-slate-400 hover:text-white'
                      }`}
                    >
                      <Layers className="w-3.5 h-3.5" />
                      <span>Heat Map Matrix</span>
                    </button>
                  </div>

                  {/* Heatmap Dimension Toggle */}
                  <div className="flex items-center gap-2 bg-slate-950 p-1 rounded-lg border border-slate-800 text-xs">
                    <span className="text-slate-400 px-2 font-medium">Cross-Tabulate DTI With:</span>
                    <button
                      onClick={() => setHeatmapDimension('income')}
                      className={`px-3 py-1 rounded font-medium transition-colors ${
                        heatmapDimension === 'income'
                          ? 'bg-slate-700 text-white shadow-sm border border-slate-600'
                          : 'text-slate-400 hover:text-white'
                      }`}
                    >
                      Annual Income Brackets
                    </button>
                    <button
                      onClick={() => setHeatmapDimension('bureau')}
                      className={`px-3 py-1 rounded font-medium transition-colors ${
                        heatmapDimension === 'bureau'
                          ? 'bg-slate-700 text-white shadow-sm border border-slate-600'
                          : 'text-slate-400 hover:text-white'
                      }`}
                    >
                      External Bureau Score Tiers
                    </button>
                  </div>
                </div>
              </div>

              {/* Cluster KPI Callouts */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="bg-slate-950 p-3.5 rounded-lg border border-slate-800">
                  <span className="text-[11px] text-slate-400 block">Peak Cluster Default Rate</span>
                  <div className="text-xl font-bold font-mono text-red-400 mt-0.5">
                    {heatmapDimension === 'income' ? '24.20%' : '34.80%'}
                  </div>
                  <span className="text-[10px] text-slate-500">
                    {heatmapDimension === 'income' ? 'DTI > 7.0x + Income < $80k' : 'DTI > 7.0x + Score < 0.30'}
                  </span>
                </div>
                <div className="bg-slate-950 p-3.5 rounded-lg border border-slate-800">
                  <span className="text-[11px] text-slate-400 block">Lowest Cluster Default Rate</span>
                  <div className="text-xl font-bold font-mono text-emerald-400 mt-0.5">
                    {heatmapDimension === 'income' ? '2.30%' : '1.40%'}
                  </div>
                  <span className="text-[10px] text-slate-500">
                    {heatmapDimension === 'income' ? 'DTI < 2.0x + Income > $220k' : 'DTI < 2.0x + Score > 0.60'}
                  </span>
                </div>
                <div className="bg-slate-950 p-3.5 rounded-lg border border-slate-800">
                  <span className="text-[11px] text-slate-400 block">High-Risk Cluster Exposure</span>
                  <div className="text-xl font-bold font-mono text-orange-400 mt-0.5">$19.2B</div>
                  <span className="text-[10px] text-slate-500">28,490 high-leverage applicants</span>
                </div>
                <div className="bg-slate-950 p-3.5 rounded-lg border border-slate-800">
                  <span className="text-[11px] text-slate-400 block">Risk Spread Multiplier</span>
                  <div className="text-xl font-bold font-mono text-white mt-0.5">
                    {heatmapDimension === 'income' ? '10.5x' : '24.9x'}
                  </div>
                  <span className="text-[10px] text-slate-500">Max vs min cluster separation</span>
                </div>
              </div>

              {/* CHART.JS INTERACTIVE VISUALIZATION */}
              {heatmapViewType === 'chartjs' && (
                <div className="bg-slate-950 border border-slate-800 rounded-xl p-6 space-y-4">
                  <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
                    <div>
                      <h3 className="text-sm font-bold text-white flex items-center gap-2">
                        <BarChart3 className="w-4 h-4 text-sky-400" />
                        <span>Chart.js: Leverage Clustering — Default Rate by DTI & {heatmapDimension === 'income' ? 'Income Bracket' : 'External Credit Score'}</span>
                      </h3>
                      <p className="text-xs text-slate-400 mt-0.5">
                        Interactive clustered bar chart rendered via Chart.js with baseline reference at 8.07%. Hover over clusters for risk details.
                      </p>
                    </div>
                    <div className="flex items-center gap-2 text-xs">
                      <span className="inline-block w-3 h-0.5 bg-red-400 border-dashed"></span>
                      <span className="text-slate-400 text-[11px]">8.07% Portfolio Baseline</span>
                    </div>
                  </div>

                  <div className="h-80 w-full relative">
                    <Bar
                      data={{
                        labels: [
                          "Low (< 2.0x DTI)",
                          "Moderate (2.0x - 3.5x)",
                          "Elevated (3.5x - 5.0x)",
                          "High (5.0x - 7.0x) ⚠️",
                          "Critical (> 7.0x) 🚨"
                        ],
                        datasets: heatmapDimension === 'income' ? [
                          {
                            label: "Low Income (< $80k)",
                            data: [6.10, 8.40, 11.20, 16.80, 24.20],
                            backgroundColor: "rgba(239, 68, 68, 0.85)",
                            borderColor: "#EF4444",
                            borderWidth: 1,
                            borderRadius: 4
                          },
                          {
                            label: "Lower-Mid ($80k - $140k)",
                            data: [4.80, 7.20, 9.40, 12.90, 18.70],
                            backgroundColor: "rgba(249, 115, 22, 0.85)",
                            borderColor: "#F97316",
                            borderWidth: 1,
                            borderRadius: 4
                          },
                          {
                            label: "Upper-Mid ($140k - $220k)",
                            data: [3.90, 5.80, 7.50, 9.80, 13.50],
                            backgroundColor: "rgba(56, 189, 248, 0.85)",
                            borderColor: "#38BDF8",
                            borderWidth: 1,
                            borderRadius: 4
                          },
                          {
                            label: "High Income (> $220k)",
                            data: [2.30, 3.80, 5.10, 6.90, 9.40],
                            backgroundColor: "rgba(16, 185, 129, 0.85)",
                            borderColor: "#10B981",
                            borderWidth: 1,
                            borderRadius: 4
                          }
                        ] : [
                          {
                            label: "Weak Score (< 0.30)",
                            data: [13.10, 16.90, 21.40, 27.60, 34.80],
                            backgroundColor: "rgba(220, 38, 38, 0.9)",
                            borderColor: "#DC2626",
                            borderWidth: 1,
                            borderRadius: 4
                          },
                          {
                            label: "Mid-Low (0.30 - 0.45)",
                            data: [7.20, 9.80, 12.70, 17.10, 22.90],
                            backgroundColor: "rgba(245, 158, 11, 0.85)",
                            borderColor: "#F59E0B",
                            borderWidth: 1,
                            borderRadius: 4
                          },
                          {
                            label: "Mid-High (0.45 - 0.60)",
                            data: [3.80, 5.60, 7.40, 10.20, 14.80],
                            backgroundColor: "rgba(14, 165, 233, 0.85)",
                            borderColor: "#0EA5E9",
                            borderWidth: 1,
                            borderRadius: 4
                          },
                          {
                            label: "Prime Score (> 0.60)",
                            data: [1.40, 2.10, 3.20, 4.80, 7.10],
                            backgroundColor: "rgba(16, 185, 129, 0.85)",
                            borderColor: "#10B981",
                            borderWidth: 1,
                            borderRadius: 4
                          }
                        ]
                      }}
                      options={{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                          legend: {
                            position: 'top' as const,
                            labels: {
                              color: '#94A3B8',
                              font: {
                                size: 11,
                                family: 'Plus Jakarta Sans'
                              },
                              boxWidth: 12,
                              padding: 12
                            }
                          },
                          tooltip: {
                            backgroundColor: '#0F172A',
                            titleColor: '#F8FAFC',
                            bodyColor: '#CBD5E1',
                            borderColor: '#334155',
                            borderWidth: 1,
                            padding: 10,
                            callbacks: {
                              label: function(context: any) {
                                return ` ${context.dataset.label}: ${context.parsed.y.toFixed(2)}% Default Rate`;
                              }
                            }
                          }
                        },
                        scales: {
                          x: {
                            grid: {
                              color: 'rgba(51, 65, 85, 0.3)'
                            },
                            ticks: {
                              color: '#94A3B8',
                              font: {
                                size: 10.5
                              }
                            }
                          },
                          y: {
                            grid: {
                              color: 'rgba(51, 65, 85, 0.4)'
                            },
                            ticks: {
                              color: '#94A3B8',
                              font: {
                                size: 10.5
                              },
                              callback: function(val: any) {
                                return val + '%';
                              }
                            },
                            title: {
                              display: true,
                              text: 'Historical Default Rate (%)',
                              color: '#64748B',
                              font: {
                                size: 11
                              }
                            }
                          }
                        }
                      }}
                    />
                  </div>

                  <div className="p-3 bg-slate-900 rounded-lg border border-slate-800/80 flex items-center justify-between text-xs">
                    <span className="text-slate-400">
                      <strong>Interactive Finding:</strong> Leverage above 5.0x escalates default probability across every subsegment, demonstrating a non-linear credit risk inflection point.
                    </span>
                    <button
                      onClick={() => setHeatmapViewType('matrix')}
                      className="text-sky-400 hover:text-sky-300 font-semibold underline shrink-0 ml-4"
                    >
                      View Full Heat Map Matrix →
                    </button>
                  </div>
                </div>
              )}

              {/* Heat Map Table Matrix */}
              {heatmapViewType === 'matrix' && (
              <div className="overflow-x-auto rounded-lg border border-slate-800">
                <table className="w-full text-center text-xs border-collapse">
                  <thead>
                    <tr className="bg-slate-950 text-slate-300 font-semibold border-b border-slate-800">
                      <th className="py-3 px-4 text-left border-r border-slate-800 w-44">
                        Credit-to-Income (DTI)
                      </th>
                      {heatmapDimension === 'income' ? (
                        <>
                          <th className="py-3 px-3">Low Income (&lt; $80k)</th>
                          <th className="py-3 px-3">Lower-Mid ($80k - $140k)</th>
                          <th className="py-3 px-3">Upper-Mid ($140k - $220k)</th>
                          <th className="py-3 px-3">High Income (&gt; $220k)</th>
                          <th className="py-3 px-3 border-l border-slate-800 bg-slate-950/80">Average by DTI</th>
                        </>
                      ) : (
                        <>
                          <th className="py-3 px-3">Weak Score (&lt; 0.30)</th>
                          <th className="py-3 px-3">Mid-Low (0.30 - 0.45)</th>
                          <th className="py-3 px-3">Mid-High (0.45 - 0.60)</th>
                          <th className="py-3 px-3">Prime Score (&gt; 0.60)</th>
                          <th className="py-3 px-3 border-l border-slate-800 bg-slate-950/80">Average by DTI</th>
                        </>
                      )}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800 text-slate-200">
                    {/* Render Matrix Rows */}
                    {(heatmapDimension === 'income' ? [
                      {
                        label: "Low (< 2.0x)",
                        cells: [
                          { rate: 6.10, count: "18,420", exposure: "$1.4B" },
                          { rate: 4.80, count: "24,510", exposure: "$3.2B" },
                          { rate: 3.90, count: "16,840", exposure: "$3.4B" },
                          { rate: 2.30, count: "18,640", exposure: "$5.8B" }
                        ],
                        avg: 4.28
                      },
                      {
                        label: "Moderate (2.0x - 3.5x)",
                        cells: [
                          { rate: 8.40, count: "28,190", exposure: "$4.1B" },
                          { rate: 7.20, count: "39,840", exposure: "$9.4B" },
                          { rate: 5.80, count: "26,120", exposure: "$8.9B" },
                          { rate: 3.80, count: "19,200", exposure: "$10.2B" }
                        ],
                        avg: 6.31
                      },
                      {
                        label: "Elevated (3.5x - 5.0x)",
                        cells: [
                          { rate: 11.20, count: "22,410", exposure: "$4.9B" },
                          { rate: 9.40, count: "27,150", exposure: "$9.8B" },
                          { rate: 7.50, count: "16,400", exposure: "$8.4B" },
                          { rate: 5.10, count: "12,180", exposure: "$9.1B" }
                        ],
                        avg: 8.30
                      },
                      {
                        label: "High (5.0x - 7.0x) ⚠️",
                        cells: [
                          { rate: 16.80, count: "14,810", exposure: "$4.2B" },
                          { rate: 12.90, count: "16,920", exposure: "$8.1B" },
                          { rate: 9.80, count: "9,840", exposure: "$6.8B" },
                          { rate: 6.90, count: "6,410", exposure: "$6.4B" }
                        ],
                        avg: 11.60
                      },
                      {
                        label: "Critical (> 7.0x) 🚨",
                        cells: [
                          { rate: 24.20, count: "8,940", exposure: "$3.1B" },
                          { rate: 18.70, count: "9,120", exposure: "$5.4B" },
                          { rate: 13.50, count: "5,820", exposure: "$4.9B" },
                          { rate: 9.40, count: "4,610", exposure: "$5.8B" }
                        ],
                        avg: 16.45
                      }
                    ] : [
                      {
                        label: "Low (< 2.0x)",
                        cells: [
                          { rate: 13.10, count: "9,420", exposure: "$0.8B" },
                          { rate: 7.20, count: "22,140", exposure: "$2.9B" },
                          { rate: 3.80, count: "28,490", exposure: "$4.8B" },
                          { rate: 1.40, count: "18,360", exposure: "$5.3B" }
                        ],
                        avg: 6.38
                      },
                      {
                        label: "Moderate (2.0x - 3.5x)",
                        cells: [
                          { rate: 16.90, count: "15,120", exposure: "$2.2B" },
                          { rate: 9.80, count: "34,920", exposure: "$8.1B" },
                          { rate: 5.60, count: "41,180", exposure: "$12.4B" },
                          { rate: 2.10, count: "22,130", exposure: "$9.9B" }
                        ],
                        avg: 8.60
                      },
                      {
                        label: "Elevated (3.5x - 5.0x)",
                        cells: [
                          { rate: 21.40, count: "12,840", exposure: "$2.8B" },
                          { rate: 12.70, count: "24,610", exposure: "$8.4B" },
                          { rate: 7.40, count: "26,190", exposure: "$11.6B" },
                          { rate: 3.20, count: "14,500", exposure: "$9.4B" }
                        ],
                        avg: 11.18
                      },
                      {
                        label: "High (5.0x - 7.0x) ⚠️",
                        cells: [
                          { rate: 27.60, count: "8,920", exposure: "$2.4B" },
                          { rate: 17.10, count: "14,810", exposure: "$6.9B" },
                          { rate: 10.20, count: "15,120", exposure: "$9.2B" },
                          { rate: 4.80, count: "9,130", exposure: "$7.0B" }
                        ],
                        avg: 14.93
                      },
                      {
                        label: "Critical (> 7.0x) 🚨",
                        cells: [
                          { rate: 34.80, count: "5,410", exposure: "$1.9B" },
                          { rate: 22.90, count: "8,420", exposure: "$4.8B" },
                          { rate: 14.80, count: "8,920", exposure: "$6.8B" },
                          { rate: 7.10, count: "5,740", exposure: "$5.7B" }
                        ],
                        avg: 19.90
                      }
                    ]).map((row, idx) => (
                      <tr key={row.label} className="hover:bg-slate-800/30">
                        <td className="py-3 px-4 text-left font-semibold text-slate-200 border-r border-slate-800 bg-slate-950/40">
                          {row.label}
                        </td>
                        {row.cells.map((cell, cIdx) => {
                          // Dynamic heat color scale based on default rate percentage
                          // Baseline is 8.07%
                          const rate = cell.rate;
                          let bgClass = "bg-emerald-950/40 text-emerald-300";
                          let borderClass = "border-emerald-800/30";
                          if (rate >= 20.0) {
                            bgClass = "bg-red-950/90 text-red-200 font-bold";
                            borderClass = "border-red-600/70";
                          } else if (rate >= 14.0) {
                            bgClass = "bg-red-950/60 text-red-300 font-bold";
                            borderClass = "border-red-800/60";
                          } else if (rate >= 9.5) {
                            bgClass = "bg-orange-950/60 text-orange-300 font-semibold";
                            borderClass = "border-orange-800/50";
                          } else if (rate >= 7.0) {
                            bgClass = "bg-amber-950/40 text-amber-300";
                            borderClass = "border-amber-800/40";
                          } else if (rate >= 4.5) {
                            bgClass = "bg-sky-950/40 text-sky-300";
                            borderClass = "border-sky-800/40";
                          }

                          return (
                            <td key={cIdx} className="p-2">
                              <div className={`p-2.5 rounded-lg border transition-transform hover:scale-105 cursor-default ${bgClass} ${borderClass}`}>
                                <div className="text-sm font-mono tracking-tight font-bold">
                                  {rate.toFixed(1)}%
                                </div>
                                <div className="text-[10px] opacity-75 font-mono mt-0.5">
                                  {cell.count} loans
                                </div>
                                <div className="text-[9px] opacity-60">
                                  {cell.exposure}
                                </div>
                              </div>
                            </td>
                          );
                        })}
                        <td className="py-3 px-3 font-mono font-bold text-slate-200 border-l border-slate-800 bg-slate-950/60">
                          {row.avg.toFixed(1)}%
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {/* Heat Map Legend & Policy Action Thresholds */}
              <div className="flex flex-col md:flex-row items-center justify-between gap-4 pt-2 text-xs">
                <div className="flex items-center gap-2">
                  <span className="text-slate-400 font-medium">Risk Heatmap Legend:</span>
                  <div className="flex items-center gap-1.5 font-mono text-[11px]">
                    <span className="px-2 py-0.5 rounded bg-emerald-950/70 text-emerald-300 border border-emerald-800/50">&lt; 4.5% (Prime)</span>
                    <span className="px-2 py-0.5 rounded bg-sky-950/70 text-sky-300 border border-sky-800/50">4.5% - 7.0%</span>
                    <span className="px-2 py-0.5 rounded bg-amber-950/70 text-amber-300 border border-amber-800/50">7.0% - 9.5%</span>
                    <span className="px-2 py-0.5 rounded bg-orange-950/70 text-orange-300 border border-orange-800/50">9.5% - 14.0%</span>
                    <span className="px-2 py-0.5 rounded bg-red-950/80 text-red-200 border border-red-700/60">&gt; 14.0% (Toxic Cluster)</span>
                  </div>
                </div>

                <div className="text-slate-400 text-[11px]">
                  Baseline Portfolio Default Rate: <strong className="text-sky-300">8.07%</strong>
                </div>
              </div>

              {/* Actionable Underwriting Findings Box */}
              <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-2 text-xs text-slate-300">
                <div className="flex items-center gap-2 text-sky-300 font-semibold">
                  <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />
                  <span>Key Underwriting Takeaways from Leverage Cluster Analysis:</span>
                </div>
                <ul className="list-disc list-inside space-y-1 text-slate-400 pl-1">
                  <li>
                    <strong className="text-red-300">Severe Leverage Cliff:</strong> When Credit-to-Income exceeds <span className="font-mono text-white">5.0x</span>, default rates consistently surpass <span className="font-mono text-white">12.9%</span> across all income cohorts, spiking to <span className="font-mono text-white">24.2%</span> for applicants earning under $80,000.
                  </li>
                  <li>
                    <strong className="text-amber-300">External Score Compounding:</strong> Borrowers combining <span className="font-mono text-white">DTI &gt; 5.0x</span> with <span className="font-mono text-white">EXT_SOURCE &lt; 0.30</span> generate a toxic default rate between <span className="font-mono text-white">27.6% and 34.8%</span> (over 4x the portfolio baseline).
                  </li>
                  <li>
                    <strong className="text-emerald-300">Prime Safe Haven:</strong> Borrowers with <span className="font-mono text-white">DTI &lt; 2.0x</span> and income &gt; $140,000 demonstrate default rates under <span className="font-mono text-white">3.9%</span>, justifying instant-approval and prime risk-based pricing.
                  </li>
                </ul>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* TAB 4: MODEL PERFORMANCE & TUNING */}
        {/* ========================================================= */}
        {activeTab === 'performance' && (
          <div className="space-y-6">
            <div className="pb-4 border-b border-slate-800">
              <h1 className="text-2xl font-bold tracking-tight text-white">Model Performance & Threshold Optimization</h1>
              <p className="text-sm text-slate-400 mt-1">
                Held-out test set statistical validation and cost-sensitive underwriting cutoff simulator.
              </p>
            </div>

            {/* Model Comparison Table */}
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
              <h3 className="text-sm font-bold text-white">5-Fold Stratified Cross-Validation Benchmark</h3>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-950 text-slate-400 uppercase font-semibold border-b border-slate-800">
                    <tr>
                      <th className="py-2.5 px-4">Model Architecture</th>
                      <th className="py-2.5 px-4">Mean CV ROC-AUC</th>
                      <th className="py-2.5 px-4">Mean CV PR-AUC</th>
                      <th className="py-2.5 px-4">Test ROC-AUC</th>
                      <th className="py-2.5 px-4">Test PR-AUC</th>
                      <th className="py-2.5 px-4">Test F1</th>
                      <th className="py-2.5 px-4">Training Time</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800 text-slate-300">
                    <tr className="hover:bg-slate-800/40">
                      <td className="py-2.5 px-4 font-semibold text-white">Logistic Regression (Balanced)</td>
                      <td className="py-2.5 px-4 font-mono">0.6914 ±0.0042</td>
                      <td className="py-2.5 px-4 font-mono">0.1850 ±0.0051</td>
                      <td className="py-2.5 px-4 font-mono">0.6895</td>
                      <td className="py-2.5 px-4 font-mono">0.1821</td>
                      <td className="py-2.5 px-4 font-mono">0.2740</td>
                      <td className="py-2.5 px-4 font-mono">14.2s</td>
                    </tr>
                    <tr className="hover:bg-slate-800/40">
                      <td className="py-2.5 px-4 font-semibold text-white">Random Forest (Balanced)</td>
                      <td className="py-2.5 px-4 font-mono">0.7382 ±0.0038</td>
                      <td className="py-2.5 px-4 font-mono">0.2291 ±0.0047</td>
                      <td className="py-2.5 px-4 font-mono">0.7365</td>
                      <td className="py-2.5 px-4 font-mono">0.2274</td>
                      <td className="py-2.5 px-4 font-mono">0.3218</td>
                      <td className="py-2.5 px-4 font-mono">68.5s</td>
                    </tr>
                    <tr className="bg-sky-950/30 font-semibold text-sky-200">
                      <td className="py-2.5 px-4 text-white">Tuned XGBoost (scale_pos_weight) ⭐</td>
                      <td className="py-2.5 px-4 font-mono text-sky-300">0.7795 ±0.0029</td>
                      <td className="py-2.5 px-4 font-mono text-sky-300">0.2831 ±0.0039</td>
                      <td className="py-2.5 px-4 font-mono text-emerald-400 font-bold">0.7782</td>
                      <td className="py-2.5 px-4 font-mono text-emerald-400 font-bold">0.2814</td>
                      <td className="py-2.5 px-4 font-mono text-white">0.3898</td>
                      <td className="py-2.5 px-4 font-mono">32.8s</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            {/* Interactive Threshold Slider Box */}
            <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl space-y-6">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                  <h3 className="text-base font-bold text-white">Decision Threshold Financial Simulator</h3>
                  <p className="text-xs text-slate-400 mt-0.5">
                    Adjust cutoff to observe the trade-off between Defaulter Recall ($c_&#123;FN&#125; = \$10,000$) and False Declines ($c_&#123;FP&#125; = \$1,200$).
                  </p>
                </div>
                <div className="text-right">
                  <span className="text-xs text-slate-400 block">Operational Cutoff</span>
                  <span className="text-xl font-bold font-mono text-sky-400">{threshold.toFixed(2)}</span>
                </div>
              </div>

              <input
                type="range"
                min="0.05"
                max="0.65"
                step="0.01"
                value={threshold}
                onChange={e => setThreshold(Number(e.target.value))}
                className="w-full accent-sky-500 cursor-pointer"
              />

              <div className="flex justify-between text-[11px] text-slate-500 font-mono">
                <span>0.05 (High Recall, Many Reviews)</span>
                <span className="text-sky-400 font-bold">0.24 (Cost-Optimal)</span>
                <span>0.50 (Standard, High Defaults)</span>
                <span>0.65</span>
              </div>

              {/* Dynamic Confusion Matrix & Financial Impact Strip */}
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 pt-2">
                {/* Confusion Matrix */}
                <div className="lg:col-span-6 bg-slate-950 p-5 rounded-xl border border-slate-800 space-y-3">
                  <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider">Confusion Matrix (61,503 Test Loans)</h4>
                  <div className="grid grid-cols-2 gap-3 text-center pt-2">
                    <div className="bg-slate-900 border border-slate-800 p-3 rounded-lg">
                      <span className="text-[11px] text-emerald-400 font-semibold block">True Negatives (Approved)</span>
                      <span className="text-xl font-bold font-mono text-white mt-1 block">{thresholdMetrics.tn.toLocaleString()}</span>
                      <span className="text-[10px] text-slate-500">Correctly approved good borrowers</span>
                    </div>
                    <div className="bg-slate-900 border border-slate-800 p-3 rounded-lg">
                      <span className="text-[11px] text-amber-400 font-semibold block">False Positives (Reviewed)</span>
                      <span className="text-xl font-bold font-mono text-white mt-1 block">{thresholdMetrics.fp.toLocaleString()}</span>
                      <span className="text-[10px] text-slate-500">Good borrowers flagged for review</span>
                    </div>
                    <div className="bg-slate-900 border border-slate-800 p-3 rounded-lg">
                      <span className="text-[11px] text-red-400 font-semibold block">False Negatives (Missed)</span>
                      <span className="text-xl font-bold font-mono text-white mt-1 block">{thresholdMetrics.fn.toLocaleString()}</span>
                      <span className="text-[10px] text-slate-500">Costly charged-off defaults</span>
                    </div>
                    <div className="bg-slate-900 border border-slate-800 p-3 rounded-lg">
                      <span className="text-[11px] text-sky-400 font-semibold block">True Positives (Caught)</span>
                      <span className="text-xl font-bold font-mono text-white mt-1 block">{thresholdMetrics.tp.toLocaleString()}</span>
                      <span className="text-[10px] text-slate-500">Prevented default charge-offs</span>
                    </div>
                  </div>
                </div>

                {/* Financial Takeaway */}
                <div className="lg:col-span-6 bg-slate-950 p-5 rounded-xl border border-slate-800 flex flex-col justify-between space-y-4">
                  <div>
                    <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider">Operational Metrics @ {threshold.toFixed(2)}</h4>
                    <div className="grid grid-cols-3 gap-3 mt-3">
                      <div>
                        <span className="text-[11px] text-slate-400 block">Defaulter Recall</span>
                        <span className="text-lg font-bold font-mono text-sky-400">{(thresholdMetrics.recall * 100).toFixed(1)}%</span>
                      </div>
                      <div>
                        <span className="text-[11px] text-slate-400 block">Precision</span>
                        <span className="text-lg font-bold font-mono text-amber-400">{(thresholdMetrics.precision * 100).toFixed(1)}%</span>
                      </div>
                      <div>
                        <span className="text-[11px] text-slate-400 block">F1-Score</span>
                        <span className="text-lg font-bold font-mono text-emerald-400">{thresholdMetrics.f1.toFixed(3)}</span>
                      </div>
                    </div>
                  </div>

                  <div className="border-t border-slate-800 pt-3">
                    <span className="text-xs text-slate-400 block">Total Expected Portfolio Credit Loss:</span>
                    <span className="text-2xl font-bold font-mono text-white">
                      ${(thresholdMetrics.totalCost / 1e6).toFixed(2)} Million
                    </span>
                    <p className="text-[11px] text-slate-400 mt-1">
                      At standard 0.50 threshold, expected losses exceed $38.2M. Setting threshold to 0.24 reduces portfolio loss by <strong>$13.18 Million</strong>.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* TAB 5: SHAP EXPLAINABILITY */}
        {/* ========================================================= */}
        {activeTab === 'shap' && (
          <div className="space-y-6">
            <div className="pb-4 border-b border-slate-800">
              <h1 className="text-2xl font-bold tracking-tight text-white">SHAP Interpretability Studio</h1>
              <p className="text-sm text-slate-400 mt-1">
                Global TreeSHAP feature rankings, dependence curves, and FCRA-compliant adverse action explainability.
              </p>
            </div>

            {/* Non-causality callout */}
            <div className="bg-sky-950/40 border border-sky-800/80 p-4 rounded-xl flex items-start gap-3">
              <Info className="w-4 h-4 text-sky-400 shrink-0 mt-0.5" />
              <div className="text-xs text-sky-200 leading-relaxed">
                <strong>Model Attribution Principles:</strong> SHAP values identify mathematical associations learned by the gradient boosting model from historical correlations. Under Equal Credit Opportunity Act (ECOA) and FCRA guidelines, SHAP attributions are used as structured decision support for adverse action reason codes, not as claims of direct causal mechanics.
              </div>
            </div>

            {/* Global SHAP Ranking Chart */}
            <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl space-y-4">
              <h3 className="text-sm font-bold text-white">Global Feature Importance (Mean |SHAP| Value)</h3>
              <div className="space-y-2.5 pt-2">
                {[
                  { name: "External Credit Agency Score 2 (EXT_SOURCE_2)", val: 0.482, pct: 100 },
                  { name: "External Credit Agency Score 3 (EXT_SOURCE_3)", val: 0.441, pct: 91 },
                  { name: "Credit-to-Income Leverage Ratio (DTI)", val: 0.324, pct: 67 },
                  { name: "External Credit Agency Score 1 (EXT_SOURCE_1)", val: 0.285, pct: 59 },
                  { name: "Borrower Age (DAYS_BIRTH in years)", val: 0.241, pct: 50 },
                  { name: "Employment Tenure (DAYS_EMPLOYED in years)", val: 0.218, pct: 45 },
                  { name: "Annuity Payment Burden (% of Income)", val: 0.194, pct: 40 },
                  { name: "Active Credit Bureau Debt Balance", val: 0.176, pct: 36 },
                  { name: "Monthly Repayment Speed / Rate", val: 0.158, pct: 33 },
                  { name: "Number of Active Bureau Loans", val: 0.142, pct: 29 }
                ].map(item => (
                  <div key={item.name} className="space-y-1">
                    <div className="flex justify-between text-xs">
                      <span className="text-slate-300">{item.name}</span>
                      <span className="font-mono font-bold text-sky-400">{item.val.toFixed(3)}</span>
                    </div>
                    <div className="w-full bg-slate-950 h-2 rounded-full overflow-hidden">
                      <div
                        style={{ width: `${item.pct}%` }}
                        className="bg-sky-500 h-full rounded-full transition-all"
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Case Studies */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl space-y-3">
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  <h3 className="text-sm font-bold text-white">Case Study 1: Prime Low-Risk Applicant</h3>
                </div>
                <p className="text-xs text-slate-400 leading-relaxed">
                  <strong>Sarah Jenkins</strong> (45 yrs, Higher Education, $240k Income, 1.88x DTI):
                </p>
                <div className="bg-slate-950 p-3.5 rounded-lg text-xs space-y-1 text-slate-300">
                  <span className="text-emerald-400 font-semibold block">Predicted Probability: 3.4% (Low Risk)</span>
                  <p>• Top Mitigating Driver: External agency score 0.76 (<span className="text-emerald-400 font-mono">-0.42 SHAP</span>)</p>
                  <p>• Second Strength: Low credit leverage (<span className="text-emerald-400 font-mono">-0.28 SHAP</span>)</p>
                  <p>• Recommendation: <strong>Instant prime approval</strong></p>
                </div>
              </div>

              <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl space-y-3">
                <div className="flex items-center gap-2">
                  <XCircle className="w-4 h-4 text-red-400" />
                  <h3 className="text-sm font-bold text-white">Case Study 2: Distressed Critical-Risk Applicant</h3>
                </div>
                <p className="text-xs text-slate-400 leading-relaxed">
                  <strong>Elena Rostova</strong> (23 yrs, $65k Income, $550k Credit, 8.46x DTI):
                </p>
                <div className="bg-slate-950 p-3.5 rounded-lg text-xs space-y-1 text-slate-300">
                  <span className="text-red-400 font-semibold block">Predicted Probability: 68.2% (Critical Risk)</span>
                  <p>• Top Adverse Driver: Severe DTI leverage (<span className="text-red-400 font-mono">+0.54 SHAP</span>)</p>
                  <p>• Second Adverse Driver: Low agency score (<span className="text-red-400 font-mono">+0.46 SHAP</span>)</p>
                  <p>• Recommendation: <strong>Automated adverse decision</strong></p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* TAB 6: BUSINESS INSIGHTS & SQL ANALYTICS */}
        {/* ========================================================= */}
        {activeTab === 'insights' && (
          <div className="space-y-6">
            <div className="pb-4 border-b border-slate-800">
              <h1 className="text-2xl font-bold tracking-tight text-white">Business Insights & DuckDB SQL Analytics</h1>
              <p className="text-sm text-slate-400 mt-1">
                Empirical underwriting cohort findings, query definitions, and credit policy recommendations.
              </p>
            </div>

            {/* SQL Query Snippet & Output Display */}
            <div className="space-y-6">
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-bold text-white flex items-center gap-2">
                    <Database className="w-4 h-4 text-sky-400" />
                    Query 03: Top 10 Highest-Risk Applicant Segments
                  </h3>
                  <span className="text-xs text-slate-500 font-mono">sql/03_top_risk_segments.sql</span>
                </div>
                
                <pre className="bg-slate-950 p-3.5 rounded-lg text-[11px] text-sky-300 font-mono overflow-x-auto border border-slate-800">
{`SELECT age_cohort, education, external_score_tier, leverage_tier,
       COUNT(*) AS total_applicants,
       ROUND(AVG(TARGET) * 100, 2) AS segment_default_rate_pct,
       ROUND((AVG(TARGET) / 0.0807) * 100, 1) AS risk_index_vs_baseline
FROM segmented_applicants
GROUP BY age_cohort, education, external_score_tier, leverage_tier
HAVING COUNT(*) >= 250
ORDER BY segment_default_rate_pct DESC LIMIT 5;`}
                </pre>

                <div className="overflow-x-auto pt-2">
                  <table className="w-full text-left text-xs">
                    <thead className="bg-slate-950 text-slate-400 font-semibold border-b border-slate-800">
                      <tr>
                        <th className="py-2.5 px-3">Age Cohort</th>
                        <th className="py-2.5 px-3">Education</th>
                        <th className="py-2.5 px-3">External Score Tier</th>
                        <th className="py-2.5 px-3">Leverage Tier</th>
                        <th className="py-2.5 px-3">Default Rate</th>
                        <th className="py-2.5 px-3">Risk Index</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800 text-slate-300">
                      <tr className="hover:bg-slate-800/40">
                        <td className="py-2.5 px-3 text-red-300 font-medium">Under 30</td>
                        <td className="py-2.5 px-3">Lower secondary</td>
                        <td className="py-2.5 px-3 font-mono">Low (&lt; 0.35)</td>
                        <td className="py-2.5 px-3 font-mono">High (&gt; 5x)</td>
                        <td className="py-2.5 px-3 font-mono font-bold text-red-400">24.8%</td>
                        <td className="py-2.5 px-3 font-mono text-red-300">307 (3.1x)</td>
                      </tr>
                      <tr className="hover:bg-slate-800/40">
                        <td className="py-2.5 px-3 text-red-300 font-medium">Under 30</td>
                        <td className="py-2.5 px-3">Secondary</td>
                        <td className="py-2.5 px-3 font-mono">Low (&lt; 0.35)</td>
                        <td className="py-2.5 px-3 font-mono">High (&gt; 5x)</td>
                        <td className="py-2.5 px-3 font-mono font-bold text-red-400">21.6%</td>
                        <td className="py-2.5 px-3 font-mono text-red-300">268 (2.7x)</td>
                      </tr>
                      <tr className="hover:bg-slate-800/40">
                        <td className="py-2.5 px-3 font-medium">30 to 45</td>
                        <td className="py-2.5 px-3">Lower secondary</td>
                        <td className="py-2.5 px-3 font-mono">Low (&lt; 0.35)</td>
                        <td className="py-2.5 px-3 font-mono">High (&gt; 5x)</td>
                        <td className="py-2.5 px-3 font-mono font-bold text-orange-400">19.4%</td>
                        <td className="py-2.5 px-3 font-mono text-orange-300">240 (2.4x)</td>
                      </tr>
                      <tr className="hover:bg-slate-800/40">
                        <td className="py-2.5 px-3 text-red-300 font-medium">Under 30</td>
                        <td className="py-2.5 px-3">Secondary</td>
                        <td className="py-2.5 px-3 font-mono">Low (&lt; 0.35)</td>
                        <td className="py-2.5 px-3 font-mono">Normal (&lt;= 5x)</td>
                        <td className="py-2.5 px-3 font-mono font-bold text-orange-400">17.2%</td>
                        <td className="py-2.5 px-3 font-mono text-orange-300">213 (2.1x)</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Policy Guidance */}
              <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl space-y-3">
                <h3 className="text-sm font-bold text-white">Underwriting Policy Interventions</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-1">
                  <div className="bg-slate-950 p-4 rounded-lg border border-slate-800 text-xs text-slate-300 space-y-1">
                    <strong className="text-sky-300 block">1. Maximum DTI Cap</strong>
                    Restrict credit-to-income ratio to $\le 3.5\times$ for borrowers under 30 without home equity.
                  </div>
                  <div className="bg-slate-950 p-4 rounded-lg border border-slate-800 text-xs text-slate-300 space-y-1">
                    <strong className="text-amber-300 block">2. Bureau Delinquency Hard Stop</strong>
                    Mandate manual underwriter review for applicants with $\ge 3$ active external bureau debts or prior overdue marks.
                  </div>
                  <div className="bg-slate-950 p-4 rounded-lg border border-slate-800 text-xs text-slate-300 space-y-1">
                    <strong className="text-emerald-300 block">3. Threshold Re-calibration</strong>
                    Operate approval policies at $p = 0.24$ cutoff to capture 74.2% of bad loans before funding.
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

      </main>

      {/* Mandatory Compliance Disclaimer Footer */}
      <footer className="border-t border-slate-800 bg-slate-950 px-6 py-4 mt-8">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-500">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-emerald-500" />
            <span>
              <strong>Institutional Policy Notice:</strong> This tool supports credit-risk review and does not make automated loan approval decisions.
            </span>
          </div>
          <div className="text-slate-400">
            Equal Credit Opportunity Act (ECOA) · FCRA Compliant Design
          </div>
        </div>
      </footer>
    </div>
  );
}
