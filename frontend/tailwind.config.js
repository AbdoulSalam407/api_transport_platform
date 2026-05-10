/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{html,ts}',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          navy: '#1A3D7C',
          orange: '#FF7A00',
          light: '#F5F7FB',
          gray: '#E5E7EB',
        },
      },
      fontFamily: {
        heading: ['Poppins', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        body: ['Roboto', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        soft: '0 10px 25px -10px rgba(26, 61, 124, 0.25)',
      },
    },
  },
  plugins: [],
};
