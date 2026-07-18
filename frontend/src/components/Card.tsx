import React from 'react';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  glow?: boolean;
}

export function Card({ children, className = '', glow = false, ...props }: CardProps) {
  return (
    <div 
      className={`glass-panel rounded-xl p-6 shadow-cyber-glass transition-all duration-300 ${
        glow ? 'border-cyan-500/10 hover:border-cyan-500/25 hover:shadow-cyber-glass-hover' : ''
      } ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}
