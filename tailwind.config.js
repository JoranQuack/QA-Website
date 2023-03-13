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
        'blue-darker' : '#02020A',
        'blue-qa' : '#18C0DE',
        'white-qa' : '#E1E2EF'
      }
    },
  },
  plugins: [],
}