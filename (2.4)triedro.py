from manim import*
from manim_slides import Slide
import numpy as np
import scipy as sp
import sympy as sy

config.background_color = WHITE

config.frame_width = 16
config.frame_height = 9

config.pixel_width = 1920
config.pixel_height = 1080

class triedroF(ThreeDScene):

    def setup(self):

        u = sy.symbols("u", real=True)

        #función
        x = (sy.cos(5*u) + 1.5) * sy.cos(2*u)
        y = (sy.cos(5*u) + 1.5) * sy.sin(2*u)
        z = - sy.sin(5*u)

        self.r_sym = sy.Matrix([x, y, z]) #función convertida a sympy

        self.r1_sym = self.r_sym.diff(u) #primera derivada
        self.r2_sym = self.r1_sym.diff(u) #segunda derivada
        
        #conversión a numpy para agilizar el cálculo
        self.r = sy.lambdify(u, self.r_sym, "numpy")
        self.r1 = sy.lambdify(u, self.r1_sym, "numpy")
        self.r2 = sy.lambdify(u, self.r2_sym, "numpy")

    def frenet(self, u):
        #relaciones dentro del triedro
        r = np.array(self.r(u), dtype=float).reshape(3)
        r1 = np.array(self.r1(u), dtype=float).reshape(3)
        r2 = np.array(self.r2(u), dtype=float).reshape(3)

        T = r1 / np.linalg.norm(r1)

        Bn = np.cross(r1, r2)
        nb = np.linalg.norm(Bn)
        if nb < 1e-10:
            B = np.zeros(3)
        else:
            B = Bn / nb

        N = np.cross(B, T)

        return r, T, N, B

    def construct(self):
        L = 3
        axes = ThreeDAxes(
            x_range=[-L, L, 1], x_length=config.frame_height - 0.5,
            y_range=[-L, L, 1], y_length=config.frame_height - 0.5,
            z_range=[-L, L, 1], z_length=config.frame_height - 0.5
        ).set_color(BLACK)

        self.add(axes)

        curva = always_redraw(
            lambda: ParametricFunction(
                lambda u: axes.c2p(*np.array(self.r(u), dtype=float).reshape(3)),
                t_range=[0, 2*PI],
                color=ORANGE
            )
        )
        self.add(curva)

        s = ValueTracker(0)

        punto = always_redraw(
            lambda: Dot3D(
                axes.c2p(*self.r(s.get_value()).reshape(3)),
                color=RED,
                radius=0.08
            )
        )
        self.add(punto)

        tangente = always_redraw(
            lambda: Arrow3D(
                punto.get_center(),
                punto.get_center() + axes.c2p(*self.frenet(s.get_value())[1]),
                color=BLUE
            )
        )

        normal = always_redraw(
            lambda: Arrow3D(
                punto.get_center(),
                punto.get_center() + axes.c2p(*self.frenet(s.get_value())[2]),
                color=RED
            )
        )

        binormal = always_redraw(
            lambda: Arrow3D(
                punto.get_center(),
                punto.get_center() + axes.c2p(*self.frenet(s.get_value())[3]),
                color=GREEN
            )
        )

        self.add(VGroup(tangente, normal, binormal))

        self.renderer.camera.light_source.move_to(3 * IN)
        self.set_camera_orientation(theta=70*DEGREES, phi=75*DEGREES)
        self.begin_ambient_camera_rotation(rate=30*DEGREES, about="theta")

        self.play(
            s.animate.set_value(2*PI),
            run_time=3,
            rate_func=linear
        )
