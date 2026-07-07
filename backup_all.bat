@echo off
echo ========================================
echo  DBIP Backup - All Locations
echo ========================================
cd C:\Users\Gaurav\Desktop\dbip

echo.
echo 📦 Adding changes...
git add .

echo.
echo 📝 Committing changes...
git commit -m "Backup: %date% %time%"

echo.
echo 🚀 Pushing to Gitea...
git push gitea master

echo.
echo 🚀 Pushing to GitHub...
git push github master

echo.
echo ========================================
echo ✅ Backup complete!
echo 📁 Local: C:\Users\Gaurav\Desktop\dbip
echo 🌐 Gitea: http://localhost:3000/admin/dbip
echo ☁️ GitHub: https://github.com/IndSecRes/dbip
echo 🌍 Cloudflare: Your tunnel URL
echo ========================================
pause   