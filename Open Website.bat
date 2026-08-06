@echo off
REM Serves the site over HTTP instead of file://
REM
REM The old version opened index.html directly. That silently broke every
REM root-absolute path (/assets/..., /services/...) because file:// resolves
REM them against C:\ instead of the site root, and the Arabic translation
REM fetch never worked at all. Serving over HTTP matches how Vercel serves
REM the site, so bugs show up here instead of in production.

start "" http://localhost:8000/
py -m http.server 8000 --directory "%~dp0"
