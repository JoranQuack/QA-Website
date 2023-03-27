/** @type {import('tailwindcss').Config} */
module.exports = {

  content: [
    "./templates/**/*.html",
    "./static/**/*.js",
    "./static/src/*.css",
  ],

  theme: {

    extend: {

      animation: {
        delayed_fade_in: 'delayed_fade_in 5s ease-in-out',
        fade_in: 'fade_in 0.3s ease-in-out',
      },

      keyframes: theme => ({
        delayed_fade_in: {
          '0%, 94%': { opacity: 0 },
          '100%': { opacity: 1 },
        },
        fade_in: {
          '0%': { opacity: 0 },
          '100%': { opacity: 1 },
        },
      }),

      colors: {
        'blue-lighter': '#183041',
        'blue-darker': '#02020A',
        'blue-qa': '#18C0DE',
        'white-qa': '#ced0de'
      }
    },

    fontFamily: {
      sans: ['Product Sans', 'sans-serif'],
      round: ['All Round Gothic', 'sans-serif']
    },

    dropShadow: {
      'glow': '0 0 10px #18c0deb6'
    },
  },
  plugins: [],
}