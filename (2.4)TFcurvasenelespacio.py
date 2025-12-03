from manim import*
import numpy as np
from scipy.integrate import solve_ivp
import pandas as pd

config.background_color = WHITE
config.frame_width = 16
config.frame_height = 9

config.pixel_width = 1920
config.pixel_height = 1080

def frenet_serret(s, y):
    T = y[0:3]
    N = y[3:6]
    B = y[6:9]
    r = y[9:12]

    k = 10 * (np.sin(np.pi * s))**2 #curvatura
    t = 3 * np.cos(np.pi * s) #torsión

    #sistema de ecuaciones
    dTds = k * N
    dNds = -k * T + t * B
    dBds = -t * N
    drds = T

    return np.concatenate([dTds, dNds, dBds, drds])

# Condiciones iniciales
T0 = np.array([1, 0, 0])
N0 = np.array([0, 1, 0])
B0 = np.array([0, 0, 1])
r0 = np.array([0, 0, 0])
y0 = np.concatenate([T0, N0, B0, r0])

# Intervalo de integración
s_span = (-2 * np.pi, 2 * np.pi)
s_eval = np.linspace(*s_span, 700)

# Resolver el sistema
sol = solve_ivp(frenet_serret, s_span, y0, t_eval=s_eval, method='RK45')

# Extraer la curva
r = sol.y[9:12].T  # Transpuesta para tener las filas como puntos

# Guardar en CSV
df = pd.DataFrame(r, columns=["x", "y", "z"])
df.to_csv("curva_frenet_serret.csv", index=False)

print("Archivo 'curva_frenet_serret.csv' guardado.")

class tfce(ThreeDScene):

    def construct(self):
        self.set_camera_orientation(theta=60 * DEGREES, phi= 75 * DEGREES, zoom = 1)
        L = 2.1
        ax = ThreeDAxes(
            x_range=[-1 * L, L, 1], x_length=config.frame_height-1,
            y_range=[-1 * L, L, 1], y_length=config.frame_height-1,
            z_range=[-1 * L, L, 1], z_length=config.frame_height-1,
            tips=False,
        ).set_color(BLACK)
        xya = ax.get_axis_labels().set_color(BLACK)
        self.add(ax,xya)

        df = pd.read_csv("curva_frenet_serret.csv")
        dots = [Dot3D(ax.c2p(x, y, z), color= BLUE,radius=0.035) for x, y, z in df.values]
        for dot in dots:
            self.add(dot)