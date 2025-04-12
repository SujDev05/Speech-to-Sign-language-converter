import React from 'react';
import { FileVideo, Wand2 } from 'lucide-react';
import { Link } from 'react-router-dom';

interface HomeProps {
  user: { name: string; email: string };
}

function Home({ user }: HomeProps) {
  return (
    <div className="min-h-[calc(100vh-4rem)] bg-gradient-to-br from-purple-900 to-gray-900 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-white mb-4">
            Welcome, {user.name}!
          </h1>
          <p className="text-purple-200 text-lg">
            Transform your speech into engaging videos with our cutting-edge converter
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          <Link
            to="/converter"
            className="bg-gray-800 p-8 rounded-lg shadow-xl border border-purple-700 hover:border-purple-500 
                     transform transition-all duration-200 hover:scale-[1.02] group"
          >
            <div className="flex flex-col items-center text-center">
              <FileVideo size={48} className="text-purple-400 mb-4 group-hover:text-purple-300 transition-colors" />
              <h2 className="text-2xl font-semibold text-white mb-2">Start Converting</h2>
              <p className="text-gray-300">
                Convert your speech to video with our easy-to-use interface
              </p>
            </div>
          </Link>

          <div className="bg-gray-800 p-8 rounded-lg shadow-xl border border-purple-700">
            <div className="flex flex-col items-center text-center">
              <Wand2 size={48} className="text-purple-400 mb-4" />
              <h2 className="text-2xl font-semibold text-white mb-2">How It Works</h2>
              <ul className="text-gray-300 text-left space-y-2">
                <li>1. Record or type your speech</li>
                <li>2. Choose your video preferences</li>
                <li>3. Generate your video</li>
                <li>4. Download and share!</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;