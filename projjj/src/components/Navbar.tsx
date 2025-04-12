import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Home, FileVideo, LogOut, Mail, Info, User } from 'lucide-react';

interface NavbarProps {
  user: { name: string; email: string };
  onLogout: () => void;
}

function Navbar({ user, onLogout }: NavbarProps) {
  const navigate = useNavigate();

  const handleLogout = () => {
    onLogout();
    navigate('/auth');
  };

  return (
    <nav className="bg-purple-900 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-8">
            <Link to="/home" className="flex items-center space-x-2 hover:text-purple-200 transition-colors">
              <Home size={20} />
              <span>Home</span>
            </Link>
            <Link to="/converter" className="flex items-center space-x-2 hover:text-purple-200 transition-colors">
              <FileVideo size={20} />
              <span>Converter</span>
            </Link>
            <Link to="/about" className="flex items-center space-x-2 hover:text-purple-200 transition-colors">
              <Info size={20} />
              <span>About</span>
            </Link>
            <Link to="/contact" className="flex items-center space-x-2 hover:text-purple-200 transition-colors">
              <Mail size={20} />
              <span>Contact Us</span>
            </Link>
          </div>
          <div className="flex items-center space-x-6">
            <div className="flex items-center space-x-2">
              <User size={20} className="text-purple-300" />
              <span className="text-purple-300">{user.name}</span>
            </div>
            <button 
              onClick={handleLogout}
              className="flex items-center space-x-2 hover:text-purple-200 transition-colors"
            >
              <LogOut size={20} />
              <span>Logout</span>
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;