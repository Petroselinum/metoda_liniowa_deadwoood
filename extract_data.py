from intersection import search_crosses
import os

#Warianty testowe (liczba transektów, kąt przesunięcia w stopniach)
warianty_testowe = [
    (2, 0),
    (3, 0),
    (4, 0),
    (5, 0),
    (2, 45),
    (2, 90),
    (3, 30),
    (3, 60),
    (3, 90),
    (4, 0),
    (4, 45),
    (5, 0),
    (6, 0)
]

#Testowane odległości początku transektu od środka w cm

odleglosc = [0, 100, 200, 300]

res_dir = "wyniki_wariantow_transektow"
os.makedirs(res_dir, exist_ok = True)

for odl in odleglosc:
    for n_trans, angle in warianty_testowe:
        res = search_crosses(n_transects=n_trans, angle=angle, dist_start=odl)
        path = os.path.join(res_dir,f'n_trans-{n_trans}_angle-{angle}_odl-{odl}.parquet')
        res.to_parquet(path)
