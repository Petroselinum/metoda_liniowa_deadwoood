from shapely.geometry import LineString
from transects import transects
from data import martw_query
import pandas as pd
import polars as pl
import matplotlib.pyplot as plt

def search_crosses(n_transects:int, angle:int, dist_start:int):
    df = martw_query().to_pandas()

    wyniki_list = []

    for i, group in df.groupby('NR_PUNKTU', as_index=False):
        trans = transects(num=n_transects,
                            angle=angle,
                            dist_start=dist_start,
                            dist_end=group.PROMIEN_A.max()) # pobieramy promień pow A bo zmienny od nachylenia

        n_crosses = [0 for _ in range(len(group))]

    # sprawdzamy które martwe kłody przecinają się z każdym transektem oraz zliczamy liczbę przecięć
        for j in trans:
            for k, l in enumerate(group.itertuples()):
                res = LineString([j[0], j[1]]).intersects(LineString([(l.X_start, l.Y_start), (l.X_end, l.Y_end)]))
                if res:
                    n_crosses[k] += 1

        group['przeciecia'] = n_crosses

        wyniki_list.append(group)

    wynik = pd.concat(wyniki_list, axis=0)

    return wynik


if __name__ == '__main__':
    
    n_transects = 3  #liczba transektów - dalszy skrypt zakłada co najmniej 2 transekty
    angle = 30        #kąt przesunięcia/rotacji całego układu
    dist_start = 100   #odległośc początku transektu od środka pow w cm

    wynik = search_crosses(n_transects=n_transects,
                           angle=angle,
                           dist_start=dist_start)

    plot_id = '0340692'
    
    df = martw_query()
    pow = df.filter(pl.col('NR_PUNKTU') == plot_id).to_pandas() #0161001
    crosses = wynik.query('przeciecia > 0 & NR_PUNKTU == @plot_id')
    tran = transects(num = n_transects, 
                     dist_end = pow.PROMIEN_A.max(), 
                     dist_start = dist_start,
                     angle=angle)

    fig, ax = plt.subplots(figsize=(8, 8))
    
    def wisl_plot():
        A = plt.Circle((0, 0), radius=pow.PROMIEN_A.max(), fill=False, color='black')
        B1 = plt.Circle((0, 0), radius=56, fill=False, color='black', linestyle = '--')
        B2 = plt.Circle((0, 0), radius=pow.PROMIEN_B.max(), fill=False, color='black', linestyle = '--')
        ax.plot(0, 0, '.', color = 'black')
        ax.add_patch(A)
        ax.add_patch(B1)
        ax.add_patch(B2)

    
    for row in pow.itertuples():
        ax.plot(
            [row.X_start, row.X_end],
            [row.Y_start, row.Y_end],
            color = "tab:red",
            linewidth = row.D12 * 0.01 #0.01 dopasowuje skalę rysowania
        )
        ax.text(row.X_start, row.Y_start, row.LP, fontdict={'size':6})
    
    for row in crosses.itertuples():
        ax.plot(
            [row.X_start, row.X_end],
            [row.Y_start, row.Y_end],
            color = "tab:green",
            linewidth = row.D12 * 0.01 #0.01 dopasowuje skalę rysowania
        )

    if isinstance(tran, tuple):
            ax.plot([tran[0][0], tran[1][0]], [tran[0][1], tran[1][1]], color = 'tab:blue')
    else:
        for i in tran:
            ax.plot([i[0][0], i[1][0]], [i[0][1], i[1][1]], color = 'tab:blue')
    

    wisl_plot()
    ax.set_aspect('equal')
    plt.show()
