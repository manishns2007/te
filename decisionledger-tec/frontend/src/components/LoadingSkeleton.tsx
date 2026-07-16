export function LoadingSkeleton({ className = '' }: { className?: string }) {
  return (
    <div className={`animate-pulse bg-slate-700 rounded-md ${className}`}></div>
  );
}
