import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Shield, Crosshair, BarChart3, Lock, Mail, MapPin, Phone, ArrowRight, ChevronUp, ArrowRightLeft } from 'lucide-react';

const Landing = () => {
  const [scrolled, setScrolled] = useState(false);
  const [showTopBtn, setShowTopBtn] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
      setShowTopBtn(window.scrollY > 400);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const scrollToSection = (id) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div className="min-h-screen bg-black text-slate-100 font-sans selection:bg-brand-teal selection:text-white">
      {/* Navigation */}
      <nav className={`fixed w-full z-50 transition-all duration-300 ${scrolled ? 'bg-black/95 backdrop-blur-md shadow-lg shadow-black/20 py-4' : 'bg-transparent py-6'}`}>
        <div className="max-w-7xl mx-auto px-6 flex justify-between items-center">
          <div className="flex items-center space-x-3 cursor-pointer" onClick={scrollToTop}>
            <img src="/logo.jpg" alt="MAMS Logo" className="w-10 h-10 object-cover rounded-lg shadow-sm shadow-brand-teal/20" />
            <span className="text-2xl font-bold tracking-tight text-white">MAMS</span>
          </div>
          <div className="hidden md:flex items-center space-x-8">
            <button onClick={() => scrollToSection('about')} className="text-slate-300 hover:text-white transition-colors font-medium">About</button>
            <button onClick={() => scrollToSection('features')} className="text-slate-300 hover:text-white transition-colors font-medium">Features</button>
            <button onClick={() => scrollToSection('contact')} className="text-slate-300 hover:text-white transition-colors font-medium">Contact</button>
            <Link to="/login" className="bg-brand-teal/10 text-brand-teal border border-brand-teal/20 px-6 py-2.5 rounded-full font-semibold hover:bg-brand-teal hover:text-white transition-all transform hover:scale-105">
              Portal Login
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section id="home" className="relative pt-32 pb-20 lg:pt-48 lg:pb-32 overflow-hidden min-h-screen flex items-center">
        {/* Background elements */}
        <div className="absolute top-0 left-0 w-full h-full overflow-hidden -z-10">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-brand-teal/20 rounded-full blur-3xl opacity-50 animate-pulse"></div>
          <div className="absolute bottom-1/4 right-1/4 w-[500px] h-[500px] bg-blue-900/20 rounded-full blur-3xl opacity-50"></div>
          <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10"></div>
          <div className="absolute inset-0 bg-gradient-to-b from-black/50 via-black to-black"></div>
        </div>

        <div className="max-w-7xl mx-auto px-6 text-center relative z-10">
          <div className="inline-flex items-center px-4 py-2 rounded-full bg-slate-800 border border-slate-700 text-sm font-medium text-brand-teal mb-8 animate-fade-in-up">
            <span className="flex h-2 w-2 rounded-full bg-brand-teal mr-2 animate-ping"></span>
            Military-Grade Security Protocol Enabled
          </div>
          <h1 className="text-5xl lg:text-7xl font-extrabold text-white mb-6 tracking-tight leading-tight animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
            Next-Generation <br className="hidden lg:block" />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-teal to-blue-500">
              Asset Management
            </span>
          </h1>
          <p className="text-lg lg:text-xl text-slate-400 mb-10 max-w-2xl mx-auto animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
            Unify your logistics, track equipment in real-time, and ensure operational readiness across all bases with our centralized command platform.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-6 animate-fade-in-up" style={{ animationDelay: '0.3s' }}>
            <button onClick={() => scrollToSection('about')} className="w-full sm:w-auto bg-brand-teal text-white px-8 py-4 rounded-full font-bold text-lg hover:bg-teal-400 hover:shadow-lg hover:shadow-brand-teal/25 transition-all transform hover:-translate-y-1 flex items-center justify-center">
              Discover MAMS <ArrowRight className="ml-2" size={20} />
            </button>
            <Link to="/login" className="w-full sm:w-auto bg-slate-800 text-white border border-slate-700 px-8 py-4 rounded-full font-bold text-lg hover:bg-slate-700 transition-all">
              Access Portal
            </Link>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-24 bg-[#050505] border-y border-slate-900 relative">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex flex-col lg:flex-row items-center gap-16">
            <div className="lg:w-1/2 space-y-6">
              <h2 className="text-3xl lg:text-5xl font-bold text-white tracking-tight">
                About The <span className="text-brand-teal">System</span>
              </h2>
              <div className="w-20 h-1 bg-gradient-to-r from-brand-teal to-blue-600 rounded-full"></div>
              <p className="text-slate-300 text-lg leading-relaxed">
                The Military Asset Management System (MAMS) was developed to solve the complex logistical challenges faced by modern defense forces. We provide a single source of truth for all operational equipment, ensuring that every asset is tracked from procurement to decommissioning.
              </p>
              <p className="text-slate-300 text-lg leading-relaxed">
                Designed with security and efficiency at its core, MAMS empowers base commanders and logistics officers with real-time data, reducing operational friction and maximizing readiness.
              </p>
              <ul className="space-y-4 pt-4">
                {[
                  'Real-time inventory synchronization across global bases',
                  'Secure, role-based access control (RBAC)',
                  'Comprehensive audit trails for absolute accountability'
                ].map((item, i) => (
                  <li key={i} className="flex items-center text-slate-200">
                    <div className="mr-4 p-1 rounded-full bg-brand-teal/20 text-brand-teal">
                      <Check size={16} />
                    </div>
                    {item}
                  </li>
                ))}
              </ul>
            </div>
            <div className="lg:w-1/2 relative">
              <div className="absolute inset-0 bg-gradient-to-tr from-brand-teal/20 to-blue-500/20 rounded-2xl transform rotate-3 scale-105 -z-10"></div>
              <img src="https://images.unsplash.com/photo-1574390095147-380d603e87d1?q=80&w=1000&auto=format&fit=crop" alt="Military Logistics" className="rounded-2xl shadow-2xl border border-slate-700 object-cover h-[500px] w-full filter brightness-75 contrast-125" />
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-24 relative">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-5xl font-bold text-white tracking-tight mb-6">Core Capabilities</h2>
            <p className="text-slate-400 max-w-2xl mx-auto text-lg">Engineered for resilience. Built for command.</p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {[
              { icon: <Crosshair size={32} />, title: 'Precision Tracking', desc: 'Monitor the exact location, status, and assignment of every piece of equipment in your arsenal.' },
              { icon: <ArrowRightLeft size={32} />, title: 'Seamless Transfers', desc: 'Initiate, approve, and complete inter-base equipment transfers with full cryptographic auditing.' },
              { icon: <BarChart3 size={32} />, title: 'Strategic Insights', desc: 'Aggregated dashboard metrics give commanders a bird\'s-eye view of operational readiness.' },
              { icon: <Lock size={32} />, title: 'Zero-Trust Security', desc: 'Every action is authenticated, authorized, and logged. If it happens in MAMS, it\'s on the record.' },
              { icon: <Shield size={32} />, title: 'Base Isolation', desc: 'Multi-tenant architecture ensures logistics officers only see and manage their authorized base inventory.' },
              { icon: <MapPin size={32} />, title: 'Global Deployment', desc: 'Cloud-native architecture designed to operate across distributed geographical locations.' },
            ].map((feature, i) => (
              <div key={i} className="bg-slate-800/50 border border-slate-700/50 p-8 rounded-2xl hover:bg-slate-800 hover:border-brand-teal/50 transition-all group">
                <div className="bg-slate-900 w-16 h-16 rounded-xl flex items-center justify-center text-brand-teal mb-6 group-hover:scale-110 group-hover:shadow-lg group-hover:shadow-brand-teal/20 transition-all">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-bold text-white mb-3">{feature.title}</h3>
                <p className="text-slate-400 leading-relaxed">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="py-24 bg-black border-t border-slate-900">
        <div className="max-w-7xl mx-auto px-6">
          <div className="bg-gradient-to-br from-slate-900 to-black border border-slate-800 rounded-3xl overflow-hidden shadow-2xl">
            <div className="grid lg:grid-cols-2">
              <div className="p-12 lg:p-16">
                <h2 className="text-3xl lg:text-4xl font-bold text-white mb-4">Request Deployment</h2>
                <p className="text-slate-400 mb-8 text-lg">Interested in deploying MAMS for your organization? Contact our defense solutions team for a technical briefing.</p>
                
                <div className="space-y-6">
                  <div className="flex items-center text-slate-300">
                    <div className="bg-slate-800 p-3 rounded-lg mr-4 border border-slate-700">
                      <Mail className="text-brand-teal" size={24} />
                    </div>
                    <div>
                      <p className="text-sm text-slate-500 font-medium">Email Operations</p>
                      <p className="font-semibold text-white">deployments@mams-defense.gov</p>
                    </div>
                  </div>
                  <div className="flex items-center text-slate-300">
                    <div className="bg-slate-800 p-3 rounded-lg mr-4 border border-slate-700">
                      <Phone className="text-brand-teal" size={24} />
                    </div>
                    <div>
                      <p className="text-sm text-slate-500 font-medium">Secure Line</p>
                      <p className="font-semibold text-white">+1 (800) 555-0199</p>
                    </div>
                  </div>
                  <div className="flex items-center text-slate-300">
                    <div className="bg-slate-800 p-3 rounded-lg mr-4 border border-slate-700">
                      <MapPin className="text-brand-teal" size={24} />
                    </div>
                    <div>
                      <p className="text-sm text-slate-500 font-medium">Headquarters</p>
                      <p className="font-semibold text-white">Department of Defense Logistics, Section 4</p>
                    </div>
                  </div>
                </div>
              </div>
              <div className="bg-slate-800/80 p-12 lg:p-16 flex flex-col justify-center">
                <form className="space-y-6" onSubmit={(e) => e.preventDefault()}>
                  <div>
                    <label className="block text-sm font-medium text-slate-400 mb-2">Organization Name</label>
                    <input type="text" className="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-white focus:outline-none focus:border-brand-teal focus:ring-1 focus:ring-brand-teal transition-colors" placeholder="e.g. 1st Infantry Division" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-400 mb-2">Official Email</label>
                    <input type="email" className="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-white focus:outline-none focus:border-brand-teal focus:ring-1 focus:ring-brand-teal transition-colors" placeholder="commander@domain.mil" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-400 mb-2">Clearance Level / Message</label>
                    <textarea rows="4" className="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-white focus:outline-none focus:border-brand-teal focus:ring-1 focus:ring-brand-teal transition-colors" placeholder="Describe your deployment requirements..."></textarea>
                  </div>
                  <button className="w-full bg-brand-teal text-white font-bold py-4 rounded-lg hover:bg-teal-400 transition-colors">
                    Submit Request
                  </button>
                </form>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-black py-8 border-t border-slate-900 text-center text-slate-500 text-sm">
        <p>&copy; {new Date().getFullYear()} Military Asset Management System. All systems operational.</p>
      </footer>

      {/* Scroll to top button */}
      <button 
        onClick={scrollToTop}
        className={`fixed bottom-8 right-8 bg-brand-teal text-white p-3 rounded-full shadow-lg shadow-brand-teal/20 transition-all duration-300 z-50 ${showTopBtn ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10 pointer-events-none'}`}
      >
        <ChevronUp size={24} />
      </button>
    </div>
  );
};

const Check = ({ size }) => (
  <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="20 6 9 17 4 12"></polyline>
  </svg>
);

export default Landing;
