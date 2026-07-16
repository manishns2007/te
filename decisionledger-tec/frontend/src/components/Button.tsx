import React from 'react';

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
    <button className={`${base} ${variants[variant]} ${className}`} {...props} />
  );
}
