/** @type {import('tailwindcss').Config} */
// eslint-disable-next-line no-undef
module.exports = {
  content: ['./frontend/**/*.{js,jsx,ts,tsx}'],
  safelist: ['grid-cols-1', 'grid-cols-2', 'grid-cols-3', 'col-span-1', 'col-span-2', 'col-span-3'],
  theme: {
    extend: {},
  },
  plugins: [],
};
