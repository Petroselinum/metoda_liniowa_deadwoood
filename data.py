from WislDbCon import connection
from WislDb import DRZEWA_MARTWE, ADRES_POW, POW_A_B, OBL_DRZEWA_MARTWE
from sqlalchemy import select
from transects import transects
import polars as pl
import matplotlib.pyplot as plt

def martw_query():

    engine = connection()

    with engine.begin() as con:
        stmt = select(DRZEWA_MARTWE.ID,
                    DRZEWA_MARTWE.LP,
                    DRZEWA_MARTWE.NR_PUNKTU,
                    DRZEWA_MARTWE.NR_PODPOW,
                    DRZEWA_MARTWE.GAT,
                    DRZEWA_MARTWE.AZYMUT,
                    DRZEWA_MARTWE.ODL,
                    DRZEWA_MARTWE.AZYMUT_PNIA,
                    DRZEWA_MARTWE.HL,
                    DRZEWA_MARTWE.D12,
                    OBL_DRZEWA_MARTWE.MIAZSZOSC,
                    DRZEWA_MARTWE.ROZL,
                    POW_A_B.PROMIEN_A,
                    POW_A_B.PROMIEN_B
                    ) \
                .join(ADRES_POW, (ADRES_POW.NR_CYKLU == DRZEWA_MARTWE.NR_CYKLU) &
                                (ADRES_POW.NR_PODPOW == DRZEWA_MARTWE.NR_PODPOW)) \
                .join(POW_A_B, (POW_A_B.NR_CYKLU == DRZEWA_MARTWE.NR_CYKLU) &
                            (POW_A_B.NR_PODPOW == DRZEWA_MARTWE.NR_PODPOW)) \
                .join(OBL_DRZEWA_MARTWE, DRZEWA_MARTWE.ID == OBL_DRZEWA_MARTWE.ID) \
                .where(DRZEWA_MARTWE.NR_CYKLU == 4,
                    ADRES_POW.STATUS_GRUNTU == 1,        #Bierzemy tylko status gruntu 1
                    DRZEWA_MARTWE.TYP.in_([1, 2, 3]),    #Drewno leżące
                    DRZEWA_MARTWE.D12.isnot(None))       #Odfiltrowanie brakujących danych - to do wyjaśnienia
        
        res = con.execute(stmt).all()

    df = pl.DataFrame(res)
    df = df.with_columns(
        HL = pl.col('HL') * 100
    )
    df = df.with_columns([
            (pl.col("ODL") * pl.col("AZYMUT").radians().sin()).round(2).alias("X_start"),
            (pl.col("ODL") * pl.col("AZYMUT").radians().cos()).round(2).alias("Y_start"),
        ]).with_columns([
            (pl.col("X_start") + (pl.col("HL") * pl.col("AZYMUT_PNIA").radians().sin()).round(2)).alias("X_end"),
            (pl.col("Y_start") + (pl.col("HL") * pl.col("AZYMUT_PNIA").radians().cos()).round(2)).alias("Y_end"),
        ])
    
    return df

if __name__ == '__main__':
    df = martw_query()
    pow = df.filter(pl.col('NR_PUNKTU') == '0340692').to_pandas() #0161001
    tran = transects(num = 3, dist_end = pow.PROMIEN_A.max(), dist_start = 100)

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
    

    if isinstance(tran, tuple):
            ax.plot([tran[0][0], tran[1][0]], [tran[0][1], tran[1][1]], color = 'tab:blue')
    else:
        for i in tran:
            ax.plot([i[0][0], i[1][0]], [i[0][1], i[1][1]], color = 'tab:blue')
    

    wisl_plot()
    ax.set_aspect('equal')
    plt.show()
