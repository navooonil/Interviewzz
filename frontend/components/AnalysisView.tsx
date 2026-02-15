import { AlertTriangle, CheckCircle2, FileText, Mic, TrendingUp, Zap, HeartPulse, Lightbulb, ArrowRight } from "lucide-react"

export default function AnalysisView({ data }: { data: any }) {
  if (!data || !data.analysis) return null

  const {
    speaking_rate_wpm,
    pause_analysis,
    filler_words
  } = data.analysis
  
  const semantic = data.semantic || {}
  const stability = data.emotional_stability || {}
  
  // Quick Frontend Calculation of Session Score (Mirroring Backend Logic for display)
  // Ideally this comes from the backend, but we compute it here for immediate feedback on the view.
  const scoreRelevance = (semantic.overall_relevance || 0) * 100
  const scoreStability = (stability.overall_emotional_stability_score || 0) * 100
  const wpm = speaking_rate_wpm || 0
  let scorePace = 100
  if (wpm < 120) scorePace = Math.max(0, 100 - (120 - wpm) * 2)
  if (wpm > 160) scorePace = Math.max(0, 100 - (wpm - 160) * 2)
  
  const score = Math.round(
      (scoreRelevance * 0.4) + 
      (scoreStability * 0.3) + 
      (scorePace * 0.15) + 
      (100 * 0.15) // Assuming clarity is perfect for this quick display
  )

  const totalPauses = pause_analysis.count
  const totalDuration = pause_analysis.total_duration

  return (
    <div className="w-full max-w-4xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-8 duration-700">
      
      {/* Header */}
      <div className="text-center space-y-4">
        <div>
            <h2 className="text-4xl font-extrabold text-indigo-900 tracking-tight">Analysis Results</h2>
            <p className="text-gray-500 text-lg">AI-powered insights on your interview performance</p>
        </div>
        
        {/* Main Score Badge */}
        <div className="inline-flex items-center gap-4 bg-gray-900 text-white px-6 py-3 rounded-full shadow-xl">
            <span className="text-sm font-semibold uppercase tracking-wider text-gray-400">Session Score</span>
            <div className="h-8 w-px bg-gray-700"></div>
            <span className={`text-3xl font-black ${
                score >= 80 ? 'text-green-400' : 
                score >= 60 ? 'text-yellow-400' : 'text-red-400'
            }`}>{score}</span>
            <span className="text-xs text-gray-500">/ 100</span>
        </div>
      </div>
      
      {/* AI Insights Section - NEW */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Strengths */}
          <div className="bg-green-50/50 p-6 rounded-2xl border border-green-100">
              <h3 className="text-lg font-bold text-green-800 mb-4 flex items-center gap-2">
                  <CheckCircle2 className="w-5 h-5" />
                  Key Strengths
              </h3>
              <ul className="space-y-3">
                  {score >= 80 && (
                      <li className="flex gap-3 text-sm text-green-900 bg-white p-3 rounded-lg border border-green-100 shadow-sm">
                          <span className="text-green-500">Only top performers hit 80+. You are in the top tier!</span>
                      </li>
                  )}
                  {wpm >= 120 && wpm <= 160 && (
                      <li className="flex gap-3 text-sm text-green-900 bg-white p-3 rounded-lg border border-green-100 shadow-sm">
                         Your speaking pace ({wpm} WPM) is perfect for listener retention.
                      </li>
                  )}
                  {filler_words.total_count < 5 && (
                      <li className="flex gap-3 text-sm text-green-900 bg-white p-3 rounded-lg border border-green-100 shadow-sm">
                          Excellent clarity. Very few filler words used.
                      </li>
                  )}
                  {(semantic.overall_relevance || 0) > 0.8 && (
                      <li className="flex gap-3 text-sm text-green-900 bg-white p-3 rounded-lg border border-green-100 shadow-sm">
                          Strong semantic match. Your answer aligned well with your resume.
                      </li>
                  )}
                  {(stability.overall_emotional_stability_score || 0) > 0.8 && (
                      <li className="flex gap-3 text-sm text-green-900 bg-white p-3 rounded-lg border border-green-100 shadow-sm">
                          You sounded confident and emotionally stable throughout.
                      </li>
                  )}
              </ul>
          </div>

          {/* Actionable Feedback */}
          <div className="bg-indigo-50/50 p-6 rounded-2xl border border-indigo-100">
              <h3 className="text-lg font-bold text-indigo-800 mb-4 flex items-center gap-2">
                  <Lightbulb className="w-5 h-5" />
                  Areas for Improvement
              </h3>
              <ul className="space-y-3">
                  {wpm > 165 && (
                       <li className="bg-white p-3 rounded-lg border border-indigo-100 shadow-sm">
                           <span className="block text-indigo-900 font-semibold text-sm mb-1">Slow Down</span>
                           <p className="text-indigo-700 text-xs">You are speaking too fast ({wpm} WPM). Aim for 140 WPM to give the interviewer time to process.</p>
                       </li>
                  )}
                  {wpm < 110 && (
                       <li className="bg-white p-3 rounded-lg border border-indigo-100 shadow-sm">
                           <span className="block text-indigo-900 font-semibold text-sm mb-1">Increase Energy</span>
                           <p className="text-indigo-700 text-xs">Your pace is a bit slow. Try to speak with more urgency to show enthusiasm.</p>
                       </li>
                  )}
                  {filler_words.total_count >= 5 && (
                       <li className="bg-white p-3 rounded-lg border border-indigo-100 shadow-sm">
                           <span className="block text-indigo-900 font-semibold text-sm mb-1">Reduce Fillers</span>
                           <p className="text-indigo-700 text-xs">You used {filler_words.total_count} filler words. Pause silently instead of saying "um".</p>
                       </li>
                  )}
                  {(semantic.overall_relevance || 0) < 0.6 && (
                       <li className="bg-white p-3 rounded-lg border border-indigo-100 shadow-sm">
                           <span className="block text-indigo-900 font-semibold text-sm mb-1">Check Relevance</span>
                           <p className="text-indigo-700 text-xs">Your answer drifted from your resume. Try to explicitly mention your key projects.</p>
                       </li>
                  )}
                   {(stability.overall_emotional_stability_score || 0) < 0.65 && (
                       <li className="bg-white p-3 rounded-lg border border-indigo-100 shadow-sm">
                           <span className="block text-indigo-900 font-semibold text-sm mb-1">Work on Confidence</span>
                           <p className="text-indigo-700 text-xs">Your voice variance suggests hesitation. Practice speaking with steady volume.</p>
                       </li>
                  )}
              </ul>
          </div>
      </div>

      {/* Top Level Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        
        {/* Semantic Relevance */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-indigo-100 hover:shadow-lg transition-all duration-300 relative overflow-hidden group">
            <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                <FileText className="w-24 h-24 text-indigo-600" />
            </div>
            <div className="relative z-10">
                <span className="text-xs font-bold text-indigo-500 uppercase tracking-widest">Relevance</span>
                <div className="mt-2 flex items-baseline gap-2">
                    <span className="text-5xl font-black text-indigo-600">
                        {Math.round((semantic.overall_relevance || 0) * 100)}%
                    </span>
                </div>
                <p className="text-sm text-gray-500 mt-2">Resume Match</p>
                
                <div className="w-full bg-indigo-50 h-2 rounded-full mt-4 overflow-hidden">
                    <div 
                        className="bg-indigo-600 h-full rounded-full transition-all duration-1000" 
                        style={{ width: `${(semantic.overall_relevance || 0) * 100}%` }}
                    />
                </div>
            </div>
        </div>

        {/* Emotional Stability - NEW */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-pink-100 hover:shadow-lg transition-all duration-300 relative overflow-hidden group">
            <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                <HeartPulse className="w-24 h-24 text-pink-600" />
            </div>
            <div className="relative z-10">
                <span className="text-xs font-bold text-pink-500 uppercase tracking-widest">Confidence</span>
                <div className="mt-2 flex items-baseline gap-2">
                    <span className="text-5xl font-black text-pink-600">
                        {Math.round((stability.overall_emotional_stability_score || 0) * 100)}%
                    </span>
                </div>
                <p className="text-sm text-gray-500 mt-2">Vocal Stability</p>
                
                <div className="w-full bg-pink-50 h-2 rounded-full mt-4 overflow-hidden">
                    <div 
                        className="bg-pink-600 h-full rounded-full transition-all duration-1000" 
                        style={{ width: `${(stability.overall_emotional_stability_score || 0) * 100}%` }}
                    />
                </div>
            </div>
        </div>

        {/* Speaking Rate */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-blue-100 hover:shadow-lg transition-all duration-300 relative overflow-hidden group">
             <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                <Mic className="w-24 h-24 text-blue-600" />
            </div>
            <div className="relative z-10">
                <span className="text-xs font-bold text-blue-500 uppercase tracking-widest">Pace</span>
                <div className="mt-2 flex items-baseline gap-2">
                    <span className="text-4xl font-bold text-gray-900">{speaking_rate_wpm}</span>
                    <span className="text-sm text-gray-500">WPM</span>
                </div>
                <p className="text-sm text-gray-500 mt-2">Target: 120-150 WPM</p>
                
                 <div className="w-full bg-blue-50 h-2 rounded-full mt-4 overflow-hidden">
                    <div 
                        className="bg-blue-500 h-full rounded-full transition-all duration-1000" 
                        style={{ width: `${Math.min(speaking_rate_wpm / 200 * 100, 100)}%` }} 
                    />
                </div>
            </div>
        </div>

        {/* Fillers */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-orange-100 hover:shadow-lg transition-all duration-300 relative overflow-hidden group">
            <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                <AlertTriangle className="w-24 h-24 text-orange-600" />
            </div>
             <div className="relative z-10">
                <span className="text-xs font-bold text-orange-500 uppercase tracking-widest">Clarity</span>
                <div className="mt-2 flex items-baseline gap-2">
                    <span className="text-4xl font-bold text-orange-600">{filler_words.total_count}</span>
                    <span className="text-sm text-gray-500">Fillers</span>
                </div>
                 <div className="flex gap-1 mt-3 flex-wrap">
                    {Object.entries(filler_words.breakdown).map(([word, count]) => (
                        <span key={word} className="px-2 py-0.5 bg-orange-50 text-orange-700 text-[10px] font-medium rounded-full border border-orange-100">
                            {word}
                        </span>
                    ))}
                </div>
            </div>
        </div>
      </div>

      {/* Semantic Timeline / Chunks */}
      {semantic.chunk_analysis && semantic.chunk_analysis.length > 0 && (
          <div className="space-y-4">
              <h3 className="text-xl font-bold text-gray-800 flex items-center gap-2">
                  <TrendingUp className="w-5 h-5 text-indigo-600" />
                  Answer Timeline & Relevance
              </h3>
              
              <div className="grid gap-4">
                  {semantic.chunk_analysis.map((chunk: any, i: number) => (
                      <div key={i} className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm hover:border-indigo-200 transition-colors flex gap-4">
                          {/* Time Indicator */}
                          <div className="flex flex-col items-center min-w-[80px]">
                              <span className="text-xs font-mono text-gray-400 bg-gray-50 px-2 py-1 rounded">
                                  {chunk.timestamp}
                              </span>
                              <div className="h-full w-0.5 bg-gray-100 my-2"></div>
                          </div>
                          
                          {/* Content */}
                          <div className="flex-1 space-y-3">
                              <p className="text-gray-800 text-sm leading-relaxed">
                                  "{chunk.text}"
                              </p>
                              
                              {/* Insights Row */}
                              <div className="flex flex-wrap gap-3 items-center pt-2 border-t border-gray-50">
                                  {/* Relevance Badge */}
                                  <div className={`flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium border ${
                                      chunk.relevance_score > 0.7 ? 'bg-green-50 text-green-700 border-green-100' : 
                                      chunk.relevance_score > 0.4 ? 'bg-yellow-50 text-yellow-700 border-yellow-100' :
                                      'bg-gray-50 text-gray-600 border-gray-200'
                                  }`}>
                                      <CheckCircle2 className="w-3 h-3" />
                                      Relevance: {Math.round(chunk.relevance_score * 100)}%
                                  </div>

                                  {/* Drift Warning */}
                                  {chunk.coherence_with_prev < 0.5 && (
                                     <div className="flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-red-50 text-red-700 border border-red-100">
                                          <TrendingUp className="w-3 h-3 rotate-180" />
                                          Topic Drift Detected
                                      </div> 
                                  )}
                                  
                                  {/* Redundancy Warning */}
                                  {chunk.max_redundancy_score > 0.85 && (
                                      <div className="flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-orange-50 text-orange-700 border border-orange-100">
                                          <Zap className="w-3 h-3" />
                                          Repetitive Point
                                      </div>
                                  )}
                              </div>
                              
                              {/* Matched Resume Section */}
                              <div className="bg-indigo-50/50 p-3 rounded-lg border border-indigo-50 text-xs">
                                  <span className="font-semibold text-indigo-700 block mb-1">Aligned with Resume:</span>
                                  <p className="text-gray-600 italic truncate">
                                      {chunk.matched_resume_section}
                                  </p>
                              </div>
                          </div>
                      </div>
                  ))}
              </div>
          </div>
      )}

      {/* Full Transcript (Collapsed/Secondary) */}
      <div className="bg-gray-50 p-6 rounded-2xl border border-gray-200">
         <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-4">Full Transcript</h3>
         <p className="text-gray-600 text-sm leading-relaxed whitespace-pre-wrap">
            {data.transcription.full_text}
         </p>
      </div>

    </div>
  )
}
