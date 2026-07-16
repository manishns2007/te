import { AlertTriangle } from 'lucide-react';

export function ErrorState({ message }: { message: string }) {
  return (
    <div className="flex flex-col items-center justify-center p-12 text-center h-full text-risk-red">
      <AlertTriangle size={48} className="mb-4" />
      <h3 className="text-lg font-medium">Something went wrong</h3>
      <p className="mt-2 text-sm max-w-sm">{message}</p>
    </div>
  );
}
