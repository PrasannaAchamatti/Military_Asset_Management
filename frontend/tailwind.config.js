/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          navy: '#0f172a',
          charcoal: '#1e293b',
          light: '#f8fafc',
          blue: '#3b82f6',
          teal: '#14b8a6',
          accent: '#0ea5e9',
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
