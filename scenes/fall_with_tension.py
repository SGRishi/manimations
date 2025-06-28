from manim import *
import numpy as np

# Use Roboto for all text
config.font = "Roboto"


class TensionDocumentary(Scene):
    """Illustrates how tension changes with both mass and angle."""

    def construct(self):
        title = Text("What is Tension?", font_size=60)
        self.play(Write(title))
        self.play(title.animate.to_corner(UL))

        # Simulation parameters
        initial_mass = 1  # kg
        final_mass = 5    # kg
        rope_length = 2   # meters
        g = 9.8
        total_time = 6

        # Track current time, mass and angle
        t_tracker = ValueTracker(0.0)
        mass_tracker = ValueTracker(initial_mass)
        angle_tracker = ValueTracker(0.0)  # radians

        def mass_func(tau):
            return initial_mass + (final_mass - initial_mass) * (tau / total_time)

        def angle_func(tau):
            # swing left/right over time
            return 0.5 * np.sin(2 * np.pi * tau / total_time)

        mass_tracker.add_updater(lambda m: m.set_value(mass_func(t_tracker.get_value())))
        angle_tracker.add_updater(lambda a: a.set_value(angle_func(t_tracker.get_value())))

        # Ceiling
        ceiling = Rectangle(width=6, height=0.3, fill_opacity=1, color=GRAY)
        ceiling.to_edge(UP)

        def ball_radius():
            return 0.2 + 0.05 * mass_tracker.get_value()

        def ball_position():
            theta = angle_tracker.get_value()
            offset = np.array([
                np.sin(theta),
                -np.cos(theta),
                0,
            ]) * rope_length
            return ceiling.get_bottom() + offset

        ball = Circle(radius=ball_radius(), color=BLUE, fill_opacity=1)
        ball.add_updater(
            lambda m: m.become(
                Circle(radius=ball_radius(), color=BLUE, fill_opacity=1)
            ).move_to(ball_position())
        )

        rope = always_redraw(lambda: Line(ceiling.get_bottom(), ball.get_center(), color=WHITE))
        mass_label = always_redraw(
            lambda: Text(f"{mass_tracker.get_value():.1f} kg", font_size=24).next_to(ball, RIGHT)
        )
        angle_label = always_redraw(
            lambda: Text(f"{np.degrees(angle_tracker.get_value()):.0f}\N{DEGREE SIGN}", font_size=24).next_to(ball, UP)
        )

        self.play(FadeIn(ceiling, ball, rope, mass_label, angle_label))

        formula = MathTex(r"T = \frac{m g}{\cos\theta}", font_size=48)
        formula.next_to(title, DOWN)
        self.play(Write(formula))

        # Axes for tension and angle
        tension_ax = Axes(
            x_range=[0, total_time, 1],
            y_range=[0, final_mass * g * 2, final_mass * g / 5],
            x_length=5,
            y_length=3,
        ).to_corner(UR)
        angle_ax = Axes(
            x_range=[0, total_time, 1],
            y_range=[-60, 60, 30],
            x_length=5,
            y_length=3,
        ).next_to(tension_ax, DOWN, buff=0.7, aligned_edge=RIGHT)

        tension_labels = tension_ax.get_axis_labels(Text("t (s)"), Text("T (N)"))
        angle_labels = angle_ax.get_axis_labels(Text("t (s)"), Text("\u03b8 (deg)"))
        self.play(Create(VGroup(tension_ax, angle_ax)), FadeIn(tension_labels, angle_labels))

        def tension_at(tau: float) -> float:
            m = mass_func(tau)
            theta = angle_func(tau)
            return m * g / np.cos(theta)

        tension_graph = always_redraw(
            lambda: tension_ax.plot(tension_at, x_range=[0, t_tracker.get_value()], color=RED)
        )
        tension_dot = always_redraw(
            lambda: Dot(tension_ax.c2p(t_tracker.get_value(), tension_at(t_tracker.get_value())), color=YELLOW)
        )

        angle_graph = always_redraw(
            lambda: angle_ax.plot(
                lambda tau: np.degrees(angle_func(tau)),
                x_range=[0, t_tracker.get_value()],
                color=GREEN,
            )
        )
        angle_dot = always_redraw(
            lambda: Dot(angle_ax.c2p(t_tracker.get_value(), np.degrees(angle_func(t_tracker.get_value()))), color=YELLOW)
        )

        self.play(FadeIn(tension_graph, tension_dot, angle_graph, angle_dot))

        self.play(t_tracker.animate.set_value(total_time), run_time=total_time, rate_func=linear)
        self.wait()
