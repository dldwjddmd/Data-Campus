import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [vue()],
    resolve: {
        alias: {
            '/@': path.resolve(__dirname, './src'),
            '/@components': path.resolve(__dirname, './src/components'),
            '/@compositions': path.resolve(__dirname, './src/compositions'),
            '/@modules': path.resolve(__dirname, './src/modules'),
            '/@router': path.resolve(__dirname, './src/router'),
            '/@types': path.resolve(__dirname, './src/types'),
            '/@secrets': path.resolve(__dirname, './src/secrets.json'),
        }
    }
})