import React from 'react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {}

export function Card({ className, ...props }: CardProps) {
  return (
    <div className={cn("bg-surface/60 backdrop-blur-xl rounded-xl border border-slate-800 shadow-lg hover:border-slate-700 hover:shadow-glow-primary/20 transition-all duration-300", className)} {...props} />
  );
}
