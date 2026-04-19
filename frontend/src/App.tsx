import React, { useState } from 'react';
import { Upload, FileText, Download, ShieldCheck, Zap, BarChart3 } from 'lucide-react';


const API_BASE = "https://your-python-api.koyeb.app";

export default function App() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/scan`, { method: "POST", body: formData });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      alert("Connection to AI Engine failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen p-8 flex flex-col items-center">
      {/* Header */}
      <header className="text-center mb-12">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-emerald-400 bg-clip-text text-transparent">
          AI Text Detector
        </h1>
        <p className="text-slate-400 mt-2">Forensic Linguistic Analysis using Perplexity & Burstiness</p>
      </header>

      <main className="w-full max-w-2xl">
        {/* Dropzone */}
        <div className={`border-2 border-dashed rounded-2xl p-12 text-center transition-all ${file ? 'border-emerald-500 bg-emerald-500/5' : 'border-slate-700 hover:border-blue-500 bg-slate-800/50'}`}>
          <input 
            type="file" 
            id="fileInput" 
            className="hidden" 
            onChange={(e) => setFile(e.target.files?.[0] || null)} 
          />
          <label htmlFor="fileInput" className="cursor-pointer flex flex-col items-center">
            <Upload className={`w-12 h-12 mb-4 ${file ? 'text-emerald-400' : 'text-slate-500'}`} />
            <span className="text-lg font-medium">
              {file ? file.name : "Drop an image or document here"}
            </span>
            <span className="text-sm text-slate-500 mt-1">Supports JPG, PNG, TXT</span>
          </label>
        </div>

        <button 
          onClick={handleUpload}
          disabled={!file || loading}
          className="w-full mt-6 py-4 rounded-xl bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 font-bold transition-all shadow-lg shadow-blue-900/20 flex justify-center items-center gap-2"
        >
          {loading ? <Zap className="animate-spin" /> : <ShieldCheck />}
          {loading ? "Analyzing Patterns..." : "Verify Content Authenticity"}
        </button>

        {/* Results Dashboard */}
        {result && (
          <div className="mt-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="bg-slate-800 border border-slate-700 rounded-2xl p-6 overflow-hidden relative">
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h3 className="text-slate-400 uppercase text-xs font-bold tracking-widest">Analysis Result</h3>
                  <p className="text-3xl font-bold">{(result.score * 100).toFixed(1)}% Likely AI</p>
                </div>
                <BarChart3 className="text-blue-400 w-8 h-8" />
              </div>

              <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="bg-slate-900/50 p-4 rounded-lg">
                  <span className="text-xs text-slate-500 block">Perplexity</span>
                  <span className="text-xl font-mono text-emerald-400">{result.perplexity}</span>
                </div>
                <div className="bg-slate-900/50 p-4 rounded-lg">
                  <span className="text-xs text-slate-500 block">Burstiness</span>
                  <span className="text-xl font-mono text-emerald-400">{result.burstiness}</span>
                </div>
              </div>

              <a 
                href={`${API_BASE}/report/${result.id}`}
                className="flex items-center justify-center gap-2 w-full py-3 bg-slate-700 hover:bg-slate-600 rounded-lg transition-colors text-sm font-semibold"
              >
                <Download size={18} />
                Download PDF Audit Report
              </a>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
