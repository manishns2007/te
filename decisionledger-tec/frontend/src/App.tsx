import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import DashboardLayout from './layouts/DashboardLayout';

import LandingPage from './pages/LandingPage';
import Dashboard from './pages/Dashboard';
import DecisionConsole from './pages/DecisionConsole';

const NotFound = () => <div className="p-8 text-center text-slate-400">404 - Page Not Found</div>;

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
