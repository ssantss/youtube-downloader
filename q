[1mdiff --git a/ecosystem.config.js b/ecosystem.config.js[m
[1mindex 17431a3..e857b60 100644[m
[1m--- a/ecosystem.config.js[m
[1m+++ b/ecosystem.config.js[m
[36m@@ -3,7 +3,7 @@[m [mmodule.exports = {[m
     {[m
       name: 'yt-downloader-backend',[m
       script: 'backend/main.py',[m
[31m-      interpreter: '/home/santiago/code/youtube-downloader/backend/venv/bin/python3',[m
[32m+[m[32m      interpreter: '/home/santiago/code/youtube-downloader/backend/venv/bin/activate',[m
       env: {[m
         PORT: 8765,[m
         NODE_ENV: 'production'[m
