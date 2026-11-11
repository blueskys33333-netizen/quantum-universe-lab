
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# =====================================================
# QUANTUM UNIVERSE LAB v1.0
# Quantum Cosmology Comparison Simulator
# =====================================================

st.set_page_config(
    page_title="Quantum Universe Lab",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- DESIGN ----------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #080d1b, #111a32);
    color: #e8efff;
}
h1, h2, h3 {
    color: #e8efff !important;
}
p, label {
    color: #c4d0e8;
}
div[data-testid="stMetric"] {
    background: rgba(35, 52, 88, 0.45);
    border: 1px solid rgba(120,160,255,0.2);
    padding: 15px;
    border-radius: 12px;
}
div[data-testid="stMetricValue"] {
    color: #8cc7ff;
}
section[data-testid="stSidebar"] {
    background: #0c1428;
}
.stButton button {
    border-radius: 10px;
    background: #244b83;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.markdown("""
# 🌌 QUANTUM UNIVERSE LAB
### Quantum Gravity & Cosmology Simulation Environment

**Explore the universe through two different approaches to quantum gravity.**
""")

st.caption(
    "VERSION 1.0 | STRING-INSPIRED COSMOLOGY | LOOP QUANTUM COSMOLOGY"
)

st.divider()

# ---------------- SIDEBAR ----------------

st.sidebar.title("⚙️ Experiment Controls")

st.sidebar.markdown("### Initial conditions")

duration = st.sidebar.slider(
    "Simulation time range",
    min_value=2.0,
    max_value=20.0,
    value=10.0,
    step=1.0
)

time_scale = st.sidebar.slider(
    "Characteristic time scale",
    min_value=0.5,
    max_value=5.0,
    value=2.0,
    step=0.1
)

st.sidebar.markdown("### String-inspired model")

string_power = st.sidebar.slider(
    "Expansion exponent",
    min_value=0.1,
    max_value=0.8,
    value=0.35,
    step=0.05
)

extra_dimension = st.sidebar.slider(
    "Extra-dimension variation",
    min_value=0.0,
    max_value=2.0,
    value=0.5,
    step=0.1
)

st.sidebar.markdown("### Loop quantum model")

loop_power = st.sidebar.slider(
    "Quantum correction exponent",
    min_value=0.1,
    max_value=0.8,
    value=0.25,
    step=0.05
)

st.sidebar.markdown("---")
st.sidebar.info(
    "These controls change parameters in simplified "
    "phenomenological models, not fundamental constants "
    "measured from nature."
)

# ---------------- SIMULATION ENGINE ----------------

def string_model(t, tau, power):
    """
    String-inspired phenomenological bounce model.

    a(t) = cosh(t/tau)^power

    This is an illustrative nonsingular scale factor,
    not a complete solution of string theory.
    """

    x = t / tau

    abs_x = np.abs(x)

    log_cosh = (
        abs_x
        + np.log1p(np.exp(-2 * abs_x))
        - np.log(2)
    )

    a = np.exp(power * log_cosh)

    return a


def loop_model(t, tau, power):
    """
    Simplified effective loop quantum cosmology model.

    a(t) = (1 + (t/tau)^2)^power

    The nonzero minimum represents a bounce
    rather than a classical singularity.
    """

    x = t / tau

    a = np.power(1 + x**2, power)

    return a


def classical_model(t, tau):
    """
    Classical radiation-dominated expanding universe.

    a(t) proportional to t^(1/2), for t > 0.

    The classical solution has a singular beginning.
    """

    t_positive = np.maximum(t, 0)

    a = np.sqrt(t_positive / tau)

    return a


# ---------------- CALCULATE ----------------

t = np.linspace(-duration, duration, 500)

a_string = string_model(
    t, time_scale, string_power
)

a_loop = loop_model(
    t, time_scale, loop_power
)

a_classical = classical_model(
    t, time_scale
)

# Normalize each model to a(0) = 1
# The classical model is normalized separately
# at its positive-time reference point.

# Extra dimension: illustrative dilaton/radius proxy
extra_radius = np.exp(
    extra_dimension * np.tanh(t / time_scale)
)

# Effective expansion rate H = (1/a) da/dt
H_string = np.gradient(
    np.log(a_string), t
)

H_loop = np.gradient(
    np.log(a_loop), t
)

# ---------------- DATA ----------------

data = pd.DataFrame({
    "Time": t,
    "String-inspired universe": a_string,
    "Loop quantum universe": a_loop,
    "Classical universe": a_classical,
    "Extra dimension proxy": extra_radius,
    "String expansion rate": H_string,
    "Loop expansion rate": H_loop
})

# ---------------- METRICS ----------------

st.markdown("## 📊 Universe status")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "String minimum",
        f"{np.min(a_string):.3f}"
    )

with c2:
    st.metric(
        "Loop minimum",
        f"{np.min(a_loop):.3f}"
    )

with c3:
    st.metric(
        "String maximum",
        f"{np.max(a_string):.3f}"
    )

with c4:
    st.metric(
        "Loop maximum",
        f"{np.max(a_loop):.3f}"
    )

st.divider()

# ---------------- TABS ----------------

tab1, tab2, tab3, tab4 = st.tabs([
    "🌌 Universe Comparison",
    "🪐 3D Spacetime",
    "🧬 Extra Dimensions",
    "📚 Physics & Data"
])

# =====================================================
# TAB 1: 2D COMPARISON
# =====================================================

with tab1:

    st.subheader("Universe Expansion Comparison")

    st.markdown("""
    Compare how the scale factor changes over time
    in the two quantum-gravity-inspired models.
    """)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t,
        y=a_string,
        mode="lines",
        name="String-inspired model",
        line=dict(color="#a78bfa", width=3)
    ))

    fig.add_trace(go.Scatter(
        x=t,
        y=a_loop,
        mode="lines",
        name="Loop quantum model",
        line=dict(color="#38bdf8", width=3)
    ))

    fig.add_trace(go.Scatter(
        x=t,
        y=a_classical,
        mode="lines",
        name="Classical radiation model",
        line=dict(
            color="#fbbf24",
            width=2,
            dash="dash"
        )
    ))

    fig.add_vline(
        x=0,
        line_dash="dot",
        line_color="white",
        annotation_text="Bounce / reference time"
    )

    fig.update_layout(
        template="plotly_dark",
        height=500,
        xaxis_title="Time (dimensionless)",
        yaxis_title="Scale factor a(t)",
        hovermode="x unified",
        legend=dict(orientation="h"),
        margin=dict(l=20, r=20, t=40, b=20)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("### Expansion rate")

    rate_fig = go.Figure()

    rate_fig.add_trace(go.Scatter(
        x=t,
        y=H_string,
        name="String-inspired",
        line=dict(color="#a78bfa", width=2)
    ))

    rate_fig.add_trace(go.Scatter(
        x=t,
        y=H_loop,
        name="Loop quantum",
        line=dict(color="#38bdf8", width=2)
    ))

    rate_fig.update_layout(
        template="plotly_dark",
        height=350,
        xaxis_title="Time",
        yaxis_title="Hubble parameter H(t)",
        hovermode="x unified"
    )

    st.plotly_chart(
        rate_fig,
        use_container_width=True
    )

    st.info(
        "A negative expansion rate indicates contraction. "
        "A positive expansion rate indicates expansion. "
        "A transition near zero indicates a minimum in "
        "the scale factor for these symmetric bounce models."
    )

# =====================================================
# TAB 2: 3D SPACETIME
# =====================================================

with tab2:

    st.subheader("Three-dimensional universe visualization")

    st.markdown("""
    Each circular cross-section represents a simplified
    spatial slice of the universe at a particular time.

    The vertical axis represents time, while the radius
    represents the scale factor.
    """)

    theta = np.linspace(0, 2 * np.pi, 70)

    time_grid = np.linspace(
        -duration, duration, 100
    )

    T, THETA = np.meshgrid(
        time_grid, theta
    )

    A_string = string_model(
        T, time_scale, string_power
    )

    A_loop = loop_model(
        T, time_scale, loop_power
    )

    X_string = A_string * np.cos(THETA)
    Y_string = A_string * np.sin(THETA)

    X_loop = A_loop * np.cos(THETA)
    Y_loop = A_loop * np.sin(THETA)

    fig3d = go.Figure()

    fig3d.add_trace(go.Surface(
        x=X_string,
        y=Y_string,
        z=T,
        colorscale=[
            [0, "#312e81"],
            [0.5, "#8b5cf6"],
            [1, "#c4b5fd"]
        ],
        opacity=0.78,
        name="String-inspired universe",
        showscale=False,
        hovertemplate=(
            "Time: %{z:.2f}<br>"
            "X: %{x:.2f}<br>"
            "Y: %{y:.2f}<extra>String model</extra>"
        )
    ))

    fig3d.add_trace(go.Surface(
        x=X_loop,
        y=Y_loop,
        z=T,
        colorscale=[
            [0, "#164e63"],
            [0.5, "#0891b2"],
            [1, "#67e8f9"]
        ],
        opacity=0.65,
        name="Loop quantum universe",
        showscale=False,
        hovertemplate=(
            "Time: %{z:.2f}<br>"
            "X: %{x:.2f}<br>"
            "Y: %{y:.2f}<extra>Loop model</extra>"
        )
    ))

    fig3d.update_layout(
        template="plotly_dark",
        height=700,
        scene=dict(
            xaxis_title="Space X",
            yaxis_title="Space Y",
            zaxis_title="Time",
            aspectmode="manual",
            aspectratio=dict(
                x=1,
                y=1,
                z=2
            )
        ),
        margin=dict(
            l=0, r=0, t=20, b=0
        )
    )

    st.plotly_chart(
        fig3d,
        use_container_width=True
    )

    st.caption(
        "This is a geometric visualization of scale-factor "
        "histories, not a full numerical solution of "
        "Einstein's field equations."
    )

# =====================================================
# TAB 3: EXTRA DIMENSIONS
# =====================================================

with tab3:

    st.subheader("Extra Dimension Laboratory")

    st.markdown("""
    String theory can involve additional spatial dimensions.
    This experiment uses an illustrative radius proxy to
    explore how an additional dimension might vary over time.
    """)

    fig_extra = go.Figure()

    fig_extra.add_trace(go.Scatter(
        x=t,
        y=extra_radius,
        name="Extra dimension radius proxy",
        fill="tozeroy",
        line=dict(
            color="#f472b6",
            width=3
        )
    ))

    fig_extra.update_layout(
        template="plotly_dark",
        height=400,
        xaxis_title="Time",
        yaxis_title="Relative radius",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig_extra,
        use_container_width=True
    )

    st.markdown("### Interpretation")

    st.write(
        "The curve represents a toy parameter describing "
        "the relative size of an additional dimension. "
        "It is not a calculated compactification solution."
    )

    st.metric(
        "Radius proxy at initial time",
        f"{extra_radius[0]:.3f}"
    )

    st.metric(
        "Radius proxy at final time",
        f"{extra_radius[-1]:.3f}"
    )

# =====================================================
# TAB 4: PHYSICS AND DATA
# =====================================================

with tab4:

    st.subheader("Physical models")

    st.markdown("### 1. String-inspired cosmology")

    st.latex(
        r"a_s(t)=\cosh\left(\frac{t}{\tau}\right)^p"
    )

    st.write(
        "A phenomenological nonsingular bounce model. "
        "The parameter p controls the shape of expansion. "
        "The model is inspired by early-universe bounce "
        "ideas but is not the full string theory."
    )

    st.divider()

    st.markdown("### 2. Loop quantum cosmology")

    st.latex(
        r"a_L(t)=\left[1+\left(\frac{t}{\tau}\right)^2\right]^q"
    )

    st.write(
        "An illustrative effective scale-factor model "
        "with a nonzero minimum. It represents the "
        "qualitative idea of a quantum bounce."
    )

    st.divider()

    st.markdown("### 3. Classical radiation-dominated universe")

    st.latex(
        r"a_C(t)\propto \sqrt{t},\quad t>0"
    )

    st.write(
        "A classical expanding-universe reference model "
        "with a singular beginning at t = 0."
    )

    st.divider()

    st.markdown("### Simulation data")

    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True
    )

    csv = data.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="📥 Download experiment data (CSV)",
        data=csv,
        file_name="quantum_universe_results.csv",
        mime="text/csv"
    )

# ---------------- FOOTER ----------------

st.divider()

st.markdown("""
<div style="text-align:center; padding:20px; color:#8ca4c8;">

QUANTUM UNIVERSE LAB v1.0

<br>

Exploring the mathematical possibilities of our universe.

<br><br>

Educational Scientific Simulation Environment

</div>
""", unsafe_allow_html=True)
