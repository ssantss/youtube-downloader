module.exports = {
  apps: [
    {
      name: 'yt-downloader-backend',
      script: './start-backend.sh',
      interpreter: '/bin/bash',
      env: {
        PORT: 8765,
        NODE_ENV: 'production'
      },
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