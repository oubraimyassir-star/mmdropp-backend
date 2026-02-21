@echo off
echo [1/3] Ajout de vercel.json et core updates...
git add vercel.json main.py
echo [2/3] Commit des changements...
git commit -m "Fix: CORS and Health Check for Live Sync"
echo [3/3] Envoi vers GitHub...
git push origin main
echo ---
echo Termine ! Allez sur Vercel ou Render et attendez le "Live".
pause
