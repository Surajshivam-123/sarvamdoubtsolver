import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const envParent = loadEnv(mode, path.resolve(__dirname, '..'), '');
  const envLocal = loadEnv(mode, __dirname, '');
  const apiKey =
    envLocal.VITE_SARVAM_API_KEY ||
    envLocal.SARVAM_API_KEY ||
    envParent.SARVAM_API_KEY ||
    envParent.VITE_SARVAM_API_KEY ||
    'sk_0vr9gnzo_1deURIBWS66KDr30XVDBOmBw';

  return {
    plugins: [react()],
    envDir: path.resolve(__dirname, '..'),
    define: {
      '__SARVAM_API_KEY__': JSON.stringify(apiKey),
      'process.env.SARVAM_API_KEY': JSON.stringify(apiKey),
    },
    server: {
      port: 3000,
    },
  };
});
