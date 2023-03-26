import React from 'react'

interface LogoProps {
  className?: string
}

function Logo({ className }: LogoProps) {
  return (
    <div className={className}>
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none">
        <g clipPath="url(#a)">
          <rect width="100%" height="100%" fill="#7950F2" rx="8" />
          <path
            fill="#fff"
            d="M22.071 47.48c-1.2 0-2.12-.32-2.76-.96-.64-.68-.96-1.64-.96-2.88V20.96c0-1.24.32-2.18.96-2.82.64-.64 1.54-.96 2.7-.96 1.16 0 2.06.32 2.7.96.64.64.96 1.58.96 2.82v4.08l-.66-1.5c.88-2.12 2.24-3.72 4.08-4.8 1.88-1.12 4-1.68 6.36-1.68 2.36 0 4.3.44 5.82 1.32 1.52.88 2.66 2.22 3.42 4.02.76 1.76 1.14 4 1.14 6.72v14.52c0 1.24-.32 2.2-.96 2.88-.64.64-1.56.96-2.76.96-1.2 0-2.14-.32-2.82-.96-.64-.68-.96-1.64-.96-2.88V29.48c0-2.28-.44-3.94-1.32-4.98-.84-1.04-2.16-1.56-3.96-1.56-2.2 0-3.96.7-5.28 2.1-1.28 1.36-1.92 3.18-1.92 5.46v13.14c0 2.56-1.26 3.84-3.78 3.84Z"
          />
        </g>
        <defs>
          <clipPath id="a">
            <rect width="100%" height="100%" fill="#fff" rx="8" />
          </clipPath>
        </defs>
      </svg>
    </div>
  )
}

export default Logo
