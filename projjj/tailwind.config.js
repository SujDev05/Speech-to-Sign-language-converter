/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        purple: {
          900: '#2D1B69',
          800: '#382180',
          700: '#442697',
          600: '#5031B5',
          500: '#5C3CD4',
        },
      },
    },
  },
  plugins: [],
};