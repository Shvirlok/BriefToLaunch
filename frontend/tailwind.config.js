/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        cyberBg: "#030712",
        cyberCard: "rgba(17, 24, 39, 0.6)",
        cyberBorder: "rgba(255, 255, 255, 0.06)",
        cyberBorderActive: "rgba(6, 182, 212, 0.25)",
      },
      backgroundImage: {
        'cyber-glow': 'radial-gradient(circle at top, rgba(99, 102, 241, 0.15), transparent 60%)',
        'cmo-glow': 'radial-gradient(circle at center, rgba(6, 182, 212, 0.08), transparent 50%)',
      },
      boxShadow: {
        'cyber-glass': '0 8px 32px 0 rgba(0, 0, 0, 0.5)',
        'cyber-glass-hover': '0 8px 32px 0 rgba(6, 182, 212, 0.12)',
      }
    },
  },
  plugins: [],
}
