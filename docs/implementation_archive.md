# Sticky Notes Project

## Decisions

### 1. Custom Drawing for Shadows
- **Reason**: QGraphicsDropShadowEffect caused errors with frameless windows.
- **Outcome**: Implemented custom drawing in `paintEvent`.

### 2. Always-on-Top Feature
- **Reason**: To ensure sticky notes are always visible.
- **Outcome**: Used `Qt.WindowStaysOnTopHint` flag.