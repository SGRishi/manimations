from manim import *
import numpy as np

# Use Roboto for all text
config.font = "Roboto"

class TensionDocumentary(Scene):
    def construct(self):
        title = Text("What is Tension?", font_size=72)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_corner(UL))

        # Parameters
        initial_mass = 1  # kg
        final_mass = 5    # kg
        total_time = 4    # seconds
        g = 9.8
        rope_length = 2

        t_tracker = ValueTracker(0.0)

        # Ceiling and object
        ceiling = Rectangle(width=6, height=0.3, fill_opacity=1, color=GRAY)
        ceiling.to_edge(UP)

        def current_mass():
            return initial_mass + (final_mass - initial_mass) * (t_tracker.get_value() / total_time)

        def ball_mobject():
            radius = 0.3 * current_mass()
            return (
                Circle(radius=radius, color=BLUE, fill_opacity=1)
                .next_to(ceiling, DOWN, buff=rope_length)
            )

        ball = always_redraw(ball_mobject)
        rope = always_redraw(lambda: Line(ceiling.get_bottom(), ball.get_top(), color=WHITE))
        mass_label = always_redraw(
            lambda: Text(f"{current_mass():.1f} kg", font_size=24).next_to(ball, RIGHT)
        )

        self.play(FadeIn(ceiling, ball, rope, mass_label))

        # Tension formula
        formula = Text("T = m g", font_size=48)
        formula.next_to(title, DOWN)
        self.play(Write(formula))

        # Axes for tension graph
        max_tension = final_mass * g
        ax = Axes(
            x_range=[0, total_time, 1],
            y_range=[0, max_tension + g, max_tension / 5],
            x_length=5,
            y_length=3,
        ).to_corner(UR)
        ax_labels = ax.get_axis_labels(Text("t (s)"), Text("T (N)"))
        self.play(Create(ax), FadeIn(ax_labels))

        def tension_at(tau):
            mass = initial_mass + (final_mass - initial_mass) * (tau / total_time)
            return mass * g

        tension_graph = always_redraw(
            lambda: ax.plot(
                tension_at,
                x_range=[0, max(t_tracker.get_value(), 0.001)],
                color=RED,
            )
        )
        tension_dot = always_redraw(
            lambda: Dot(ax.c2p(t_tracker.get_value(), tension_at(t_tracker.get_value())), color=YELLOW)
        )

        self.play(FadeIn(tension_graph, tension_dot))

        self.play(t_tracker.animate.set_value(total_time), run_time=total_time, rate_func=linear)
        self.wait(1)
