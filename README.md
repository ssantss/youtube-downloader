# YouTube Downloader

A modern YouTube video downloader built with Svelte and FastAPI. Features a clean UI, real-time video preview, download history, and seamless YouTube integration via userscript.

## Features

- Real-time URL validation and video preview
- Persistent download history
- Browser integration through userscript
- Clean and responsive interface
- Progress tracking with visual feedback

## Prerequisites

- Node.js (v16 or higher)
- Python (v3.8 or higher)
- Make

## Quick Start

1. **Installation**

```bash
make install
```

This will install all dependencies for both frontend and backend.

2. **Run the application**

```bash
make run
```

The application will be available at:

- Frontend: http://localhost:5270
- Backend: http://localhost:5173

## Browser Integration

1. Install Tampermonkey extension in your browser
2. Import the userscript from `userscript/youtube-downloader.user.js`
3. Visit any YouTube video and you'll see a "DOWNLOAD" button next to the video

## Project Structure

```
frontend/     # Svelte frontend application
backend/      # Python FastAPI backend
userscript/   # YouTube integration script
```

## Development

- Start frontend development server:

For development, you can run the frontend separately:

```bash
cd frontend && npm run dev
```

This will run the frontend on http://localhost:5270

Run the backend server:

```bash
cd backend && python main.py
```

This will run the API on http://localhost:5173

For production, just use `make run` which will serve the frontend through the backend.

## License

MIT

## Credits

Developed by Santiago Jimenez with the assistance of Claude AI (Anthropic).

This project was created as a learning experience combining modern web technologies
and demonstrating the integration between frontend, backend, and browser extensions.
