import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Settings, Lock } from 'lucide-react';

export default function Sidebar() {
  const navItems = [
    { name: 'Dashboard', path: '/dashboard', icon: <LayoutDashboard size={20} /> },
    { name: 'Audit Ledger', path: '/ledger', icon: <Lock size={20} /> },
    { name: 'Settings', path: '/settings', icon: <Settings size={20} /> },
  ];

  return (
    <aside className="w-64 bg-surface/50 backdrop-blur-xl border-r border-slate-800 flex flex-col hidden md:flex shrink-0">
      <nav className="flex-1 py-6 px-4 space-y-2">
        {navItems.map((item) => (
            <NavLink 
              key={item.name} 
              to={item.path}
              className={({ isActive }) => 
                `flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-300 font-medium border-l-2 ${isActive ? 'bg-primary/10 text-primary border-primary shadow-[inset_0_0_20px_rgba(56,189,248,0.1)]' : 'border-transparent text-slate-400 hover:bg-slate-800/50 hover:text-white'}`
              }
            >
              <div className="transition-transform duration-300 group-hover:scale-110">
                {item.icon}
              </div>
              <span>{item.name}</span>
            </NavLink>
        ))}
      </nav>
    </aside>
  );
}
