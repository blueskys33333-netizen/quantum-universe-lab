
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.constants import G, c

# =========================================================
# QUANTUM UNIVERSE LAB 2.0
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
st.subheader("초끈이론 · 루프 양자중력 · 블랙홀 · 우주 진화")

st.markdown("""
**우주의 탄생부터 블랙홀 내부까지 탐구하는 가상 물리 실험실**

서로 다른 이론적 모형을 적용하고
시공간의 변화와 우주의 구조를 비교합니다.
""")

st.caption("QUANTUM UNIVERSE LAB | VERSION 2.0")

st.divider()

# =========================================================
# 사이드바 설정
# =========================================================

st.sidebar.title("⚙️ 실험 제어실")

st.sidebar.markdown("### 우주 초기 조건")

duration = st.sidebar.slider(
    "우주 시간 범위",
    2.0, 20.0, 10.0, 1.0
)

time_scale = st.sidebar.slider(
    "시간 척도",
    0.5, 5.0, 2.0, 0.1
)

st.sidebar.markdown("### 초끈이론 모형")

string_power = st.sidebar.slider(
    "초끈이론 팽창 지수",
    0.1, 0.8, 0.35, 0.05
)

extra_dimension = st.sidebar.slider(
    "추가 차원 변화 계수",
    0.0, 2.0, 0.5, 0.1
)

st.sidebar.markdown("### 루프 양자중력 모형")

loop_power = st.sidebar.slider(
    "루프 양자 보정 지수",
    0.1, 0.8, 0.25, 0.05
)

st.sidebar.divider()

st.sidebar.info(
    "실험 변수는 교육용 단순화 모형의 매개변수입니다. "
    "자연계의 측정된 물리 상수와 동일한 값은 아닙니다."
)

# =========================================================
# 우주 모형
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
# 우주 데이터 계산
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
# 상단 상태판
# =========================================================

st.header("📊 우주 상태판")

a, b, c1, d = st.columns(4)

a.metric(
    "초끈이론 최소 크기",
    f"{np.min(초끈우주):.3f}"
)

b.metric(
    "루프 양자중력 최소 크기",
    f"{np.min(루프우주):.3f}"
)

c1.metric(
    "초끈이론 최대 크기",
    f"{np.max(초끈우주):.3f}"
)

d.metric(
    "루프 양자중력 최대 크기",
    f"{np.max(루프우주):.3f}"
)

st.divider()

# =========================================================
# 실험실 탭
# =========================================================

탭 = st.tabs([
    "🌌 우주 이론 비교",
    "🪐 3D 우주 애니메이션",
    "🕳️ 블랙홀 내부와 특이점",
    "🧬 추가 차원 실험실",
    "📚 물리 이론과 데이터"
])

# =========================================================
# 탭 1. 우주 이론 비교
# =========================================================

with 탭[0]:

    st.header("🌌 우주 팽창 이론 비교")

    st.write(
        "초끈이론에서 영감을 얻은 모형, "
        "루프 양자우주론 모형, 고전 우주를 비교합니다."
    )

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
        line=dict(color="#fbbf24", dash="dash")
    ))

    fig.add_vline(
        x=0,
        line_dash="dot",
        annotation_text="바운스 기준 시점"
    )

    fig.update_layout(
        template="plotly_dark",
        height=480,
        xaxis_title="시간",
        yaxis_title="우주 크기 척도",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("우주 팽창률")

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

    st.plotly_chart(rate, use_container_width=True)

    st.info(
        "팽창률은 H = (1/a) da/dt로 정의합니다. "
        "양수는 팽창, 음수는 수축을 나타냅니다."
    )

# =========================================================
# 탭 2. 시간에 따른 3D 우주 애니메이션
# =========================================================

with 탭[1]:

    st.header("🪐 움직이는 3차원 우주")

    st.write("""
    시간이 흐르면서 우주의 크기가 어떻게 변하는지
    3차원 공간에서 관찰합니다.

    보라색 구체는 초끈이론에서 영감을 얻은 모형,
    청록색 구체는 루프 양자중력 모형입니다.
    """)

    프레임수 = 36

    애니시간 = np.linspace(
        -duration, duration, 프레임수
    )

    # 구체의 표면을 생성
    theta = np.linspace(0, np.pi, 24)
    phi = np.linspace(0, 2*np.pi, 36)

    THETA, PHI = np.meshgrid(theta, phi)

    단위X = np.sin(THETA) * np.cos(PHI)
    단위Y = np.sin(THETA) * np.sin(PHI)
    단위Z = np.cos(THETA)

    def 구체좌표(반지름):
        return (
            반지름 * 단위X,
            반지름 * 단위Y,
            반지름 * 단위Z
        )

    초기시간 = 애니시간[0]

    초기초끈 = float(
        string_model(
            초기시간, time_scale, string_power
        )
    )

    초기루프 = float(
        loop_model(
            초기시간, time_scale, loop_power
        )
    )

    X1, Y1, Z1 = 구체좌표(초기초끈)
    X2, Y2, Z2 = 구체좌표(초기루프)

    애니메이션 = go.Figure(
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

    프레임목록 = []

    for i, 현재시간 in enumerate(애니시간):

        r1 = float(
            string_model(
                현재시간, time_scale, string_power
            )
        )

        r2 = float(
            loop_model(
                현재시간, time_scale, loop_power
            )
        )

        xx1, yy1, zz1 = 구체좌표(r1)
        xx2, yy2, zz2 = 구체좌표(r2)

        프레임목록.append(
            go.Frame(
                name=str(i),
                data=[
                    go.Surface(
                        x=xx1, y=yy1, z=zz1,
                        colorscale=[
                            [0, "#312e81"],
                            [1, "#c4b5fd"]
                        ],
                        opacity=0.65,
                        showscale=False
                    ),
                    go.Surface(
                        x=xx2, y=yy2, z=zz2,
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

    애니메이션.frames = 프레임목록

    애니메이션.update_layout(
        template="plotly_dark",
        height=650,
        title="시간에 따른 우주 크기 변화",
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
                                "mode": "immediate",
                                "transition": {
                                    "duration": 0
                                }
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
        애니메이션,
        use_container_width=True
    )

    st.caption(
        "구체는 공간의 모든 방향을 단순화해 표현한 "
        "3차원 시각화입니다. 실제 우주의 경계나 모양을 "
        "나타내는 것은 아닙니다."
    )

    st.subheader("현재 우주 크기 비교")

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
        "초끈이론 우주 크기",
        f"{현재초끈:.4f}"
    )

    y.metric(
        "루프 양자중력 우주 크기",
        f"{현재루프:.4f}"
    )

# =========================================================
# 탭 3. 블랙홀 내부와 특이점
# =========================================================

with 탭[2]:

    st.header("🕳️ 블랙홀 내부와 특이점 실험실")

    st.write("""
    블랙홀의 사건의 지평선과 시공간 곡률을 탐구합니다.

    고전적인 일반상대성이론 모형과
    특이점을 유한한 곡률로 바꾸어 보는
    가상 양자중력 보정 모형을 비교합니다.
    """)

    st.divider()

    st.subheader("블랙홀 조건 설정")

    col1, col2 = st.columns(2)

    with col1:
        질량 = st.slider(
            "블랙홀 질량 (태양 질량 단위)",
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

    슈바르츠실트반지름 = 2 * G * M / c**2

    반지름_km = 슈바르츠실트반지름 / 1000

    st.markdown("### 블랙홀 기본 정보")

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

    st.subheader("1. 블랙홀의 시공간 곡률")

    st.write("""
    슈바르츠실트 블랙홀의 크레치만 스칼라를
    이용해 시공간 곡률을 계산합니다.
    """)

    st.latex(
        r"K=\frac{48G^2M^2}{c^4r^6}"
    )

    st.write("""
    사건의 지평선에서 곡률은 유한하지만,
    고전적인 모형에서는 중심으로 접근할수록
    곡률이 발산합니다.
    """)

    # 무차원 반지름 r / rs
    x = np.linspace(0.08, 3.0, 500)

    # K * rs^4 = 12 / x^6
    고전곡률 = 12 / x**6

    # 가상 양자중력 보정 모형
    # 실제 LQG 방정식에서 유도한 해가 아님
    양자곡률 = 12 / (
        x**6 + 보정길이**6
    )

    곡률그래프 = go.Figure()

    곡률그래프.add_trace(go.Scatter(
        x=x,
        y=고전곡률,
        name="고전 일반상대성이론",
        line=dict(
            color="#f87171",
            width=3
        )
    ))

    곡률그래프.add_trace(go.Scatter(
        x=x,
        y=양자곡률,
        name="가상 양자중력 보정 모형",
        line=dict(
            color="#38bdf8",
            width=3
        )
    ))

    곡률그래프.add_vline(
        x=1,
        line_dash="dash",
        line_color="white",
        annotation_text="사건의 지평선"
    )

    곡률그래프.update_layout(
        template="plotly_dark",
        height=480,
        xaxis_title="중심으로부터의 거리 / 슈바르츠실트 반지름",
        yaxis_title="무차원 시공간 곡률 K·rₛ⁴",
        yaxis_type="log",
        hovermode="x unified"
    )

    st.plotly_chart(
        곡률그래프,
        use_container_width=True
    )

    st.info("""
    파란색 곡선은 특이점이 어떻게 완화될 수 있는지
    탐색하기 위한 현상론적 예시입니다.

    실제 루프 양자중력의 블랙홀 해를 계산한 것은 아닙니다.
    """)

    st.divider()

    st.subheader("2. 블랙홀 구조 탐색")

    선택반지름 = st.slider(
        "블랙홀 중심으로부터 거리 (슈바르츠실트 반지름 단위)",
        0.1,
        3.0,
        1.5,
        0.05
    )

    if 선택반지름 > 1:
        st.success("현재 위치: 사건의 지평선 바깥")
    elif 선택반지름 == 1:
        st.warning("현재 위치: 사건의 지평선")
    else:
        st.error("현재 위치: 사건의 지평선 내부")

    고전_선택곡률 = 12 / 선택반지름**6

    양자_선택곡률 = 12 / (
        선택반지름**6 + 보정길이**6
    )

    z1, z2 = st.columns(2)

    z1.metric(
        "고전 모형의 곡률",
        f"{고전_선택곡률:.4e}"
    )

    z2.metric(
        "가상 양자 보정 곡률",
        f"{양자_선택곡률:.4e}"
    )

    st.markdown("### 3. 블랙홀의 물리적 특징")

    with st.expander("사건의 지평선"):
        st.write("""
        사건의 지평선은 외부로 빛이 탈출할 수 없는
        영역의 경계입니다.

        슈바르츠실트 블랙홀에서는
        r = 2GM/c²에 해당합니다.
        """)

    with st.expander("고전적 특이점"):
        st.write("""
        고전적인 슈바르츠실트 해에서는
        r = 0에서 곡률 불변량이 발산합니다.

        이것은 고전 이론이 그 영역에서
        더 이상 충분한 설명을 제공하지 못한다는
        문제를 보여줍니다.
        """)

    with st.expander("양자중력의 가능성"):
        st.write("""
        루프 양자중력과 다른 양자중력 접근법은
        고전적 특이점 문제를 해결할 가능성을 연구합니다.

        그러나 블랙홀 내부의 실제 물리적 구조가
        무엇인지는 아직 확정되지 않았습니다.
        """)

# =========================================================
# 탭 4. 추가 차원
# =========================================================

with 탭[3]:

    st.header("🧬 추가 차원 실험실")

    st.write("""
    초끈이론에서 연구되는 추가 공간 차원의
    상대적 크기 변화를 탐구합니다.
    """)

    차원그래프 = go.Figure()

    차원그래프.add_trace(go.Scatter(
        x=시간,
        y=추가차원,
        name="추가 차원 크기 지표",
        fill="tozeroy",
        line=dict(color="#f472b6", width=3)
    ))

    차원그래프.update_layout(
        template="plotly_dark",
        height=400,
        xaxis_title="시간",
        yaxis_title="상대적 크기"
    )

    st.plotly_chart(
        차원그래프,
        use_container_width=True
    )

    q1, q2 = st.columns(2)

    q1.metric(
        "초기 추가 차원 지표",
        f"{추가차원[0]:.3f}"
    )

    q2.metric(
        "최종 추가 차원 지표",
        f"{추가차원[-1]:.3f}"
    )

    st.info(
        "이 값은 실제 칼라비-야우 다양체의 크기 계산이 아닌 "
        "교육용 상대 크기 지표입니다."
    )

# =========================================================
# 탭 5. 물리 이론과 데이터
# =========================================================

with 탭[4]:

    st.header("📚 물리 이론 자료실")

    st.subheader("초끈이론에서 영감을 얻은 모형")

    st.latex(
        r"a_s(t)=\cosh(t/\tau)^p"
    )

    st.write("""
    비특이 우주 바운스의 형태를 보여 주는
    현상론적 모형입니다.

    정식 초끈이론의 완전한 우주론 해는 아닙니다.
    """)

    st.divider()

    st.subheader("루프 양자우주론 모형")

    st.latex(
        r"a_L(t)=[1+(t/\tau)^2]^q"
    )

    st.write("""
    우주 크기가 0에 도달하지 않고
    최소 크기를 갖는 바운스 형태를 표현합니다.
    """)

    st.divider()

    st.subheader("고전 우주 모형")

    st.latex(
        r"a_C(t)\propto\sqrt{t},\quad t>0"
    )

    st.write("""
    복사 지배 우주의 고전적인 팽창 모형입니다.
    t = 0에서 고전적 특이점을 갖습니다.
    """)

    st.divider()

    st.subheader("블랙홀 곡률")

    st.latex(
        r"K=\frac{48G^2M^2}{c^4r^6}"
    )

    st.write("""
    슈바르츠실트 블랙홀의 시공간 곡률을 나타내는
    크레치만 스칼라입니다.
    """)

    st.divider()

    st.subheader("📊 우주 실험 데이터")

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

초끈이론 · 루프 양자중력 · 블랙홀 · 우주론

<br>

교육용 과학 가상실험 환경

<br><br>

VERSION 2.0

</div>
""", unsafe_allow_html=True)
