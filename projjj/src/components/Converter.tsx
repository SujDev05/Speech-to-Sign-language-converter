import React, { useState, useEffect } from 'react';
import { Mic, MicOff, Play } from 'lucide-react';

function Converter() {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  
  const toggleListening = () => {
    if (!isListening) {
      startListening();
    } else {
      stopListening();
    }
  };

  const startListening = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;
      
      recognition.onstart = () => setIsListening(true);
      recognition.onend = () => setIsListening(false);
      recognition.onresult = (event) => {
        const transcript = Array.from(event.results)
          .map(result => result[0])
          .map(result => result.transcript)
          .join('');
        setTranscript(transcript);
      };
      
      recognition.start();
    } else {
      alert('Speech recognition is not supported in this browser.');
    }
  };

  const stopListening = () => {
    setIsListening(false);
    // The recognition.stop() would be called here in a full implementation
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] bg-gradient-to-br from-purple-900 to-gray-900 p-6">
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Left side - Speech Input */}
        <div className="bg-gray-800 rounded-lg p-6 shadow-xl border border-purple-700">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold text-white">Speech Input</h2>
            <button
              onClick={toggleListening}
              className={`p-3 rounded-full transition-colors ${
                isListening 
                  ? 'bg-red-600 hover:bg-red-700' 
                  : 'bg-purple-600 hover:bg-purple-700'
              }`}
            >
              {isListening ? <MicOff size={24} /> : <Mic size={24} />}
            </button>
          </div>
          <textarea
            value={transcript}
            onChange={(e) => setTranscript(e.target.value)}
            className="w-full h-64 bg-gray-700 text-white rounded-lg p-4 focus:outline-none focus:ring-2 focus:ring-purple-500"
            placeholder="Your speech will appear here..."
          />
        </div>

        {/* Right side - Video Output */}
        <div className="bg-gray-800 rounded-lg p-6 shadow-xl border border-purple-700">
          <h2 className="text-xl font-semibold text-white mb-4">Video Output</h2>
          <div className="aspect-video bg-gray-700 rounded-lg flex items-center justify-center">
            <div className="text-gray-400 flex flex-col items-center gap-4">
              <Play size={48} />
              <span className="text-sm">Video will appear here</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Converter;