import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Converter from './components/Converter';
import Auth from './components/Auth';
import Home from './components/Home';
import SpeechToSign from './components/SpeechToSign.tsx';

function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 to-gray-900 flex flex-col items-center justify-center p-4">
      <h1 className="text-5xl font-semibold text-white mb-2 p-8">SignWave</h1>

      {/* Video placeholder */}
      <div className="w-72 aspect-video bg-gray-800 rounded-lg shadow-xl mb-8 flex items-center justify-center border border-purple-700 hover:border-purple-600 transition-colors">
        <video autoPlay loop muted playsInline preload='auto'>
          <source src='src/Assets/Age.mp4' type='video/mp4' />
        </video>
      </div>

      {/* Get Started button */}
      <button 
        onClick={() => navigate('/auth')}
        className="px-8 py-4 bg-purple-600 hover:bg-purple-700 text-white font-semibold rounded-lg 
                   shadow-lg transform transition-all duration-200 hover:scale-105 
                   focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-opacity-50"
      >
        Get Started
      </button>
    </div>
  );
}

function App() {
  const [user, setUser] = useState<{ name: string; email: string } | null>(null);

  return (
    <Router>
      <Routes>
        <Route path="/" element={!user ? <LandingPage /> : <Navigate to="/home" replace />} />
        <Route path="/auth" element={!user ? <Auth onLogin={setUser} /> : <Navigate to="/home" replace />} />
        <Route
          path="/home"
          element={
            user ? (
              <>
                <Navbar user={user} onLogout={() => setUser(null)} />
                <Home user={user} />
              </>
            ) : (
              <Navigate to="/auth" replace />
            )
          }
        />
        <Route
          path="/converter"
          element={
            user ? (
              <>
                <Navbar user={user} onLogout={() => setUser(null)} />
                <Converter />
              </>
            ) : (
              <Navigate to="/auth" replace />
            )
          }
        />
        <Route
          path="/speech-to-sign"
          element={
            user ? (
              <>
                <Navbar user={user} onLogout={() => setUser(null)} />
                <SpeechToSign />
              </>
            ) : (
              <Navigate to="/auth" replace />
            )
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
