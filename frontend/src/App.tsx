import React, { useState } from 'react';


interface ScanResult {
  text: string;
  aiScore: number;
  isAI: boolean;
}

const App: React.FC = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [token, setToken] = useState<string | null>(null);
  const [result, setResult] = useState<ScanResult | null>(null);
  const [loading, setLoading] = useState(false);

  
  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    setToken("demo_token_123"); 
    alert(isLogin ? "Logged in successfully!" : "Account created!");
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files?.[0]) return;
    setLoading(true);
    
    
    setTimeout(() => {
      setResult({
        text: "The quick brown fox jumped over...",
        aiScore: 0.89,
        isAI: true
      });
      setLoading(false);
    }, 1500);
  };

  
  if (!token) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center p-4">
        <div className="bg-white p-8 rounded-2xl shadow-2xl w-full max-w-md">
          <h1 className="text-3xl font-black text-slate-800 mb-2">{isLogin ? "Welcome" : "Join Us"}</h1>
          <p className="text-slate-500 mb-8">AI Text & OCR Detector Pro</p>
          
          <form onSubmit={handleAuth} className="space-y-4">
            <input type="text" placeholder="Username" className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" required />
            <input type="password" placeholder="Password" className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" required />
            <button className="w-full bg-blue-600 text-white py-3 rounded-lg font-bold hover:bg-blue-700 transition">
              {isLogin ? "Sign In" : "Create Account"}
            </button>
          </form>
          
          <button onClick={() => setIsLogin(!isLogin)} className="w-full mt-4 text-sm text-blue-600 font-medium">
            {isLogin ? "Need an account? Sign Up" : "Already have an account? Login"}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <header className="max-w-5xl mx-auto flex justify-between items-center mb-12">
        <h2 className="text-2xl font-bold text-slate-800 underline decoration-blue-500">AI.Shield</h2>
        <button onClick={() => setToken(null)} className="text-red-500 font-medium">Logout</button>
      </header>

      <main className="max-w-5xl mx-auto grid md:grid-cols-2 gap-8">
        {/* Upload Card */}
        <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100">
          <h3 className="text-xl font-bold mb-4">Analyze Document</h3>
          <div className="border-2 border-dashed border-gray-200 rounded-xl p-10 text-center hover:border-blue-400 transition cursor-pointer">
            <input type="file" onChange={handleFileUpload} className="hidden" id="fileInput" />
            <label htmlFor="fileInput" className="cursor-pointer text-blue-600 font-bold">
              Click to upload Image for OCR
            </label>
            <p className="text-xs text-gray-400 mt-2">Supports JPG, PNG</p>
          </div>
        </div>

        {/* Result Card */}
        <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 min-h-[300px]">
          <h3 className="text-xl font-bold mb-4">Detection Result</h3>
          {loading ? (
            <div className="animate-pulse flex space-y-4 flex-col">
              <div className="h-4 bg-gray-200 rounded w-3/4"></div>
              <div className="h-12 bg-gray-200 rounded"></div>
            </div>
          ) : result ? (
            <div>
              <div className={`text-5xl font-black mb-2 ${result.isAI ? 'text-red-500' : 'text-green-500'}`}>
                {(result.aiScore * 100).toFixed(0)}%
              </div>
              <p className="font-bold text-slate-700 mb-4">{result.isAI ? 'Likely AI Generated' : 'Likely Human Written'}</p>
              <div className="p-4 bg-gray-50 rounded-lg text-sm text-gray-600 italic">
                "{result.text}"
              </div>
              <button className="mt-6 w-full py-2 border-2 border-blue-600 text-blue-600 rounded-lg font-bold hover:bg-blue-50 transition">
                Generate PDF Report
              </button>
            </div>
          ) : (
            <p className="text-gray-400">Scan a document to see the magic.</p>
          )}
        </div>
      </main>
    </div>
  );
};

export default App;
