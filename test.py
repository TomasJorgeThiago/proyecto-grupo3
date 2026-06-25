import proyecto

def test_contar_combustible():
    assert proyecto.contar_combustible(proyecto.todos_datos(), "2") == 2758
    assert proyecto.contar_combustible(proyecto.todos_datos(), "3") == 2694
    assert proyecto.contar_combustible(proyecto.todos_datos(), "6") == 1090
    assert proyecto.contar_combustible(proyecto.todos_datos(), "19") == 2713
    assert proyecto.contar_combustible(proyecto.todos_datos(), "21") == 2740
    assert proyecto.contar_combustible(proyecto.todos_datos(), "999") == 0  # Combustible inexistente
    assert proyecto.contar_combustible({"idproducto": []}, "") == 0  # Caso de datos vacíos

def test_promedio_combustible():
    assert proyecto.promedio_combustible(proyecto.todos_datos(), "TODO", "2") == 1509.6638868745467
    assert proyecto.promedio_combustible(proyecto.todos_datos(), "TODO", "3") == 1741.2977060133628
    assert proyecto.promedio_combustible(proyecto.todos_datos(), "TODO", "6") == 706.0924036697256
    assert proyecto.promedio_combustible(proyecto.todos_datos(), "TODO", "19") == 1558.6327976409875
    assert proyecto.promedio_combustible(proyecto.todos_datos(), "TODO", "21") == 1761.8082372262775
    assert proyecto.promedio_combustible(proyecto.todos_datos(), "TODO", "999") == 0  # Combustible inexistente
    assert proyecto.promedio_combustible({"provincia": [], "idproducto": [], "precio": []}, "TODO", "2") == 0  # Caso de datos vacíos