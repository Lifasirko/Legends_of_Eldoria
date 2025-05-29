import pytest
from bot.services.battle_service import calculate_effective_dmg, calculate_final_dmg, simulate_fight


def test_calculate_effective_dmg():
    assert calculate_effective_dmg(120, 30) == 92  # floor(120*100/130)


def test_calculate_final_dmg_no_variation():
    assert calculate_final_dmg(120, 30, random_factor=0) == 92


def test_simulate_fight_player_wins():
    player = {'hp': 100, 'atk': 20, 'def': 5}
    monster = {'hp': 30, 'atk': 10, 'def': 2}
    logs, result = simulate_fight(player, monster, random_factor=0)
    assert result is True
    # Перевіримо, що принаймні один хід був записаний
    assert len(logs) >= 1 