from manim import*
from manim_slides import Slide
import numpy as np
import scipy as sp
import sympy as sy
#nuevas:
import scipy.integrate as sc
from sympy.abc import u, v

config.background_color = WHITE

'''
config.frame_width = 16
config.frame_height = 9

config.pixel_width = 1920
config.pixel_height = 1080
'''
config.frame_width = 10
config.frame_height = 10

config.pixel_width = 1080
config.pixel_height = 1080

def Christoffel_esfera():
    Gamma1 = sy.Matrix([[0, -sy.tan(v)], 
                         [-sy.tan(v), 0]]) 

    Gamma2 = sy.Matrix([[sy.sin(v)*sy.cos(v), 0], 
                         [0, 0]])

    return [Gamma1, Gamma2] 

def f(y, s, C, u_sym, v_sym):
    y0 = y[0]
    y1 = y[1]
    y2 = y[2]
    y3 = y[3]
    dy = np.zeros_like(y)
    dy[0] = y1 
    dy[2] = y3 
    
    Gamma1 = C[0].subs({u_sym: y0, v_sym: y2}) 
    Gamma2 = C[1].subs({u_sym: y0, v_sym: y2}) 

    dy[1] = -(Gamma1[0,0] * y1**2 + 2 * Gamma1[0,1] * y1 * y3 + Gamma1[1,1] * y3**2)
    dy[3] = -(Gamma2[0,0] * y1**2 + 2 * Gamma2[0,1] * y1 * y3 + Gamma2[1,1] * y3**2)
    
    return dy.astype(float) 

def solve_geodesic(C, u0, s0, s1, ds):
    s = np.arange(s0, s1 + ds, ds)
    return sc.odeint(f, u0, s, args=(C, u, v))

class GeodesicaEsfera(ThreeDScene):
    def construct(self):
        
        u0 = [0, 0.1, 0, 0.1] 
        s0 = 0
        s1 = 18 * np.pi
        ds = 0.15
        
        C = Christoffel_esfera()
        X = solve_geodesic(C, u0, s0, s1, ds)
        
        u_geo, v_geo = X[:, 0], X[:, 2]
        x_geo = np.cos(u_geo) * np.cos(v_geo)
        y_geo = np.sin(u_geo) * np.cos(v_geo)
        z_geo = np.sin(v_geo)
        
        geodesic_points = np.vstack([x_geo, y_geo, z_geo]).T
        
        self.set_camera_orientation(
            phi=70 * DEGREES, 
            theta=220 * DEGREES,
            zoom = 1.75
        ) 
        self.camera.background_color = BLACK #"#202020"

        axes = ThreeDAxes(
            x_range=(-1.5, 1.5, 0.5), y_range=(-1.5, 1.5, 0.5), z_range=(-1.5, 1.5, 0.5), 
            x_length=3, y_length=3, z_length=3
        ).set_opacity(0.5)

        def esfera_func(u_val, v_val):
            x = np.cos(u_val) * np.cos(v_val)
            y = np.sin(u_val) * np.cos(v_val)
            z = np.sin(v_val)
            return np.array([x, y, z])

        esfera = Surface(
            esfera_func,
            u_range=[0, 2 * np.pi],
            v_range=[-np.pi / 2, np.pi / 2],
            resolution=(40, 40),
            fill_opacity=0.6,
            checkerboard_colors=[BLUE_D, BLUE_E],
            stroke_color=WHITE,
            stroke_width=0.2
        )
    
        geodesic_line = VMobject()
        geodesic_line.set_points_as_corners(geodesic_points)
        geodesic_line.set_stroke(color=RED, width=5)
        geodesic_line.set_shade_in_3d(True)

        start_point = Sphere(
            radius=0.05,
            color=YELLOW,
            resolution=10
        ).move_to(geodesic_points[0])

        title = MathTex(
            r"\text{Geodésica en la Esfera } R=1",
            font_size=50
        ).to_corner(UP + LEFT)
        
        params_text = MathTex(
            r"\gamma(s) = (u(s), v(s)) \quad (u_0, u'_0, v_0, v'_0) = (0, 0.1, 0, 0.1)",
            font_size=30
        ).next_to(title, DOWN, aligned_edge=LEFT)

        self.add_fixed_in_frame_mobjects(title, params_text) 
        
        self.play(Create(axes), run_time=1)
        self.play(Create(esfera), run_time=2)
        self.play(Create(start_point), run_time=0.5)

        self.play(
            ShowPassingFlash(geodesic_line, time_width=0.4, run_time=7, color=RED, rate_func=linear),
            MoveAlongPath(start_point, geodesic_line, run_time=7, rate_func=linear), 
        )
        
        self.add(geodesic_line) 
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(5)
        self.stop_ambient_camera_rotation()
        
        self.wait(1)


#TORO

R_toro = 1.5
r_toro = 0.5

def Christoffel_toro(R=R_toro, r=r_toro):
    Gamma1_uv = -r * sy.sin(v) / (R + r * sy.cos(v))
    Gamma2_uu = -(R + r * sy.cos(v)) * sy.cos(v) / r
    
    Gamma1 = sy.Matrix([[0, Gamma1_uv], 
                     [Gamma1_uv, 0]]) 

    Gamma2 = sy.Matrix([[Gamma2_uu, 0], 
                     [0, 0]])

    return [Gamma1, Gamma2] 

def f(y, s, C, u_sym, v_sym):
    y0 = y[0]
    y1 = y[1]
    y2 = y[2]
    y3 = y[3]
    dy = np.zeros_like(y)
    dy[0] = y1 
    dy[2] = y3 
    
    Gamma1 = C[0].subs({u_sym: y0, v_sym: y2}) 
    Gamma2 = C[1].subs({u_sym: y0, v_sym: y2}) 

    dy[1] = -(Gamma1[0,0] * y1**2 + 2 * Gamma1[0,1] * y1 * y3 + Gamma1[1,1] * y3**2)
    dy[3] = -(Gamma2[0,0] * y1**2 + 2 * Gamma2[0,1] * y1 * y3 + Gamma2[1,1] * y3**2)
    
    return dy.astype(float) 

def solve_geodesic(C, u0, s0, s1, ds):
    s = np.arange(s0, s1 + ds, ds)
    return sc.odeint(f, u0, s, args=(C, u, v))

class GeodesicaToro(ThreeDScene):
    def construct(self):
        
        u0 = [0.0, 0.5, 0.0, 0.5] 
        s0 = 0
        s1 = 15 * np.pi 
        ds = 0.1
        
        C = Christoffel_toro(R_toro, r_toro)
        X = solve_geodesic(C, u0, s0, s1, ds)
        
        u_geo, v_geo = X[:, 0], X[:, 2]
        x_geo = (R_toro + r_toro * np.cos(v_geo)) * np.cos(u_geo)
        y_geo = (R_toro + r_toro * np.cos(v_geo)) * np.sin(u_geo)
        z_geo = r_toro * np.sin(v_geo)
        
        geodesic_points = np.vstack([x_geo, y_geo, z_geo]).T
        
        #self.set_camera_orientation(phi=75 * DEGREES, theta=270 * DEGREES, zoom = 2) 

        axes = ThreeDAxes(
            x_range=(-3, 3, 1), y_range=(-3, 3, 1), z_range=(-1.5, 1.5, 1), 
            x_length=6, y_length=6, z_length=3
        ).set_opacity(1)
        axes.set_color(BLACK)
        self.add(axes)

        def toro_func(u_val, v_val):
            x = (R_toro + r_toro * np.cos(v_val)) * np.cos(u_val)
            y = (R_toro + r_toro * np.cos(v_val)) * np.sin(u_val)
            z = r_toro * np.sin(v_val)
            return np.array([x, y, z])

        toro = Surface(
            toro_func,
            u_range=[0, 2 * np.pi],
            v_range=[0, 2 * np.pi],
            resolution=(60, 30), 
            fill_opacity=0.4,
            checkerboard_colors=["#e290c7ff"],
            stroke_color=WHITE,
            stroke_width=0.1
        )
        
        geodesic_line = VMobject()
        geodesic_line.set_points_as_corners(geodesic_points)
        geodesic_line.set_stroke(color="#5adb3aff", width=2.5)
        geodesic_line.set_shade_in_3d(True)

        start_point = Sphere(
            radius=0.05,
            color=YELLOW,
            resolution=10
        ).move_to(geodesic_points[0])

        title = MathTex(
            r"\text{Geodésica en el Toro } (R=1.5, r=0.5)",
            font_size=50
        ).to_corner(UP + LEFT)
        
        params_text = MathTex(
            r"(u_0, u'_0, v_0, v'_0) = (0, 0.5, 0, 0.5)",
            font_size=30
        ).next_to(title, DOWN, aligned_edge=LEFT)
        
        '''
        self.add_fixed_in_frame_mobjects(title, params_text) 
        
        self.play(Create(toro), run_time=3)
        self.play(Create(start_point), run_time=0.5)

        self.play(
            ShowPassingFlash(geodesic_line, time_width=0.4, run_time=7, color=RED, rate_func=linear),
            MoveAlongPath(start_point, geodesic_line, run_time=7, rate_func=linear), 
        )
        
        self.add(geodesic_line) 
        
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(5)
        self.stop_ambient_camera_rotation()
        
        self.wait(1)
        '''
        self.set_camera_orientation(theta=50 * DEGREES, phi=70 * DEGREES, zoom=1.9)
        self.add(toro, geodesic_line)

#AGNESI

u, v = sy.symbols('u v')

a_agnesi = 1.0

def Christoffel_agnesi(a=a_agnesi):
    """
    Símbolos de Christoffel de segunda especie para la
    Bruja de Agnesi (parametrización: r = (2a/(1+u^2), u, v)).

    Métrica:
    E = g_uu = (4 * a**2 * 4 * u**2) / (1 + u**2)**4 + 1
    G = g_vv = (4 * a**2) / (1 + u**2)**2
    F = g_uv = 0
    """
    f = 2 * a / (1 + u**2)
    f_prime = sy.diff(f, u)  # -4a*u / (1 + u**2)**2
    g_prime = 1  # 1
    
    E = sy.simplify(f_prime**2 + g_prime**2) 
    G = f**2
    
    E_u = sy.diff(E, u)
    G_u = sy.diff(G, u)
    
    
    
    # Gamma^1 (i=1)
    # Gamma^1_uu = 1/(2E) * E_u
    Gamma1_uu = sy.Rational(1, 2) * (1 / E) * E_u
    # Gamma^1_vv = -1/(2E) * G_u
    Gamma1_vv = sy.Rational(-1, 2) * (1 / E) * G_u
    # Gamma^1_uv = Gamma^1_vu = 0 (por ser F=0)

    # Gamma^2 (i=2)
    # Gamma^2_uv = Gamma^2_vu = 1/(2G) * G_u
    Gamma2_uv = sy.Rational(1, 2) * (1 / G) * G_u
    # Gamma^2_uu = Gamma^2_vv = 0 (por ser F=0)
    
    Gamma1 = sy.Matrix([
        [Gamma1_uu, 0], 
        [0, Gamma1_vv]
    ]) 

    Gamma2 = sy.Matrix([
        [0, Gamma2_uv], 
        [Gamma2_uv, 0]
    ])

    return [Gamma1, Gamma2] 

def f(y, s, C, u_sym, v_sym):
    """
    Sistema de 4 EDOs de primer orden para las geodésicas.
    """
    y0, y1, y2, y3 = y
    dy = np.zeros_like(y)
    dy[0] = y1  # u'
    dy[2] = y3  # v'
    
    # Sustitución de variables simbólicas
    Gamma1 = C[0].subs({u_sym: y0, v_sym: y2}) 
    Gamma2 = C[1].subs({u_sym: y0, v_sym: y2}) 

    # Ecuaciones geodésicas (u'' = dy[1], v'' = dy[3])
    dy[1] = -(Gamma1[0,0] * y1**2 + 2 * Gamma1[0,1] * y1 * y3 + Gamma1[1,1] * y3**2)
    dy[3] = -(Gamma2[0,0] * y1**2 + 2 * Gamma2[0,1] * y1 * y3 + Gamma2[1,1] * y3**2)
    
    return dy.astype(float) 

def solve_geodesic(C, u0, s0, s1, ds):
    s = np.arange(s0, s1 + ds, ds)
    # u0 = [u(0), u'(0), v(0), v'(0)]
    return sc.odeint(f, u0, s, args=(C, u, v))

class GeodesicaBrujaAgnesi(ThreeDScene):
    def construct(self):
        
        # --- Parámetros de la Geodésica ---
        # u0 = [u(0), u'(0), v(0), v'(0)]
        # u (el eje z) va de -inf a inf, v es el ángulo [0, 2pi]
        u0 = [1.0, 0.5, 0.0, 0.5] 
        s0 = 0
        s1 = 15  # Longitud de arco
        ds = 0.1
        
        C = Christoffel_agnesi(a_agnesi)
        
        X = solve_geodesic(C, u0, s0, s1, ds)
        
        u_geo, v_geo = X[:, 0], X[:, 2]
        
        # --- Parametrización de la Bruja de Agnesi ---
        # x = (2a / (1+u^2)) * cos(v)
        # y = (2a / (1+u^2)) * sin(v)
        # z = u
        factor_x_y = 2 * a_agnesi / (1 + u_geo**2)
        x_geo = factor_x_y * np.cos(v_geo)
        y_geo = factor_x_y * np.sin(v_geo)
        z_geo = u_geo
        
        geodesic_points = np.vstack([x_geo, y_geo, z_geo]).T
        
        
        #self.set_camera_orientation(phi=60 * DEGREES, theta=270 * DEGREES, zoom = 0.9) 
        #self.camera.background_color = BLACK # "#202020"

        axes = ThreeDAxes(
             x_range=(-3, 3, 1), y_range=(-3, 3, 1), z_range=(-3.5, 3.5, 1), 
             x_length=6, y_length=6, z_length=7
        ).set_opacity(1)
        axes.set_color(BLACK)
        self.add(axes)

        def agnesi_func(u_val, v_val):
            factor_xy = 2 * a_agnesi / (1 + u_val**2)
            x = factor_xy * np.cos(v_val)
            y = factor_xy * np.sin(v_val)
            z = u_val
            return np.array([x, y, z])

        bruja_agnesi = Surface(
            agnesi_func,
            u_range=[-3, 3],
            v_range=[0, 2 * np.pi],
            resolution=(60, 30), 
            fill_opacity=0.6,
            checkerboard_colors=[BLUE_B, TEAL],
            stroke_color=WHITE,
            stroke_width=0.1
        )
        
        geodesic_line = VMobject()
        geodesic_line.set_points_as_corners(geodesic_points)
        geodesic_line.set_stroke(color=RED_E, width=5)
        geodesic_line.set_shade_in_3d(True)

        start_point = Sphere(
            radius=0.07,
            color=YELLOW,
            resolution=10
        ).move_to(geodesic_points[0])

        title = MathTex(
            r"\text{Geodésica en la Bruja de Agnesi } (a=1)",
            font_size=50
        ).to_corner(UP + LEFT)
        
        params_text = MathTex(
            r"(u_0, u'_0, v_0, v'_0) = (1.0, 0.5, 0.0, 0.5)",
            font_size=30
        ).next_to(title, DOWN, aligned_edge=LEFT)

        '''
        self.add_fixed_in_frame_mobjects(title, params_text) 
        
        self.play(Create(bruja_agnesi), run_time=3)
        self.play(Create(start_point), run_time=0.5)

        self.play(
            ShowPassingFlash(geodesic_line, time_width=0.4, run_time=7, color=RED, rate_func=linear),
            MoveAlongPath(start_point, geodesic_line, run_time=7, rate_func=linear), 
        )
        
        self.add(geodesic_line) 
        
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(5)
        '''
        self.set_camera_orientation(theta=140 * DEGREES, phi=70 * DEGREES, zoom=1.4)
        self.add(bruja_agnesi, geodesic_line)