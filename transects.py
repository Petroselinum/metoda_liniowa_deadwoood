from math import sin, cos, radians
import matplotlib.pyplot as plt

def transects(num = 1, angle = 0, dist_start = 0, dist_end = 1128, dok = 2):
    '''
    Funkcja tworzy transekty:
    num - liczba transektów
    angle - kąt przesunięcia względem azymutu 0
    dist_start - odległość początku transektu od środka powierzchni
    dist_end - odległość końca transektu od granicy powierzchni
    dok - liczba zwracanych miejsc po przecinku

    Domyślnie zwraca 1 transekt na azymucie 0 i długości 11.28
    '''
    
    angle = radians(angle)

    def calculate_coords():
        return (round(dist_start * sin(angle), dok), round(dist_start * cos(angle), dok)), \
               (round(dist_end * sin(angle), dok), round(dist_end * cos(angle), dok))
    
    if num == 1:
        return calculate_coords()
    
    else:
        angle_delta = radians(360 / num)
        coords_col = []

        for i in range(num):
            res = calculate_coords()
            angle+=angle_delta
            coords_col.append(res)

        return coords_col
    

if __name__ == '__main__':

    res = (transects(num = 6, angle = 0, dist_start=100))
    print(res)
    fig, ax = plt.subplots(figsize = (8,8))

    def wisl_plot():
        A = plt.Circle((0, 0), radius=1128, fill=False, color='black')
        B1 = plt.Circle((0, 0), radius=56, fill=False, color='black', linestyle = '--')
        B2 = plt.Circle((0, 0), radius=259, fill=False, color='black', linestyle = '--')
        ax.plot(0, 0, '.', color = 'black')
        ax.add_patch(A)
        ax.add_patch(B1)
        ax.add_patch(B2)

    if isinstance(res, tuple):
        ax.plot([res[0][0], res[1][0]], [res[0][1], res[1][1]], color = 'tab:blue')
        wisl_plot()
        plt.show()

    else:
        for i in res:
            ax.plot([i[0][0], i[1][0]], [i[0][1], i[1][1]], color = 'tab:blue')
        wisl_plot()
        plt.show()


