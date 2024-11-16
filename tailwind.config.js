import forms from '@tailwindcss/forms'

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './src/components/tailwind/*.vue',
    './src/components/tailwind/**/*.vue',
    './src/App.vue',
    // 其他文件...
  ],
  theme: {
    extend: {
      colors: {
        bg: '#F1F2F3',
      },
    },
    screens: {
      ssm: '0px',
      lm: { max: '640px' },
      ld: { max: '768px' },
      llg: { max: '1023px' },
      sm: '640px',
      smd: '641px',
      md: '768px',
      lg: '1024px',
      xl: '1280px',
      '2xl': '1536px',
    },
  },
  plugins: [forms],
}
