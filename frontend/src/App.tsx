import React, { useEffect, useRef, useState } from 'react'
import Hls from 'hls.js'

const BACKEND = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

export default function App() {
  const [manifestUrl, setManifestUrl] = useState<string | null>(null)
  const [movieId, setMovieId] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)
  const videoRef = useRef<HTMLVideoElement | null>(null)

  useEffect(() => {
    const video = videoRef.current
    if (!video || !manifestUrl) return
    if (Hls.isSupported()) {
      const hls = new Hls()
      hls.loadSource(manifestUrl)
      hls.attachMedia(video)
      return () => {
        hls.destroy()
      }
    } else {
      video.src = manifestUrl
    }
  }, [manifestUrl])

  async function onUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0]
    if (!file) return
    setBusy(true)
    try {
      const form = new FormData()
      form.append('file', file)
      const res = await fetch(`${BACKEND}/upload`, { method: 'POST', body: form })
      if (!res.ok) throw new Error('Upload failed')
      const data = await res.json()
      setManifestUrl(`${BACKEND}${data.manifest}`)
      setMovieId(data.movie_id)
    } catch (err) {
      alert('Upload failed')
    } finally {
      setBusy(false)
    }
  }

  async function onCleanup() {
    if (!movieId) return
    try {
      await fetch(`${BACKEND}/cleanup/${movieId}`, { method: 'POST' })
      setMovieId(null)
      setManifestUrl(null)
    } catch {}
  }

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 p-6">
      <div className="max-w-3xl mx-auto space-y-4">
        <h1 className="text-2xl font-semibold">Compliant HLS Streamer</h1>
        <p className="text-sm text-gray-600">Upload your own or public-domain videos to stream.</p>

        <label className="inline-block px-4 py-2 bg-blue-600 text-white rounded cursor-pointer">
          {busy ? 'Uploading…' : 'Choose Video'}
          <input type="file" accept="video/*" onChange={onUpload} className="hidden" />
        </label>

        <div className="aspect-video bg-black rounded overflow-hidden">
          <video ref={videoRef} controls className="w-full h-full" />
        </div>

        {movieId && (
          <button onClick={onCleanup} className="px-4 py-2 bg-red-600 text-white rounded">
            Cleanup
          </button>
        )}
      </div>
    </div>
  )
}


