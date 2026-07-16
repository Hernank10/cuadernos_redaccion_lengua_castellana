# Índice de Técnicas de Lengua Castellana

$(sqlite3 tecnicas_lengua.db -header -markdown "SELECT categoria, COUNT(*) as total FROM tecnicas GROUP BY categoria ORDER BY total DESC;")

## Técnicas por categoría

$(sqlite3 tecnicas_lengua.db -header -markdown "SELECT id, titulo, categoria FROM tecnicas ORDER BY categoria, id LIMIT 50;")
