"use client"

import React, { useState, useRef } from "react"
import { UploadCloud, Mic, Square, Loader2, Play, FileAudio } from "lucide-react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

interface AudioRecorderProps {
  onTranscriptionComplete: (data: any) => void
}


const DUMMY_DATA = {
  "transcription": {
    "full_text": "I believe I am a great fit for this role because I have over 5 years of experience in Python development. I started my career as a junior developer at TechCorp, where I optimized backend APIs. Um, then I moved to start-up land, which was, uh, very chaotic but I learned a lot about scaling systems. I think my leadership skills are also strong.",
    "segments": []
  },
  "analysis": {
    "speaking_rate_wpm": 142.5,
    "pause_analysis": {
      "count": 4,
      "total_duration": 2.8,
      "details": [{ "duration": 0.8 }, { "duration": 1.2 }, { "duration": 0.5 }, { "duration": 0.3 }]
    },
    "filler_words": {
      "total_count": 3,
      "breakdown": { "um": 1, "uh": 1, "like": 0, "you know": 0 }
    }
  },
  "emotional_stability": {
    "overall_emotional_stability_score": 0.88,
    "metrics": {
      "average_pitch_stability": 0.85,
      "average_energy_stability": 0.91
    }
  },
  "semantic": {
    "overall_relevance": 0.92,
    "chunk_analysis": [
      {
        "timestamp": "0s - 15s",
        "text": "I believe I am a great fit for this role because I have over 5 years of experience in Python development.",
        "relevance_score": 0.95,
        "matched_resume_section": "Experience: Senior Python Developer (5+ Years)",
        "coherence_with_prev": 1.0,
        "max_redundancy_score": 0.0
      },
      {
        "timestamp": "15s - 30s",
        "text": "I started my career as a junior developer at TechCorp, where I optimized backend APIs.",
        "relevance_score": 0.89,
        "matched_resume_section": "History: Jr. Dev at TechCorp - API Optimization",
        "coherence_with_prev": 0.92,
        "max_redundancy_score": 0.1
      },
      {
         "timestamp": "30s - 45s",
         "text": "Um, then I moved to start-up land, which was, uh, very chaotic but I learned a lot about scaling systems.",
         "relevance_score": 0.78,
         "matched_resume_section": "Skills: System Scaling, High Load Architecture",
         "coherence_with_prev": 0.85, 
         "max_redundancy_score": 0.05
      }
    ]
  }
}

export default function AudioRecorder({ onTranscriptionComplete }: AudioRecorderProps) {
  const [isRecording, setIsRecording] = useState(false)
  const [audioUrl, setAudioUrl] = useState<string | null>(null)
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null)
  const [resumeText, setResumeText] = useState("")
  const [isUploading, setIsUploading] = useState(false)
  
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const chunksRef = useRef<Blob[]>([])

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      mediaRecorderRef.current = new MediaRecorder(stream)
      chunksRef.current = []

      mediaRecorderRef.current.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data)
        }
      }

      mediaRecorderRef.current.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: "audio/wav" })
        const url = URL.createObjectURL(blob)
        setAudioUrl(url)
        setAudioBlob(blob)
      }

      mediaRecorderRef.current.start()
      setIsRecording(true)
    } catch (err) {
      console.error("Error accessing microphone:", err)
      alert("Microphone access denied or not available.")
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
      // Stop all tracks
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop())
    }
  }

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      const url = URL.createObjectURL(file)
      setAudioUrl(url)
      setAudioBlob(file)
    }
  }

  const handleSubmit = async () => {
    if (!audioBlob) return

    setIsUploading(true)
    const formData = new FormData()
    // Append file with specific name for backend
    formData.append("file", audioBlob, "recording.wav")

    try {
      const response = await fetch("http://127.0.0.1:8000/api/v1/transcription/transcribe", {
        method: "POST",
        body: formData,
      })

      if (!response.ok) {
        throw new Error("Upload failed")
      }

      const transcriptionData = await response.json()
      
      // Step 2: Semantic Analysis
      // We chained this request to the analysis endpoint
      const analysisResponse = await fetch("http://127.0.0.1:8000/api/v1/analysis/relevance", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
              transcript: transcriptionData,
              resume_text: resumeText
          })
      })

      if (!analysisResponse.ok) {
           throw new Error("Semantic analysis failed")
      }

      const analysisData = await analysisResponse.json()
      
      // Merge datasets
      onTranscriptionComplete({
          transcription: transcriptionData,
          analysis: transcriptionData.analysis, // speech analysis metrics
          emotional_stability: transcriptionData.emotional_stability, // NEW: audio analysis metrics
          semantic: analysisData // semantic data
      })
    } catch (error) {
      console.error("Error uploading file:", error)
      alert("Failed to analyze audio. Please ensure backend is running.")
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div className="w-full max-w-md mx-auto p-6 bg-white rounded-xl shadow-lg border border-gray-100">
      <h2 className="text-xl font-bold mb-4 text-center text-gray-800">Record Your Answer</h2>
      
      <div className="flex flex-col items-center gap-6">
        
        {/* Resume Input - New Section */}
        <div className="w-full space-y-2">
            <label className="text-sm font-medium text-gray-700">Paste your Resume / Job Description</label>
            <textarea
                className="w-full p-3 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 outline-none resize-none h-32"
                placeholder="Paste the text here to check relevance..."
                value={resumeText}
                onChange={(e) => setResumeText(e.target.value)}
            />
        </div>
        
        <div className="w-full border-t border-gray-100 my-2"></div>
        {/* Recording Visualizer Placeholder */}
        <div className={cn(
          "w-32 h-32 rounded-full flex items-center justify-center transition-all duration-300",
          isRecording ? "bg-red-50 animate-pulse ring-4 ring-red-100" : "bg-blue-50"
        )}>
          {isRecording ? (
             <div className="w-16 h-16 bg-red-500 rounded flex items-center justify-center animate-bounce">
                <span className="text-white font-bold text-xs">REC</span>
             </div>
          ) : (
            <Mic className="w-12 h-12 text-blue-500" />
          )}
        </div>

        {/* Controls */}
        <div className="flex gap-4 w-full justify-center">
          {!isRecording ? (
        <div className="flex flex-col gap-3 w-full">
            <Button 
              onClick={startRecording} 
              className="w-full py-6 text-lg bg-indigo-600 hover:bg-indigo-700 shadow-lg shadow-indigo-200"
            >
              <Mic className="mr-2 h-5 w-5" /> Start Recording
            </Button>
            
            <Button 
                variant="ghost" 
                size="sm"
                onClick={() => onTranscriptionComplete(DUMMY_DATA)}
                className="text-xs text-gray-400 hover:text-indigo-600 hover:bg-indigo-50"
            >
                Try Demo Data (No Mic Required)
            </Button>
        </div>
      ) : (
            <Button 
              onClick={stopRecording} 
              variant="danger"
              className="w-full py-6 text-lg shadow-lg shadow-red-200"
            >
              <Square className="mr-2 h-5 w-5" /> Stop
            </Button>
          )}
        </div>

        {/* Playback & Upload */}
        {audioUrl && !isRecording && (
          <div className="w-full space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="flex items-center gap-3 bg-gray-50 p-3 rounded-lg border border-gray-200">
              <Button size="sm" variant="secondary" onClick={() => {
                const audio = new Audio(audioUrl);
                audio.play();
              }}>
                <Play className="h-4 w-4" />
              </Button>
              <div className="h-2 flex-1 bg-gray-200 rounded-full overflow-hidden">
                 <div className="h-full bg-blue-500 w-1/3"></div>
              </div>
              <span className="text-xs text-gray-500">Preview</span>
            </div>

            <Button 
              onClick={handleSubmit} 
              disabled={isUploading} 
              className="w-full py-4 text-lg bg-green-600 hover:bg-green-700"
            >
              {isUploading ? (
                <>
                  <Loader2 className="mr-2 h-5 w-5 animate-spin" /> Analyzing...
                </>
              ) : (
                <>
                  <UploadCloud className="mr-2 h-5 w-5" /> Analyze Response
                </>
              )}
            </Button>
          </div>
        )}

        <div className="relative w-full">
            <div className="absolute inset-0 flex items-center">
                <span className="w-full border-t" />
            </div>
            <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-white px-2 text-muted-foreground">Or upload file</span>
            </div>
        </div>

        <div className="w-full">
            <input
                type="file"
                accept="audio/*"
                className="hidden"
                id="file-upload"
                onChange={handleFileUpload}
            />
            <label 
                htmlFor="file-upload"
                className="flex items-center justify-center w-full px-4 py-2 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors"
            >
                <FileAudio className="mr-2 h-4 w-4 text-gray-500" />
                <span className="text-sm text-gray-600">Choose .wav or .mp3</span>
            </label>
        </div>

      </div>
    </div>
  )
}
