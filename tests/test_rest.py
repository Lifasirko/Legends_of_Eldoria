from bot.services.rest_service import calculate_rest


def test_calculate_rest_full_restore():
    # Якщо поточне HP мале, за 10 годин відпочинку має відновитись до max
    new_hp, new_mp = calculate_rest(current_hp=10, max_hp=100, current_mp=5, max_mp=50, hours=10)
    assert new_hp == 100
    assert new_mp == 50


def test_calculate_rest_partial():
    new_hp, new_mp = calculate_rest(current_hp=40, max_hp=100, current_mp=10, max_mp=50, hours=2)
    # HP += 100*0.1*2 = 20
    assert new_hp == 60
    # MP += 50*0.15*2 = 15
    assert new_mp == 25 