CREATE TABLE hotels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    area TEXT,
    is_open INTEGER,        -- 1:営業中, 0:停止
    food_stock INTEGER,     -- 備蓄食料量 (人数分)
    water_stock INTEGER     -- 備蓄水量 (人数分)
);
