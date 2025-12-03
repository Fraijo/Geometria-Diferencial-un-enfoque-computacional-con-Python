from manim import *
import numpy as np
import scipy.integrate as spi
from scipy.interpolate import interp1d

config.background_color = WHITE
config.frame_width = 16
config.frame_height = 9

config.pixel_width = 1920
config.pixel_height = 1080

class tfcp(Scene):

    def construct(self):

        t_min = -4*np.pi
        t_max = 4*np.pi
        N = 10000  # más puntos -> curva suave
        T = np.linspace(t_min, t_max, N)

        #función curvatura
        def k(x):
            return x * np.cos(x) + np.sin(x)

        P = np.array([spi.quad(k, 0, t)[0] for t in T])

        dX = np.cos(P)
        dY = np.sin(P)

        X_raw = spi.cumulative_trapezoid(dX, T, initial=0)
        Y_raw = spi.cumulative_trapezoid(dY, T, initial=0)

        idx0 = np.argmin(np.abs(T - 0))

        X = X_raw - X_raw[idx0]
        Y = Y_raw - Y_raw[idx0]

        fx = interp1d(T, X, kind="cubic")
        fy = interp1d(T, Y, kind="cubic")

        s = ValueTracker(t_min)

        ax = Axes(
            x_range=[np.min(X)-0.25, np.max(X)+0.25, 1],
            y_range=[np.min(Y)-0.25, np.max(Y)+0.25, 1],
            x_length=6,
            y_length=6,
            tips=False,
            axis_config={"color": BLACK, "include_numbers": True},
        )

        caja = SurroundingRectangle(ax, color=BLACK, buff=0.2)
        grafica = VGroup(ax, caja)
        self.add(grafica)

        x0 = fx(t_min)
        y0 = fy(t_min)
        ball = Dot(radius=0.035, color=RED).move_to(ax.c2p(x0, y0))
        self.add(ball)

        path = VMobject(color=RED, stroke_width = 2.5)
        path.set_points_as_corners([ball.get_center(), ball.get_center()])
        self.add(path)

        def update_ball(m):
            t = s.get_value()
            m.move_to(ax.c2p(fx(t), fy(t)))
        ball.add_updater(update_ball)

        def update_path(m):
            new_point = ball.get_center()
            last = m.get_last_point()
            if np.linalg.norm(new_point - last) > 1e-4:
                m.add_points_as_corners([new_point])
        path.add_updater(update_path)

        todo = VGroup(ax, caja, ball, path)
        todo.move_to([0, 0, 0])
        todo.scale(1.25)
        self.add(todo)

        self.play(s.animate.set_value(t_max), run_time=14, rate_func=linear)
        self.wait()
