/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", // Scans all HTML files in templates
    "./static/**/*.js"       // Scans any JS files where you might inject classes
  ],
  theme: {
    extend: {
      colors: {
        primary: '#2563eb', 
        dark: '#0f172a',
      }
    },
  },
  plugins: [],
}
