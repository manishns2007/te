import { Outlet } from 'react-router-dom';
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
