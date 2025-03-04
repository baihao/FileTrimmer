pyinstaller \
  --name "FileTrimmer" \
  --windowed \
  --onefile \
  --add-data="templates:templates" \
  --hidden-import=flask \
  --osx-bundle-identifier com.pangbao.FileTrimmer \
  desktop_app.py
