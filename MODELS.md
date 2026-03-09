## Users (Django's built-in model - no need to create manually)
- id → BigAutoField(PK, auto)
- password → CharField(max_length=128) ← Django stores hashed passwords
- last_login → DateTimeField(null=True, blank=True)
- is_superuser → BooleanField(default=False)
- username → CharField(max_length=150, unique=True)
- first_name → CharField(max_length=150, blank=True)
- last_name → CharField(max_length=150, blank=True)
- email → EmailField(max_length=254, blank=True)
- is_staff → BooleanField(default=False)
- is_active → BooleanField(default=True)
- date_joined → DateTimeField(default=timezone.now)

## UserProfile
- id            → BigAutoField(PK, auto)
- user_id       → OneToOneField → Users(FK, on_delete=CASCADE)
- avatar        → URLField(max_length=500, blank=True, null=True)
- brainlycoins  → IntegerField(default=0)
- created_at    → DateTimeField(auto_now_add=True)

## Games
- id            → BigAutoField(PK, auto)
- name          → CharField(max_length=100)
- slug          → SlugField(max_length=100, unique=True)
- description   → TextField(blank=True)
- is_active     → BooleanField(default=True)
- created_at    → DateTimeField(auto_now_add=True)

## Scores
- id            → BigAutoField(PK, auto)
- user_id       → ForeignKey → Users(FK, on_delete=CASCADE)
- game_id       → ForeignKey → Games(FK, on_delete=CASCADE)
- score         → IntegerField()
- submitted_at  → DateTimeField(auto_now_add=True)

## BrainlyCoins
- id            → BigAutoField(PK, auto)
- user_id       → ForeignKey → Users(FK, on_delete=CASCADE)
- coins_earned  → IntegerField()
- reason        → CharField(max_length=255)
- created_at    → DateTimeField(auto_now_add=True)

## Leaderboard → derived from Scores (query-based, no separate table)

## Items
- id            → BigAutoField(PK, auto)
- name          → CharField(max_length=100)
- type          → CharField(max_length=50)   ← "skin" or "item"
- price_coins   → IntegerField()
- image_url     → URLField(max_length=500)
- is_available  → BooleanField(default=True)

## UserInventory
- id            → BigAutoField(PK, auto)
- user_id       → ForeignKey → Users(FK, on_delete=CASCADE)
- item_id       → ForeignKey → Items(FK, on_delete=CASCADE)
- purchased_at  → DateTimeField(auto_now_add=True)

## Transactions
- id            → BigAutoField(PK, auto)
- user_id       → ForeignKey → Users(FK, on_delete=CASCADE)
- item_id       → ForeignKey → Items(FK, on_delete=CASCADE)
- coins_spent   → IntegerField()
- created_at    → DateTimeField(auto_now_add=True)