/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/src/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
        'blue-lighter': '#183041',
        'blue-darker' : '#02020A'
      }
    },
  },
  plugins: [],
}