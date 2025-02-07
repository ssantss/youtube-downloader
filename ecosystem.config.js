module.exports = {
  apps: [
    {
      name: 'yt-downloader-backend',
      script: 'make',
      args: 'run-backend',
      watch: false,
      autorestart: true,
      max_memory_restart: '1G'
    },
    {
      name: 'yt-downloader-frontend',
      cwd: 'frontend',
      script: 'npm',
      args: 'run start',
      env: {
        PORT: 5270,
        VITE_PORT: 5270,
        NODE_ENV: 'production'
      },
      watch: false,
      autorestart: true,
      max_memory_restart: '500M'
    }
  ]
}; 