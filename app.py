
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from scipy.constants import G, c

# =========================================================
# QUANTUM UNIVERSE LAB v2.1
# 양자 우주 실험실
# =========================================================

st.set_page_config(
    page_title="양자 우주 실험실",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 디자인
# =========================================================

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
    background: rgba(35,52,88,0.45);
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

# =========================================================
# 제목
# =========================================================

st.title("🌌 양자 우주 실험실")

st.subheader(
    "초끈이론 · 루프 양자중력 · 블랙홀 · 중력 렌즈"
)

st.markdown("""
우주의 탄생부터 블랙홀 내부까지 탐구하는
가상 물리 실험실입니다.

서로 다른 이론적 모형을 적용하고
시공간의 변화와 우주의 구조를 비교합니다.
""")

st.caption("QUANTUM UNIVERSE LAB | VERSION 2.1")

st.divider()

# =========================================================
# 사이드바
# =========================================================

st.sidebar.title("⚙️ 실험 제어실")

st.sidebar.markdown("### 🌌 우주 초기 조건")

duration = st.sidebar.slider(
    "우주 시간 범위",
    2.0, 20.0, 10.0, 1.0
)

time_scale = st.sidebar.slider(
    "시간 척도",
    0.5, 5.0, 2.0, 0.1
)

st.sidebar.markdown("### 🧬 초끈이론 모형")

string_power = st.sidebar.slider(
    "초끈이론 팽창 지수",
    0.1, 0.8, 0.35, 0.05
)

extra_dimension = st.sidebar.slider(
    "추가 차원 변화 계수",
    0.0, 2.0, 0.5, 0.1
)

st.sidebar.markdown("### 🔵 루프 양자중력 모형")

loop_power = st.sidebar.slider(
    "루프 양자 보정 지수",
    0.1, 0.8, 0.25, 0.05
)

st.sidebar.divider()

st.sidebar.info("""
실험 변수는 교육용 단순화 모형의 매개변수입니다.

실제 자연계의 측정값이나
확정된 양자중력 이론의 해와는 다릅니다.
""")

# =========================================================
# 물리 모형
# =========================================================

def string_model(t, tau, power):

    x = np.asarray(t) / tau
    ax = np.abs(x)

    log_cosh = (
        ax
        + np.log1p(np.exp(-2 * ax))
        - np.log(2)
    )

    return np.exp(power * log_cosh)


def loop_model(t, tau, power):

    x = np.asarray(t) / tau

    return (1 + x**2)**power


def classical_model(t, tau):

    t = np.maximum(np.asarray(t), 0)

    return np.sqrt(t / tau)


# =========================================================
# 우주 계산
# =========================================================

시간 = np.linspace(-duration, duration, 500)

초끈우주 = string_model(
    시간, time_scale, string_power
)

루프우주 = loop_model(
    시간, time_scale, loop_power
)

고전우주 = classical_model(
    시간, time_scale
)

추가차원 = np.exp(
    extra_dimension * np.tanh(시간 / time_scale)
)

초끈_팽창률 = np.gradient(
    np.log(초끈우주), 시간
)

루프_팽창률 = np.gradient(
    np.log(루프우주), 시간
)

우주데이터 = pd.DataFrame({
    "시간": 시간,
    "초끈이론 우주": 초끈우주,
    "루프 양자중력 우주": 루프우주,
    "고전 우주": 고전우주,
    "추가 차원 지표": 추가차원,
    "초끈이론 팽창률": 초끈_팽창률,
    "루프 양자중력 팽창률": 루프_팽창률
})

# =========================================================
# 상태판
# =========================================================

st.header("📊 우주 시뮬레이션 상태")

a, b, cc, d = st.columns(4)

a.metric(
    "초끈이론 최소 크기",
    f"{np.min(초끈우주):.3f}"
)

b.metric(
    "루프 양자중력 최소 크기",
    f"{np.min(루프우주):.3f}"
)

cc.metric(
    "초끈이론 최대 크기",
    f"{np.max(초끈우주):.3f}"
)

d.metric(
    "루프 양자중력 최대 크기",
    f"{np.max(루프우주):.3f}"
)

st.divider()

# =========================================================
# 탭 구성
# =========================================================

탭 = st.tabs([
    "🌌 우주 이론 비교",
    "🪐 3D 우주 애니메이션",
    "🕳️ 블랙홀과 특이점",
    "🔭 중력 렌즈 실험",
    "🧬 추가 차원",
    "📚 물리 이론과 데이터"
])

# =========================================================
# 1. 우주 이론 비교
# =========================================================

with 탭[0]:

    st.header("🌌 우주 팽창 이론 비교")

    st.write("""
    초끈이론에서 영감을 얻은 모형,
    루프 양자우주론 모형,
    고전 우주 모형을 비교합니다.
    """)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=시간,
        y=초끈우주,
        name="초끈이론 모형",
        line=dict(color="#a78bfa", width=3)
    ))

    fig.add_trace(go.Scatter(
        x=시간,
        y=루프우주,
        name="루프 양자중력 모형",
        line=dict(color="#38bdf8", width=3)
    ))

    fig.add_trace(go.Scatter(
        x=시간,
        y=고전우주,
        name="고전 우주 모형",
        line=dict(
            color="#fbbf24",
            dash="dash",
            width=2
        )
    ))

    fig.add_vline(
        x=0,
        line_dash="dot",
        line_color="white",
        annotation_text="바운스 기준 시점"
    )

    fig.update_layout(
        template="plotly_dark",
        height=480,
        xaxis_title="시간",
        yaxis_title="우주 크기 척도",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("우주 팽창률 비교")

    rate = go.Figure()

    rate.add_trace(go.Scatter(
        x=시간,
        y=초끈_팽창률,
        name="초끈이론",
        line=dict(color="#a78bfa", width=2)
    ))

    rate.add_trace(go.Scatter(
        x=시간,
        y=루프_팽창률,
        name="루프 양자중력",
        line=dict(color="#38bdf8", width=2)
    ))

    rate.update_layout(
        template="plotly_dark",
        height=350,
        xaxis_title="시간",
        yaxis_title="팽창률 H(t)"
    )

    st.plotly_chart(
        rate,
        use_container_width=True
    )

    st.info("""
    H = (1/a) da/dt

    양수는 팽창, 음수는 수축을 의미합니다.
    """)

# =========================================================
# 2. 3D 우주 애니메이션
# =========================================================

with 탭[1]:

    st.header("🪐 시간에 따라 움직이는 3D 우주")

    st.write("""
    시간에 따라 우주의 크기가 어떻게 변하는지
    두 가지 모형으로 비교합니다.

    보라색은 초끈이론 모형,
    청록색은 루프 양자중력 모형입니다.
    """)

    프레임수 = 36

    애니시간 = np.linspace(
        -duration, duration, 프레임수
    )

    theta = np.linspace(0, np.pi, 24)
    phi = np.linspace(0, 2*np.pi, 36)

    THETA, PHI = np.meshgrid(theta, phi)

    단위X = np.sin(THETA) * np.cos(PHI)
    단위Y = np.sin(THETA) * np.sin(PHI)
    단위Z = np.cos(THETA)

    def 구체좌표(r):

        return (
            r * 단위X,
            r * 단위Y,
            r * 단위Z
        )

    r1 = float(
        string_model(
            애니시간[0], time_scale, string_power
        )
    )

    r2 = float(
        loop_model(
            애니시간[0], time_scale, loop_power
        )
    )

    X1, Y1, Z1 = 구체좌표(r1)
    X2, Y2, Z2 = 구체좌표(r2)

    animation = go.Figure(
        data=[
            go.Surface(
                x=X1,
                y=Y1,
                z=Z1,
                colorscale=[
                    [0, "#312e81"],
                    [1, "#c4b5fd"]
                ],
                opacity=0.65,
                showscale=False,
                name="초끈이론 우주"
            ),
            go.Surface(
                x=X2,
                y=Y2,
                z=Z2,
                colorscale=[
                    [0, "#164e63"],
                    [1, "#67e8f9"]
                ],
                opacity=0.48,
                showscale=False,
                name="루프 양자중력 우주"
            )
        ]
    )

    frames = []

    for i, t in enumerate(애니시간):

        rr1 = float(
            string_model(
                t, time_scale, string_power
            )
        )

        rr2 = float(
            loop_model(
                t, time_scale, loop_power
            )
        )

        xx1, yy1, zz1 = 구체좌표(rr1)
        xx2, yy2, zz2 = 구체좌표(rr2)

        frames.append(
            go.Frame(
                name=str(i),
                data=[
                    go.Surface(
                        x=xx1,
                        y=yy1,
                        z=zz1,
                        colorscale=[
                            [0, "#312e81"],
                            [1, "#c4b5fd"]
                        ],
                        opacity=0.65,
                        showscale=False
                    ),
                    go.Surface(
                        x=xx2,
                        y=yy2,
                        z=zz2,
                        colorscale=[
                            [0, "#164e63"],
                            [1, "#67e8f9"]
                        ],
                        opacity=0.48,
                        showscale=False
                    )
                ]
            )
        )

    animation.frames = frames

    animation.update_layout(
        template="plotly_dark",
        height=650,
        title="우주의 시간 진화",
        scene=dict(
            xaxis_title="공간 X",
            yaxis_title="공간 Y",
            zaxis_title="공간 Z",
            aspectmode="cube"
        ),
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                x=0.05,
                y=1.12,
                buttons=[
                    dict(
                        label="▶ 재생",
                        method="animate",
                        args=[
                            None,
                            {
                                "frame": {
                                    "duration": 150,
                                    "redraw": True
                                },
                                "fromcurrent": True,
                                "transition": {
                                    "duration": 0
                                }
                            }
                        ]
                    ),
                    dict(
                        label="⏸ 일시정지",
                        method="animate",
                        args=[
                            [None],
                            {
                                "frame": {
                                    "duration": 0,
                                    "redraw": False
                                },
                                "mode": "immediate"
                            }
                        ]
                    )
                ]
            )
        ],
        sliders=[
            dict(
                active=0,
                currentvalue={
                    "prefix": "우주 시간: "
                },
                steps=[
                    dict(
                        method="animate",
                        args=[
                            [str(i)],
                            {
                                "mode": "immediate",
                                "frame": {
                                    "duration": 0,
                                    "redraw": True
                                },
                                "transition": {
                                    "duration": 0
                                }
                            }
                        ],
                        label=f"{애니시간[i]:.1f}"
                    )
                    for i in range(프레임수)
                ]
            )
        ]
    )

    st.plotly_chart(
        animation,
        use_container_width=True
    )

    st.divider()

    st.subheader("현재 시간의 우주 크기")

    현재시점 = st.slider(
        "시간 선택",
        -duration,
        duration,
        0.0,
        0.1,
        key="현재_우주_시간"
    )

    현재초끈 = float(
        string_model(
            현재시점, time_scale, string_power
        )
    )

    현재루프 = float(
        loop_model(
            현재시점, time_scale, loop_power
        )
    )

    x, y = st.columns(2)

    x.metric(
        "초끈이론 우주",
        f"{현재초끈:.4f}"
    )

    y.metric(
        "루프 양자중력 우주",
        f"{현재루프:.4f}"
    )

    st.caption(
        "구체는 공간 단면을 단순화한 시각적 표현이며 "
        "실제 우주의 경계나 모양을 뜻하지 않습니다."
    )

# =========================================================
# 3. 블랙홀과 특이점
# =========================================================

with 탭[2]:

    st.header("🕳️ 블랙홀 내부와 특이점 실험")

    st.write("""
    블랙홀의 질량과 사건의 지평선을 계산하고
    고전적 시공간 곡률과 가상 양자 보정 모형을 비교합니다.
    """)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        질량 = st.slider(
            "블랙홀 질량 (태양 질량)",
            1.0,
            50.0,
            10.0,
            1.0
        )

    with col2:

        보정길이 = st.slider(
            "가상 양자중력 보정 길이",
            0.05,
            0.8,
            0.25,
            0.05
        )

    태양질량 = 1.98847e30

    M = 질량 * 태양질량

    rs = 2 * G * M / c**2

    반지름_km = rs / 1000

    m1, m2, m3 = st.columns(3)

    m1.metric(
        "블랙홀 질량",
        f"{질량:.1f} 태양 질량"
    )

    m2.metric(
        "슈바르츠실트 반지름",
        f"{반지름_km:.2f} km"
    )

    m3.metric(
        "사건의 지평선 지름",
        f"{2*반지름_km:.2f} km"
    )

    st.divider()

    st.subheader("시공간 곡률 실험")

    st.latex(
        r"K=\frac{48G^2M^2}{c^4r^6}"
    )

    x = np.linspace(0.08, 3.0, 500)

    고전곡률 = 12 / x**6

    양자곡률 = 12 / (
        x**6 + 보정길이**6
    )

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x,
        y=고전곡률,
        name="고전 일반상대성이론",
        line=dict(color="#f87171", width=3)
    ))

    fig.add_trace(go.Scatter(
        x=x,
        y=양자곡률,
        name="가상 양자중력 보정",
        line=dict(color="#38bdf8", width=3)
    ))

    fig.add_vline(
        x=1,
        line_dash="dash",
        annotation_text="사건의 지평선"
    )

    fig.update_layout(
        template="plotly_dark",
        height=480,
        xaxis_title="중심 거리 / 슈바르츠실트 반지름",
        yaxis_title="무차원 곡률",
        yaxis_type="log"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.info("""
    고전 모형에서는 중심으로 접근할수록
    곡률이 발산합니다.

    파란색은 특이점 완화 가능성을 살펴보기 위한
    임의의 현상론적 모형입니다.
    실제 루프 양자중력의 해가 아닙니다.
    """)

    st.divider()

    st.subheader("블랙홀 내부 위치 탐색")

    위치 = st.slider(
        "중심으로부터 거리 (슈바르츠실트 반지름 단위)",
        0.1,
        3.0,
        1.5,
        0.05
    )

    if 위치 > 1:
        st.success("사건의 지평선 바깥")
    elif 위치 == 1:
        st.warning("사건의 지평선")
    else:
        st.error("사건의 지평선 내부")

    고전값 = 12 / 위치**6

    양자값 = 12 / (
        위치**6 + 보정길이**6
    )

    q1, q2 = st.columns(2)

    q1.metric(
        "고전 곡률",
        f"{고전값:.4e}"
    )

    q2.metric(
        "가상 양자 보정 곡률",
        f"{양자값:.4e}"
    )

    with st.expander("사건의 지평선이란?"):

        st.write("""
        사건의 지평선은 외부로 빛이 탈출할 수 없는
        영역의 경계입니다.

        슈바르츠실트 블랙홀에서는
        r = 2GM/c²에 해당합니다.
        """)

    with st.expander("특이점이란?"):

        st.write("""
        고전적인 슈바르츠실트 해에서는
        중심에서 곡률 불변량이 발산합니다.

        양자중력은 이 문제를 해결할 가능성을 연구하지만
        실제 블랙홀 내부의 구조는 아직 확정되지 않았습니다.
        """)

# =========================================================
# 4. 중력 렌즈와 빛의 휘어짐
# =========================================================

with 탭[3]:

    st.header("🔭 중력 렌즈와 빛의 휘어짐")

    st.write("""
    블랙홀의 질량이 빛의 경로에 미치는 영향을 탐구합니다.

    약한 중력장 근사와 이상적인 렌즈 배치를 사용한
    교육용 시뮬레이션입니다.
    """)

    st.divider()

    st.subheader("블랙홀 조건 설정")

    col1, col2 = st.columns(2)

    with col1:

        렌즈질량 = st.slider(
            "렌즈 블랙홀 질량 (태양 질량)",
            1.0,
            100.0,
            10.0,
            1.0,
            key="렌즈_질량"
        )

    with col2:

        렌즈간격 = st.slider(
            "빛의 경로 간격",
            0.2,
            1.0,
            0.4,
            0.1
        )

    M_lens = 렌즈질량 * 1.98847e30

    rs_lens = 2 * G * M_lens / c**2

    st.metric(
        "렌즈 블랙홀 슈바르츠실트 반지름",
        f"{rs_lens/1000:.2f} km"
    )

    st.divider()

    st.subheader("1. 빛의 휘어짐 각도")

    st.latex(
        r"\alpha \approx \frac{4GM}{c^2b}"
    )

    st.write("""
    약한 중력장 근사에서 빛의 편향각입니다.
    b는 충돌 매개변수입니다.
    """)

    충돌거리 = np.linspace(4, 12, 250)

    편향각 = 2 / 충돌거리

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=충돌거리,
        y=np.degrees(편향각),
        mode="lines",
        name="빛의 편향각",
        line=dict(color="#38bdf8", width=3)
    ))

    fig.update_layout(
        template="plotly_dark",
        height=400,
        xaxis_title="충돌 매개변수 (슈바르츠실트 반지름 단위)",
        yaxis_title="편향각 (도)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.caption(
        "강한 중력장에 가까운 광선에는 이 근사식이 정확하지 않습니다."
    )

    st.divider()

    st.subheader("2. 3차원 광선 경로")

    st.write("""
    블랙홀 주변을 통과하는 빛의 경로를
    단순화된 광선 방정식으로 시각화합니다.
    """)

    # 무차원 좌표: 길이 단위는 슈바르츠실트 반지름
    # y'' = -y/(x²+y²)^(3/2)
    # 약한 중력장 근사
    def 광선계산(b, x_start=-30, x_end=30, steps=600):

        xs = np.linspace(x_start, x_end, steps)

        dx = xs[1] - xs[0]

        y = np.zeros(steps)
        v = np.zeros(steps)

        y[0] = b
        v[0] = 0.0

        def acceleration(x, y_value):
            r2 = x*x + y_value*y_value
            return -y_value / (r2**1.5 + 1e-12)

        for i in range(steps - 1):

            x = xs[i]
            yy = y[i]
            vv = v[i]

            k1y = vv
            k1v = acceleration(x, yy)

            k2y = vv + 0.5*dx*k1v
            k2v = acceleration(
                x + 0.5*dx,
                yy + 0.5*dx*k1y
            )

            k3y = vv + 0.5*dx*k2v
            k3v = acceleration(
                x + 0.5*dx,
                yy + 0.5*dx*k2y
            )

            k4y = vv + dx*k3v
            k4v = acceleration(
                x + dx,
                yy + dx*k3y
            )

            y[i+1] = yy + dx * (
                k1y + 2*k2y + 2*k3y + k4y
            ) / 6

            v[i+1] = vv + dx * (
                k1v + 2*k2v + 2*k3v + k4v
            ) / 6

        return xs, y

    광선그림 = go.Figure()

    # 블랙홀 표시
    theta = np.linspace(0, np.pi, 35)
    phi = np.linspace(0, 2*np.pi, 50)

    TH, PH = np.meshgrid(theta, phi)

    BX = np.sin(TH) * np.cos(PH)
    BY = np.sin(TH) * np.sin(PH)
    BZ = np.cos(TH)

    광선그림.add_trace(go.Surface(
        x=BX,
        y=BY,
        z=BZ,
        colorscale=[
            [0, "#050505"],
            [1, "#454545"]
        ],
        showscale=False,
        opacity=1,
        name="블랙홀"
    ))

    광선색상 = [
        "#fbbf24",
        "#38bdf8",
        "#a78bfa",
        "#f472b6",
        "#34d399",
        "#fb923c",
        "#e879f9"
    ]

    for i, b in enumerate(
        np.arange(-3, 4) * 렌즈간격 + 5
    ):

        # 너무 작은 충돌 매개변수는 제외
        if b < 4:
            continue

        xx, yy = 광선계산(b)

        광선그림.add_trace(go.Scatter3d(
            x=xx,
            y=yy,
            z=np.zeros_like(xx),
            mode="lines",
            name=f"광선 {i+1}",
            line=dict(
                color=광선색상[i],
                width=5
            )
        ))

    광선그림.update_layout(
        template="plotly_dark",
        height=650,
        scene=dict(
            xaxis_title="공간 X",
            yaxis_title="공간 Y",
            zaxis_title="공간 Z",
            aspectmode="cube"
        )
    )

    st.plotly_chart(
        광선그림,
        use_container_width=True
    )

    st.caption(
        "무차원 약한 중력장 광선 모델입니다. "
        "정확한 강한 중력장 광선 추적은 슈바르츠실트 "
        "시공간의 영측지선 방정식을 풀어야 합니다."
    )

    st.divider()

    st.subheader("3. 아인슈타인 고리 실험")

    st.write("""
    광원과 관측자 사이에 렌즈가 있고
    세 천체가 정확히 정렬된 이상적인 상황을 가정합니다.
    """)

    거리1 = st.slider(
        "관측자에서 렌즈까지 거리 (Mpc)",
        1.0,
        1000.0,
        100.0,
        1.0
    )

    거리2 = st.slider(
        "렌즈에서 광원까지 거리 (Mpc)",
        1.0,
        1000.0,
        200.0,
        1.0
    )

    Mpc = 3.085677581491367e22

    Dl = 거리1 * Mpc
    Dls = 거리2 * Mpc
    Ds = Dl + Dls

    theta_E = np.sqrt(
        (4 * G * M_lens / c**2)
        * Dls / (Dl * Ds)
    )

    theta_arcsec = (
        np.degrees(theta_E) * 3600
    )

    st.metric(
        "아인슈타인 각반지름",
        f"{theta_arcsec:.8f} 초각"
    )

    angle = np.linspace(
        0, 2*np.pi, 300
    )

    ring = go.Figure()

    ring.add_trace(go.Scatter(
        x=theta_arcsec*np.cos(angle),
        y=theta_arcsec*np.sin(angle),
        mode="lines",
        name="아인슈타인 고리",
        line=dict(
            color="#fbbf24",
            width=4
        )
    ))

    ring.add_trace(go.Scatter(
        x=[0],
        y=[0],
        mode="markers",
        name="렌즈 중심",
        marker=dict(
            size=12,
            color="#111111",
            line=dict(
                color="white",
                width=2
            )
        )
    ))

    ring.update_layout(
        template="plotly_dark",
        height=450,
        xaxis_title="각도 (초각)",
        yaxis_title="각도 (초각)",
        yaxis=dict(
            scaleanchor="x",
            scaleratio=1
        )
    )

    st.plotly_chart(
        ring,
        use_container_width=True
    )

    st.success(
        "이상적인 아인슈타인 고리 계산 완료"
    )

    with st.expander("중력 렌즈란?"):

        st.write("""
        질량을 가진 천체는 시공간을 휘게 합니다.

        빛은 휘어진 시공간을 따라 이동하기 때문에
        외부 관측자에게 빛의 방향이 바뀐 것처럼 보입니다.
        """)

    with st.expander("아인슈타인 고리란?"):

        st.write("""
        광원, 렌즈, 관측자가 정확하게 정렬되면
        빛이 고리 형태의 상을 만들 수 있습니다.
        """)

# =========================================================
# 5. 추가 차원 실험실
# =========================================================

with 탭[4]:

    st.header("🧬 추가 차원 실험실")

    st.write("""
    초끈이론에서는 우리가 경험하는 공간 외에
    추가 공간 차원이 존재할 가능성을 연구합니다.
    """)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=시간,
        y=추가차원,
        name="추가 차원 크기 지표",
        fill="tozeroy",
        line=dict(
            color="#f472b6",
            width=3
        )
    ))

    fig.update_layout(
        template="plotly_dark",
        height=400,
        xaxis_title="시간",
        yaxis_title="상대적 크기"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    x, y = st.columns(2)

    x.metric(
        "초기 추가 차원 지표",
        f"{추가차원[0]:.3f}"
    )

    y.metric(
        "최종 추가 차원 지표",
        f"{추가차원[-1]:.3f}"
    )

    st.info("""
    이 그래프는 추가 차원의 상대적 크기를 표현한
    교육용 모형입니다.

    실제 칼라비-야우 공간의 해를 계산한 것은 아닙니다.
    """)

# =========================================================
# 6. 물리 이론과 데이터
# =========================================================

with 탭[5]:

    st.header("📚 물리 이론 자료실")

    st.subheader("초끈이론에서 영감을 얻은 모형")

    st.latex(
        r"a_s(t)=\cosh(t/\tau)^p"
    )

    st.write("""
    비특이 우주 바운스 형태를 나타내는
    현상론적 모형입니다.
    """)

    st.divider()

    st.subheader("루프 양자우주론 모형")

    st.latex(
        r"a_L(t)=[1+(t/\tau)^2]^q"
    )

    st.write("""
    양자 보정으로 인해 우주의 크기가
    0에 도달하지 않는 형태를 표현합니다.
    """)

    st.divider()

    st.subheader("고전 복사 지배 우주")

    st.latex(
        r"a_C(t)\propto\sqrt{t},\quad t>0"
    )

    st.divider()

    st.subheader("블랙홀 곡률")

    st.latex(
        r"K=\frac{48G^2M^2}{c^4r^6}"
    )

    st.divider()

    st.subheader("중력 렌즈")

    st.latex(
        r"\alpha\approx\frac{4GM}{c^2b}"
    )

    st.divider()

    st.subheader("실험 데이터")

    st.dataframe(
        우주데이터,
        use_container_width=True,
        hide_index=True
    )

    csv = 우주데이터.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        "📥 우주 실험 데이터 다운로드",
        data=csv,
        file_name="양자_우주_실험_데이터.csv",
        mime="text/csv"
    )

# =========================================================
# 하단
# =========================================================

st.divider()

st.markdown("""
<div style="text-align:center; padding:25px; color:#8ca4c8;">

<h3>🌌 QUANTUM UNIVERSE LAB</h3>

양자 우주 실험실

<br><br>

초끈이론 · 루프 양자중력 · 블랙홀 · 중력 렌즈

<br>

교육용 과학 가상실험 환경

<br><br>

VERSION 2.1

</div>
""", unsafe_allow_html=True)
