import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Settings, Lock } from 'lucide-react';

export default function Sidebar() {
  const navItems = [
    { name: 'Dashboard', path: '/dashboard', icon: <LayoutDashboard size={20} /> },
    { name: 'Audit Ledger', path: '/ledger', icon: <Lock size={20} /> },
    { name: 'Settings', path: '/settings', icon: <Settings size={20} /> },
  ];

  return (
    <aside className="w-64 bg-surface border-r border-slate-700 flex flex-col hidden md:flex shrink-0">
      <nav className="flex-1 py-6 px-4 space-y-2">
        {navItems.map((item) => (
            <NavLink 
              key={item.name} 
              to={item.path}
              className={({ isActive }) => 
                `flex items-center gap-3 px-4 py-3 rounded-lg transition-colors font-medium ${isActive ? 'bg-primary text-white' : 'text-slate-400 hover:bg-slate-800'}`
              }
            >
              {item.icon}
              <span>{item.name}</span>
            </NavLink>
        ))}
      </nav>
    </aside>
  );
}
