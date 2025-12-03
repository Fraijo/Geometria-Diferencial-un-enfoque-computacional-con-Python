from manim import*
import numpy as np
import sympy as sy

config.background_color = WHITE

config.frame_width = 16
config.frame_height = 9

config.pixel_width = 1920
config.pixel_height = 1080



def plano_tangente():
    u, v = sy.symbols('u v')
    f_expr = u**2 + v**2

    fu = sy.diff(f_expr, u)
    fv = sy.diff(f_expr, v)

    u0, v0 = 1, 1
    f0 = f_expr.subs({u: u0, v: v0})
    fu0 = fu.subs({u: u0, v: v0})
    fv0 = fv.subs({u: u0, v: v0})

    z_tangent_expr = f0 + fu0 * (u - u0) + fv0 * (v - v0)
    z_tangent_func = sy.lambdify((u, v), z_tangent_expr, 'numpy')

    def plano_func(u_vals, v_vals):
        return np.array([u_vals, v_vals, z_tangent_func(u_vals, v_vals)])
    
    return plano_func

class PlanoTangente(ThreeDScene):
    
    def func(self, u, v):
        return np.array([u, v, u**2 +v**2])

    def construct(self):

        u0, uf = -1, 1.5
        v0, vf = -1, 1.5

        l = 2.5
        
        axes = ThreeDAxes(
            x_range=[-l,l, int(l)], x_length=config.frame_height-0.5,
            y_range=[-l,l, int(l)], y_length=config.frame_height-0.5,
            z_range=[-l,l, int(l)], z_length=config.frame_height-0.5
            ).set_color(BLACK)

        self.set_camera_orientation(theta=-25 * DEGREES, phi=75 * DEGREES, zoom = 1.2)

        superficie = Surface(
            lambda u, v: axes.c2p(*self.func(u,v)),
            u_range=[u0, uf],
            v_range=[v0, vf],
            resolution=64,
            checkerboard_colors = [RED],
            fill_opacity=0.9,
            stroke_width = 0.1,
        )

        plano_func = plano_tangente()
        plano = Surface(
            lambda u, v: axes.c2p(*plano_func(u, v)),
            u_range=[u0, uf],
            v_range=[v0, vf],
            resolution=64,
            checkerboard_colors = [YELLOW],
            fill_opacity=0.8,
            stroke_width = 0.1,
        )

        punto = Dot3D(axes.c2p(*self.func(1,1)), color=RED)

        self.add(axes, superficie, plano, punto)