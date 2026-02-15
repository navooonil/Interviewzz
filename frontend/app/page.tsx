"use client"

import { useState } from "react"
import AudioRecorder from "@/components/AudioRecorder"
import AnalysisView from "@/components/AnalysisView"

export default function Home() {
  const [analysisData, setAnalysisData] = useState<any>(null)

  return (
    <main className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-8 bg-grid-pattern bg-dot-grid">
      <div className="w-full max-w-4xl space-y-12">
        <div className="text-center space-y-4">
          <h1 className="text-5xl font-extrabold tracking-tight text-gray-900 bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
            Interview Analyzer
          </h1>
          <p className="text-xl text-gray-500 max-w-2xl mx-auto">
            Practice your interview answers and get instant AI feedback on your speaking pace, filler words, and confidence.
          </p>
        </div>

        {!analysisData ? (
          <AudioRecorder onTranscriptionComplete={setAnalysisData} />
        ) : (
          <div className="animate-in fade-in zoom-in duration-500">
            <AnalysisView data={analysisData} />
            <div className="text-center mt-8">
              <button 
                onClick={() => setAnalysisData(null)}
                className="text-indigo-600 hover:text-indigo-800 font-medium underline underline-offset-4"
              >
                Start Over
              </button>
            </div>
          </div>
        )}
      </div>
    </main>
  )
}
