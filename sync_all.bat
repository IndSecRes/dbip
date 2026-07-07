@echo off
echo ========================================
echo  DBIP Sync - Gitea + GitHub
echo ========================================
cd C:\Users\Gaurav\Desktop\dbip

echo.
echo 📦 Adding changes...
git add .

echo.
echo 📝 Committing changes...
git commit -m "Auto sync: %date% %time%"

echo.
echo 🚀 Pushing to Gitea...
git push gitea master

echo.
echo 🚀 Pushing to GitHub...
git push github master

echo.
echo ========================================
echo ✅ Sync complete!
echo ========================================
pause