## Auth
- POST `/api/auth/register/`     → Register a new user
- POST `/api/auth/login/`        → Login, returns JWT tokens
- POST `/api/auth/logout/`       → Logout, blacklists refresh token
- GET  `/api/auth/me/`           → Get logged in user info
- POST `/api/auth/token/refresh/` → Refresh access token

## Profile
- GET   `/api/profile/`          → Get user profile + total BrainlyCoins
- PATCH `/api/profile/`          → Update profile (username, avatar)
- GET   `/api/profile/coins/`    → Get full BrainlyCoins history
- POST `/api/profile/coins/add/` → Internal endpoint to add coins (called by game logic later)

## Games
- GET  `/api/games/`                        → List all active games
- GET  `/api/games/<slug>/`                 → Get single game details
- POST `/api/games/<slug>/submit-score/`    → Submit a score (protected)
- GET  `/api/games/<slug>/my-scores/`       → Get logged in user's score history for a game

## Leaderboard
- GET `/api/leaderboard/`              → Global leaderboard (top 50 by total score)
- GET `/api/leaderboard/<game_slug>/`  → Per game leaderboard (top 50)