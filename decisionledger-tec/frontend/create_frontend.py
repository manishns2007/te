import os

frontend_path = r"C:\Users\NEELS\Desktop\TeleFusion\decisionledger-tec\frontend"

files = {
    "tailwind.config.js": """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#0f172a',
        surface: '#1e293b',
        primary: '#3b82f6',
        secondary: '#06b6d4',
        risk: {
          green: '#10b981',
          yellow: '#f59e0b',
          orange: '#f97316',
          red: '#ef4444'
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
""",
    "postcss.config.js": """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
""",
    "src/index.css": """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-background text-slate-200 font-sans antialiased;
  }
}
""",
    ".env": """VITE_API_BASE_URL=http://localhost:8000/api
""",
    "src/services/api.ts": """import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
    headers: {
        'Content-Type': 'application/json',
    },
});

export const DashboardService = {
    getDashboardData: () => api.get('/dashboard'),
};

export const TransactionService = {
    getTransaction: (id: string) => api.get(/transactions/),
};

export const DecisionService = {
    submitDecision: (id: string, action: string, notes: string) => 
        api.post(/transactions//decision, { action_taken: action, notes, investigator_id: 'Investigator-1' }),
};

export default api;
""",
    "src/App.tsx": """import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import DashboardLayout from './layouts/DashboardLayout';

const LandingPage = () => <div>Landing Page</div>;
const Dashboard = () => <div>Executive Dashboard</div>;
const DecisionConsole = () => <div>Decision Console</div>;
const NotFound = () => <div className="p-8 text-center">404 - Page Not Found</div>;

function App() {
  return (
    <Router>
      <Routes>
        <Route element={<MainLayout />}>
          <Route path="/" element={<LandingPage />} />
        </Route>
        <Route element={<DashboardLayout />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/decision/:transactionId" element={<DecisionConsole />} />
        </Route>
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
}

export default App;
""",
    "src/layouts/MainLayout.tsx": """import { Outlet } from 'react-router-dom';
import Navbar from '../components/Navbar';

export default function MainLayout() {
  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Navbar />
      <main className="flex-grow">
        <Outlet />
      </main>
    </div>
  );
}
""",
    "src/layouts/DashboardLayout.tsx": """import { Outlet } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import Navbar from '../components/Navbar';

export default function DashboardLayout() {
  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <Sidebar />
      <div className="flex flex-col flex-1 overflow-hidden">
        <Navbar />
        <main className="flex-1 overflow-y-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
""",
    "src/components/Navbar.tsx": """import { Activity } from 'lucide-react';

export default function Navbar() {
  return (
    <header className="bg-surface border-b border-slate-700 h-16 flex items-center px-6 shrink-0 shadow-sm z-10">
      <div className="flex items-center gap-2">
        <Activity className="text-primary w-6 h-6" />
        <span className="text-lg font-semibold text-white tracking-wide">DecisionLedger <span className="text-primary font-bold">TEC</span></span>
      </div>
    </header>
  );
}
""",
    "src/components/Sidebar.tsx": """import { NavLink } from 'react-router-dom';
import { LayoutDashboard, FileText, Settings, Info } from 'lucide-react';

export default function Sidebar() {
  const navItems = [
    { name: 'Dashboard', path: '/dashboard', icon: <LayoutDashboard size={20} /> },
    { name: 'Decision Console', path: '/decision/placeholder', icon: <FileText size={20} /> },
    { name: 'Settings', path: '/settings', icon: <Settings size={20} />, disabled: true },
    { name: 'About', path: '/about', icon: <Info size={20} /> },
  ];

  return (
    <aside className="w-64 bg-surface border-r border-slate-700 flex flex-col hidden md:flex shrink-0">
      <nav className="flex-1 py-6 px-4 space-y-2">
        {navItems.map((item) => (
          item.disabled ? (
            <div key={item.name} className="flex items-center gap-3 px-4 py-3 rounded-lg text-slate-500 cursor-not-allowed">
              {item.icon}
              <span className="font-medium">{item.name}</span>
            </div>
          ) : (
            <NavLink 
              key={item.name} 
              to={item.path}
              className={({ isActive }) => 
                lex items-center gap-3 px-4 py-3 rounded-lg transition-colors font-medium 
              }
            >
              {item.icon}
              <span>{item.name}</span>
            </NavLink>
          )
        ))}
      </nav>
    </aside>
  );
}
""",
    "src/components/Card.tsx": """import React from 'react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {}

export function Card({ className, ...props }: CardProps) {
  return (
    <div className={cn("bg-surface rounded-xl border border-slate-700 shadow-sm", className)} {...props} />
  );
}
""",
    "src/components/Badge.tsx": """import React from 'react';

export function Badge({ children, className = '' }: { children: React.ReactNode, className?: string }) {
  return (
    <span className={inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium }>
      {children}
    </span>
  );
}
""",
    "src/components/Button.tsx": """import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
}

export function Button({ variant = 'primary', className = '', ...props }: ButtonProps) {
  const base = "inline-flex items-center justify-center px-4 py-2 rounded-lg font-medium transition-colors focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed";
  const variants = {
    primary: "bg-primary hover:bg-blue-600 text-white",
    secondary: "bg-slate-700 hover:bg-slate-600 text-white",
    danger: "bg-risk-red hover:bg-red-600 text-white",
    ghost: "hover:bg-slate-800 text-slate-300 hover:text-white"
  };
  
  return (
    <button className={${base}  } {...props} />
  );
}
""",
    "src/components/StatusChip.tsx": """import { Badge } from './Badge';

export function StatusChip({ status }: { status: string }) {
  let color = 'bg-slate-700 text-slate-300';
  if (status === 'PENDING') color = 'bg-yellow-500/20 text-yellow-500';
  if (status === 'FLAGGED') color = 'bg-orange-500/20 text-orange-500';
  if (status === 'FREEZE') color = 'bg-red-500/20 text-red-500';
  if (status === 'MONITOR') color = 'bg-blue-500/20 text-blue-500';
  
  return <Badge className={color}>{status}</Badge>;
}
""",
    "src/components/MetricCard.tsx": """import { Card } from './Card';
import React from 'react';

interface MetricCardProps {
  title: string;
  value: string | number;
  icon?: React.ReactNode;
  description?: string;
}

export function MetricCard({ title, value, icon, description }: MetricCardProps) {
  return (
    <Card className="p-6">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-slate-400">{title}</p>
          <p className="mt-2 text-3xl font-semibold text-white">{value}</p>
        </div>
        {icon && <div className="p-3 bg-slate-800 rounded-lg text-primary">{icon}</div>}
      </div>
      {description && <p className="mt-4 text-sm text-slate-500">{description}</p>}
    </Card>
  );
}
""",
    "src/components/SectionCard.tsx": """import { Card } from './Card';
import React from 'react';

interface SectionCardProps {
  title: string;
  children: React.ReactNode;
  className?: string;
}

export function SectionCard({ title, children, className = '' }: SectionCardProps) {
  return (
    <Card className={lex flex-col }>
      <div className="px-6 py-4 border-b border-slate-700">
        <h3 className="text-lg font-medium text-white">{title}</h3>
      </div>
      <div className="p-6 flex-1">
        {children}
      </div>
    </Card>
  );
}
""",
    "src/components/PageHeader.tsx": """export function PageHeader({ title, subtitle }: { title: string, subtitle?: string }) {
  return (
    <div className="mb-8">
      <h1 className="text-2xl font-bold text-white">{title}</h1>
      {subtitle && <p className="mt-1 text-slate-400">{subtitle}</p>}
    </div>
  );
}
""",
    "src/components/LoadingSpinner.tsx": """import { Loader2 } from 'lucide-react';

export function LoadingSpinner({ size = 24 }: { size?: number }) {
  return (
    <div className="flex justify-center items-center h-full w-full">
      <Loader2 size={size} className="animate-spin text-primary" />
    </div>
  );
}
""",
    "src/components/LoadingSkeleton.tsx": """export function LoadingSkeleton({ className = '' }: { className?: string }) {
  return (
    <div className={nimate-pulse bg-slate-700 rounded-md }></div>
  );
}
""",
    "src/components/EmptyState.tsx": """import React from 'react';
import { Inbox } from 'lucide-react';

export function EmptyState({ title, description, icon }: { title: string, description?: string, icon?: React.ReactNode }) {
  return (
    <div className="flex flex-col items-center justify-center p-12 text-center h-full">
      <div className="text-slate-500 mb-4">{icon || <Inbox size={48} />}</div>
      <h3 className="text-lg font-medium text-white">{title}</h3>
      {description && <p className="mt-2 text-sm text-slate-400 max-w-sm">{description}</p>}
    </div>
  );
}
""",
    "src/components/ErrorState.tsx": """import { AlertTriangle } from 'lucide-react';

export function ErrorState({ message }: { message: string }) {
  return (
    <div className="flex flex-col items-center justify-center p-12 text-center h-full text-risk-red">
      <AlertTriangle size={48} className="mb-4" />
      <h3 className="text-lg font-medium">Something went wrong</h3>
      <p className="mt-2 text-sm max-w-sm">{message}</p>
    </div>
  );
}
"""
}

for rel_path, content in files.items():
    full_path = os.path.join(frontend_path, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
print("Frontend files generated successfully.")
