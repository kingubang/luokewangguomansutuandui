import { defineConfig } from 'unocss'

export default defineConfig({
  shortcuts: {
    'flex-center': 'flex justify-center items-center',
    'flex-between': 'flex justify-between items-center',
    'page-container': 'px-4 py-3'
  },
  theme: {
    colors: {
      primary: '#FF6B35',
      secondary: '#004E89',
      accent: '#FFD700',
      background: '#F5F5F5',
      surface: '#FFFFFF',
      text: '#333333',
      'text-secondary': '#666666',
      'text-light': '#999999'
    }
  },
  rules: [
    [/^fc-(\w+)-(\w+)$/, ([, justify, align]) => `flex justify-${justify} items-${align}`]
  ]
})
