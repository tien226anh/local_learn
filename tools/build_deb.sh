#!/bin/bash
# tools/build_deb.sh

APP_NAME="local-learn"
VERSION="0.1.0"
ARCH="amd64"
BUILD_DIR="build/deb/${APP_NAME}_${VERSION}_${ARCH}"
DIST_BIN="dist/${APP_NAME}"

# Ensure we have the binary
if [ ! -f "$DIST_BIN" ]; then
    echo "Error: Binary $DIST_BIN not found. Run 'poetry run pyinstaller ...' first."
    exit 1
fi

# Clean previous build
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR/DEBIAN"
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/share/applications"
# mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/scalable/apps"

# Copy binary
cp "$DIST_BIN" "$BUILD_DIR/usr/bin/$APP_NAME"
chmod +x "$BUILD_DIR/usr/bin/$APP_NAME"

# Create Control File
cat > "$BUILD_DIR/DEBIAN/control" << EOF
Package: $APP_NAME
Version: $VERSION
Section: utils
Priority: optional
Architecture: $ARCH
Maintainer: anhnt226 <tien226anh@gmail.com>
Description: Local Learn Desktop App
 Organize and learn from local video courses effectively.
EOF

# Create Desktop Entry
cat > "$BUILD_DIR/usr/share/applications/${APP_NAME}.desktop" << EOF
[Desktop Entry]
Name=Local Learn
Comment=Local Video Course Organizer
Exec=/usr/bin/${APP_NAME}
Type=Application
Categories=Education;Utils;
Terminal=false
EOF

# Build DEB
dpkg-deb --build "$BUILD_DIR" "dist/${APP_NAME}_${VERSION}_${ARCH}.deb"

echo "Build complete: dist/${APP_NAME}_${VERSION}_${ARCH}.deb"
