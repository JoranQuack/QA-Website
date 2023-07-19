// @ts-nocheck
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
        fade_in: 'fade 0.3s ease-in forwards',
        fade_out: 'fade 0.3s ease-out forwards reverse',
        error: 'error 5s ease forwards',
        collapse_row: 'collapse_row 0.3s ease-in-out forwards',
      },

      keyframes: theme => ({
        delayed_fade_in: {
          '0%, 90%': { opacity: 0 },
          '100%': { opacity: 1 },
        },
        fade: {
          '0%': { opacity: 0 },
          '100%': { opacity: 1 },
        },
        error: {
          '0%': { transform: 'translateY(310%)' },
          '10%, 90%': { transform: 'translateY(0%)' },
          '100%': { transform: 'translateY(310%)' }
        },
        collapse_row: {
          '0%': {},
          '100%': { 'padding-bottom': '0', 'padding-top': '0', transform: 'scaleY(0)' },
        },
      }),



      colors: {
        'blue-lighter': '#243f53',
        'blue-darker': '#030b13',
        'blue-qa': '#18C0DE',
        'white-qa': '#ced0de',
        'success': '#166534',
        'error': '#991b1b'
      }
    },

    fontFamily: {
      sans: ['Product Sans', 'sans-serif'],
      round: ['All Round Gothic', 'sans-serif']
    },

    dropShadow: {
      'glow-intense': '0 0 5px #18c0de',
      'glow-light': '0 0 10px #18c0deb6'
    },
  },
  plugins: [],
}