/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/*.html", "./main.py"],
  theme: {
    container: {
      center: true,
      padding: '2rem'
    },
    extend: {
      colors: {
        warning: 'red',
        white: 'white'
      }
    },
  },
  plugins: [],
}

