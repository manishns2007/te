/** @type {import('tailwindcss').Config} */
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
