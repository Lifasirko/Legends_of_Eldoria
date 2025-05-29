from .base import Resource, Enemy, Player, Track

# Початкові ресурси
INITIAL_RESOURCES = [
    Resource(
        name="Гриби",
        description="Свіжі гриби, які можна використовувати для приготування їжі",
        spawn_chance=0.7,
        min_amount=1,
        max_amount=3
    ),
    Resource(
        name="Гілки",
        description="Сухі гілки для розпалу",
        spawn_chance=0.8,
        min_amount=2,
        max_amount=5
    ),
    Resource(
        name="Трава",
        description="Лікарська трава",
        spawn_chance=0.6,
        min_amount=1,
        max_amount=4
    ),
    Resource(
        name="Камінь",
        description="Звичайний камінь",
        spawn_chance=0.5,
        min_amount=1,
        max_amount=2
    )
]

# Початкові вороги
INITIAL_ENEMIES = [
    Enemy(
        name="Вовк",
        hp=50,
        attack=15,
        defense=5,
        exp=20,
        gold=10,
        spawn_chance=0.3,
        track_description="Сліди вовка"
    ),
    Enemy(
        name="Ведмідь",
        hp=100,
        attack=25,
        defense=15,
        exp=50,
        gold=30,
        spawn_chance=0.2,
        track_description="Ведмежі сліди"
    ),
    Enemy(
        name="Бандит",
        hp=80,
        attack=20,
        defense=10,
        exp=40,
        gold=25,
        spawn_chance=0.25,
        track_description="Сліди людини"
    )
]

async def init_initial_data(session):
    """Ініціалізація початкових даних в базі даних"""
    # Додавання ресурсів
    for resource in INITIAL_RESOURCES:
        existing = await session.execute(
            select(Resource).where(Resource.name == resource.name)
        )
        if not existing.scalar_one_or_none():
            session.add(resource)
    
    # Додавання ворогів
    for enemy in INITIAL_ENEMIES:
        existing = await session.execute(
            select(Enemy).where(Enemy.name == enemy.name)
        )
        if not existing.scalar_one_or_none():
            session.add(enemy)
    
    await session.commit() 