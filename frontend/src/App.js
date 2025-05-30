import { useEffect, useState } from "react";
import "./App.css";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const TikTokPromo = () => {
  const [promoContent, setPromoContent] = useState(null);
  const [currentTestimonial, setCurrentTestimonial] = useState(0);
  const [isAnimating, setIsAnimating] = useState(false);

  useEffect(() => {
    fetchPromoContent();
    
    // Auto-rotate testimonials every 3 seconds
    const interval = setInterval(() => {
      setCurrentTestimonial(prev => (prev + 1) % 3);
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  const fetchPromoContent = async () => {
    try {
      const response = await axios.get(`${API}/promo-content`);
      setPromoContent(response.data);
    } catch (error) {
      console.error('Error fetching promo content:', error);
    }
  };

  const trackClick = async (clickType) => {
    try {
      await axios.post(`${API}/track-click`, {
        click_type: clickType,
        user_agent: navigator.userAgent,
        ip_address: null // Would be set by backend in real app
      });
    } catch (error) {
      console.error('Error tracking click:', error);
    }
  };

  const handleBeaconsClick = () => {
    setIsAnimating(true);
    trackClick('beacons_link');
    
    setTimeout(() => {
      window.open('https://beacons.ai/junior47620', '_blank');
      setIsAnimating(false);
    }, 300);
  };

  const handleShare = () => {
    trackClick('share');
    if (navigator.share) {
      navigator.share({
        title: '💰 Make Money From Your PC!',
        text: 'Discover how to earn $100+ daily from your computer!',
        url: 'https://beacons.ai/junior47620'
      });
    } else {
      // Fallback to copying to clipboard
      navigator.clipboard.writeText('https://beacons.ai/junior47620');
      alert('Link copied to clipboard!');
    }
  };

  if (!promoContent) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-white text-xl">Loading amazing opportunity...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-white relative overflow-hidden">
      {/* Background gradient animation */}
      <div className="absolute inset-0 bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 opacity-50"></div>
      
      {/* Floating money emojis */}
      <div className="absolute inset-0 pointer-events-none">
        {[...Array(15)].map((_, i) => (
          <div
            key={i}
            className={`absolute text-2xl animate-bounce`}
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 2}s`,
              animationDuration: `${2 + Math.random() * 2}s`
            }}
          >
            💰
          </div>
        ))}
      </div>

      {/* Main content container */}
      <div className="relative z-10 flex flex-col min-h-screen">
        
        {/* Header */}
        <div className="flex justify-between items-center p-4">
          <div className="text-lg font-bold">💻 PC Money Maker</div>
          <button 
            onClick={handleShare}
            className="bg-pink-500 hover:bg-pink-600 px-4 py-2 rounded-full text-sm font-bold transition-colors"
          >
            📤 Share
          </button>
        </div>

        {/* Main video-style content */}
        <div className="flex-1 flex flex-col justify-center items-center px-6 py-8">
          
          {/* Title with pulsing animation */}
          <h1 className="text-4xl md:text-6xl font-black text-center mb-6 animate-pulse bg-gradient-to-r from-yellow-400 via-pink-500 to-purple-600 bg-clip-text text-transparent">
            {promoContent.title}
          </h1>

          {/* Subtitle */}
          <h2 className="text-xl md:text-2xl text-center mb-8 text-yellow-300 font-bold">
            {promoContent.subtitle}
          </h2>

          {/* Benefits list with stagger animation */}
          <div className="mb-8 space-y-3">
            {promoContent.benefits.map((benefit, index) => (
              <div 
                key={index}
                className={`text-lg md:text-xl text-center transform transition-all duration-500 ${
                  index % 2 === 0 ? 'animate-slide-in-left' : 'animate-slide-in-right'
                }`}
                style={{ animationDelay: `${index * 0.2}s` }}
              >
                {benefit}
              </div>
            ))}
          </div>

          {/* Testimonial carousel */}
          <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 mb-8 max-w-md mx-auto border border-white/20">
            <div className="text-center">
              <div className="text-2xl font-bold text-green-400 mb-2">
                {promoContent.testimonials[currentTestimonial].amount}
              </div>
              <div className="text-sm mb-2 opacity-90">
                "{promoContent.testimonials[currentTestimonial].quote}"
              </div>
              <div className="text-xs text-gray-300">
                - {promoContent.testimonials[currentTestimonial].name}
              </div>
            </div>
          </div>

          {/* Main CTA Button */}
          <button
            onClick={handleBeaconsClick}
            className={`
              bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700
              text-white font-black text-xl md:text-2xl px-8 py-4 rounded-full
              transform transition-all duration-300 hover:scale-110 shadow-2xl
              border-4 border-yellow-400 hover:border-yellow-300
              ${isAnimating ? 'animate-pulse scale-110' : ''}
            `}
          >
            🚀 {promoContent.call_to_action} 🚀
          </button>

          {/* Urgency text */}
          <div className="mt-4 text-center">
            <div className="text-red-400 font-bold animate-blink">
              ⚡ LIMITED TIME OFFER ⚡
            </div>
            <div className="text-sm text-gray-300 mt-2">
              Join 10,000+ people already earning daily!
            </div>
          </div>
        </div>

        {/* Bottom action bar (TikTok style) */}
        <div className="flex justify-center items-center space-x-8 p-6 bg-black/50 backdrop-blur-md">
          <button className="flex flex-col items-center space-y-1 text-white hover:text-pink-400 transition-colors">
            <div className="text-2xl">❤️</div>
            <div className="text-xs">Like</div>
          </button>
          
          <button 
            onClick={handleShare}
            className="flex flex-col items-center space-y-1 text-white hover:text-yellow-400 transition-colors"
          >
            <div className="text-2xl">📤</div>
            <div className="text-xs">Share</div>
          </button>
          
          <button 
            onClick={handleBeaconsClick}
            className="flex flex-col items-center space-y-1 text-white hover:text-green-400 transition-colors"
          >
            <div className="text-2xl">💰</div>
            <div className="text-xs">Earn</div>
          </button>
        </div>
      </div>

      {/* Floating action button */}
      <div className="fixed bottom-20 right-6">
        <button
          onClick={handleBeaconsClick}
          className="bg-green-500 hover:bg-green-600 text-white p-4 rounded-full shadow-2xl animate-bounce text-2xl"
        >
          💸
        </button>
      </div>
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <TikTokPromo />
    </div>
  );
}

export default App;
