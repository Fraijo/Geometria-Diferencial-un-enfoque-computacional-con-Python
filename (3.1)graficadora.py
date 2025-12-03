from manim import*

config.background_color = WHITE

config.frame_width = 16
config.frame_height = 9

config.pixel_width = 1920
config.pixel_height = 1080


class helicoide(ThreeDScene):
    def func(self, u, v):
        return np.array([
            v * np.cos(u),
            v * np.sin(u),
            u
            ])

    def construct(self):
        L = 3
        axes = ThreeDAxes(
            x_range=[-L,L,1], x_length=config.frame_height-0.5,
            y_range=[-L,L,1], y_length=config.frame_height-0.5,
            z_range=[-L,L,1], z_length=config.frame_height-0.5
            ).set_color(BLACK)
        surface = Surface(
            lambda u, v: axes.c2p(*self.func(u, v)),
            u_range=[-PI, PI], v_range=[-1, 1],
            resolution=32,  checkerboard_colors = [PINK],
            stroke_width= 0.05, fill_opacity = 0.8
        )
        #self.renderer.camera.light_source.move_to(3*IN) # changes the source of the light
        self.set_camera_orientation(theta= 40 * DEGREES, phi=75* DEGREES, zoom = 1)
        self.add(axes, surface)

class hiperboloide(ThreeDScene):
    def func(self, u, v):
        return np.array([
            np.cosh(u) * np.cos(v),
            np.cosh(u) * np.sin(v),
            np.sinh(u)
            ])

    def construct(self):
        L = 2
        axes = ThreeDAxes(
            x_range=[-L,L,1], x_length=config.frame_height-0.5,
            y_range=[-L,L,1], y_length=config.frame_height-0.5,
            z_range=[-L,L,1], z_length=config.frame_height-0.5
            ).set_color(BLACK)
        surface = Surface(
            lambda u, v: axes.c2p(*self.func(u, v)),
            u_range=[-1, 1], v_range=[0, 2*PI],
            resolution=32,  checkerboard_colors = [GREEN],
            stroke_width= 0.05, fill_opacity = 0.8
        )
        #self.renderer.camera.light_source.move_to(3*IN) # changes the source of the light
        self.set_camera_orientation(theta=60 * DEGREES, phi=60 * DEGREES, zoom = 1)
        self.add(axes, surface)

class toro(ThreeDScene):
    def func(self, u, v):
        R = 5
        r = 2
        return np.array([
            (R + r * np.sin(u)) * np.cos(v),
            (R + r * np.sin(u)) * np.sin(v),
            r * np.cos(u)
            ])

    def construct(self):
        L = 8
        axes = ThreeDAxes(
            x_range=[-L,L,1], x_length=config.frame_height-0.5,
            y_range=[-L,L,1], y_length=config.frame_height-0.5,
            z_range=[-L,L,1], z_length=config.frame_height-0.5
            ).set_color(BLACK)
        surface = Surface(
            lambda u, v: axes.c2p(*self.func(u, v)),
            u_range=[0, 2*PI], v_range=[0, 2*PI],
            resolution=32,  checkerboard_colors = [RED],
            stroke_width= 0.05, fill_opacity = 0.7
        )
        self.renderer.camera.light_source.move_to(3*IN) # changes the source of the light
        self.set_camera_orientation(theta=60 * DEGREES, phi=60 * DEGREES, zoom = 1)
        self.add(axes, surface)
