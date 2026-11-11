
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# =====================================================
# QUANTUM UNIVERSE LAB
# 양자 우주 실험실 v1.1
# =====================================================

st.set_page_config(
    page_title="양자 우주 실험실",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# 화면 디자인
# =====================================================

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

# =====================================================
# 메인 제목
# =====================================================

st.title("🌌 양자 우주 실험실")
st.subheader("초끈이론과 루프 양자중력으로 탐구하는 우주")

st.markdown("""
이곳은 서로 다른 양자중력 이론을 바탕으로
우주의 탄생과 진화, 시공간의 구조를 탐구하는
가상 물리 실험실입니다.
""")

st.caption("QUANTUM UNIVERSE LAB | 버전 1.1")

st.divider()

# =====================================================
# 실험 설정
# =====================================================

st.sidebar.title("⚙️ 실험 설정")

st.sidebar.markdown("### 🌌 우주 초기 조건")

duration = st.sidebar.slider(
    "시뮬레이션 시간 범위",
    2.0, 20.0, 10.0, 1.0
)

time_scale = st.sidebar.slider(
    "시간 척도",
    0.5, 5.0, 2.0, 0.1
)

st.sidebar.markdown("### 🧬 초끈이론 모형")

string_power = st.sidebar.slider(
    "우주 팽창 지수",
    0.1, 0.8, 0.35, 0.05
)

extra_dimension = st.sidebar.slider(
    "추가 차원 변화 계수",
    0.0, 2.0, 0.5, 0.1
)

st.sidebar.markdown("### 🔵 루프 양자중력 모형")

loop_power = st.sidebar.slider(
    "양자 보정 지수",
    0.1, 0.8, 0.25, 0.05
)

st.sidebar.divider()

st.sidebar.info("""
실험 변수는 교육용 단순화 모형의
매개변수입니다.

실제 자연계의 측정된 물리 상수와
동일한 값은 아닙니다.
""")

# =====================================================
# 물리 시뮬레이션 함수
# =====================================================

def 초끈이론_모형(t, tau, power):
    """
    초끈이론에서 영감을 얻은
    현상론적 우주 바운스 모형

    a(t) = cosh(t/tau)^power

    정식 초끈이론의 완전한 해는 아님.
    """

    x = t / tau
    abs_x = np.abs(x)

    log_cosh = (
        abs_x
        + np.log1p(np.exp(-2 * abs_x))
        - np.log(2)
    )

    return np.exp(power * log_cosh)


def 루프양자중력_모형(t, tau, power):
    """
    단순화된 루프 양자우주론 모형

    a(t) = (1 + (t/tau)^2)^power

    최소 크기가 0보다 큰
    양자 바운스를 표현함.
    """

    x = t / tau

    return np.power(1 + x**2, power)


def 고전우주_모형(t, tau):
    """
    복사 지배 고전 팽창 우주

    a(t) ∝ sqrt(t)

    t = 0에서 특이점이 발생하는
    고전적 기준 모형.
    """

    t_positive = np.maximum(t, 0)

    return np.sqrt(t_positive / tau)


# =====================================================
# 시뮬레이션 계산
# =====================================================

시간 = np.linspace(-duration, duration, 500)

초끈우주 = 초끈이론_모형(
    시간, time_scale, string_power
)

루프우주 = 루프양자중력_모형(
    시간, time_scale, loop_power
)

고전우주 = 고전우주_모형(
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

# =====================================================
# 실험 데이터
# =====================================================

데이터 = pd.DataFrame({
    "시간": 시간,
    "초끈이론 우주": 초끈우주,
    "루프 양자중력 우주": 루프우주,
    "고전 우주": 고전우주,
    "추가 차원 크기 지표": 추가차원,
    "초끈이론 팽창률": 초끈_팽창률,
    "루프 양자중력 팽창률": 루프_팽창률
})

# =====================================================
# 우주 상태
# =====================================================

st.header("📊 현재 우주 시뮬레이션 상태")

a, b, c, d = st.columns(4)

with a:
    st.metric(
        "초끈이론 최소 우주 크기",
        f"{np.min(초끈우주):.3f}"
    )

with b:
    st.metric(
        "루프 양자중력 최소 우주 크기",
        f"{np.min(루프우주):.3f}"
    )

with c:
    st.metric(
        "초끈이론 최대 우주 크기",
        f"{np.max(초끈우주):.3f}"
    )

with d:
    st.metric(
        "루프 양자중력 최대 우주 크기",
        f"{np.max(루프우주):.3f}"
    )

st.divider()

# =====================================================
# 실험실 탭
# =====================================================

탭1, 탭2, 탭3, 탭4 = st.tabs([
    "🌌 우주 이론 비교",
    "🪐 3차원 시공간",
    "🧬 추가 차원 실험실",
    "📚 물리 이론 및 데이터"
])

# =====================================================
# 탭 1 : 우주 이론 비교
# =====================================================

with 탭1:

    st.subheader("우주 팽창 비교 실험")

    st.write("""
    세 가지 우주 모형의 시간에 따른
    우주 크기 변화를 비교합니다.
    """)

    그래프 = go.Figure()

    그래프.add_trace(go.Scatter(
        x=시간,
        y=초끈우주,
        mode="lines",
        name="초끈이론 모형",
        line=dict(color="#a78bfa", width=3)
    ))

    그래프.add_trace(go.Scatter(
        x=시간,
        y=루프우주,
        mode="lines",
        name="루프 양자중력 모형",
        line=dict(color="#38bdf8", width=3)
    ))

    그래프.add_trace(go.Scatter(
        x=시간,
        y=고전우주,
        mode="lines",
        name="고전 우주 모형",
        line=dict(
            color="#fbbf24",
            width=2,
            dash="dash"
        )
    ))

    그래프.add_vline(
        x=0,
        line_dash="dot",
        line_color="white",
        annotation_text="바운스 기준 시점"
    )

    그래프.update_layout(
        template="plotly_dark",
        height=500,
        xaxis_title="시간",
        yaxis_title="우주 크기 척도",
        hovermode="x unified",
        legend=dict(orientation="h")
    )

    st.plotly_chart(
        그래프,
        use_container_width=True
    )

    st.subheader("우주 팽창률 비교")

    팽창그래프 = go.Figure()

    팽창그래프.add_trace(go.Scatter(
        x=시간,
        y=초끈_팽창률,
        name="초끈이론",
        line=dict(color="#a78bfa", width=2)
    ))

    팽창그래프.add_trace(go.Scatter(
        x=시간,
        y=루프_팽창률,
        name="루프 양자중력",
        line=dict(color="#38bdf8", width=2)
    ))

    팽창그래프.update_layout(
        template="plotly_dark",
        height=350,
        xaxis_title="시간",
        yaxis_title="팽창률 H(t)",
        hovermode="x unified"
    )

    st.plotly_chart(
        팽창그래프,
        use_container_width=True
    )

    st.info("""
    팽창률이 양수이면 우주가 팽창하고,
    음수이면 우주가 수축하는 것으로 해석합니다.

    팽창률이 0을 통과하는 지점은
    우주 크기가 최소 또는 최대가 되는
    전환점일 수 있습니다.
    """)

# =====================================================
# 탭 2 : 3차원 시공간
# =====================================================

with 탭2:

    st.subheader("🌌 3차원 우주 시각화")

    st.write("""
    시간에 따른 우주의 크기 변화를
    3차원 표면으로 표현합니다.

    가로축과 세로축은 공간을,
    높이축은 시간을 나타냅니다.
    """)

    각도 = np.linspace(
        0, 2 * np.pi, 70
    )

    시간격자 = np.linspace(
        -duration, duration, 100
    )

    T, THETA = np.meshgrid(
        시간격자, 각도
    )

    A1 = 초끈이론_모형(
        T, time_scale, string_power
    )

    A2 = 루프양자중력_모형(
        T, time_scale, loop_power
    )

    X1 = A1 * np.cos(THETA)
    Y1 = A1 * np.sin(THETA)

    X2 = A2 * np.cos(THETA)
    Y2 = A2 * np.sin(THETA)

    우주3D = go.Figure()

    우주3D.add_trace(go.Surface(
        x=X1,
        y=Y1,
        z=T,
        colorscale=[
            [0, "#312e81"],
            [0.5, "#8b5cf6"],
            [1, "#c4b5fd"]
        ],
        opacity=0.78,
        name="초끈이론 우주",
        showscale=False
    ))

    우주3D.add_trace(go.Surface(
        x=X2,
        y=Y2,
        z=T,
        colorscale=[
            [0, "#164e63"],
            [0.5, "#0891b2"],
            [1, "#67e8f9"]
        ],
        opacity=0.65,
        name="루프 양자중력 우주",
        showscale=False
    ))

    우주3D.update_layout(
        template="plotly_dark",
        height=700,
        scene=dict(
            xaxis_title="공간 X",
            yaxis_title="공간 Y",
            zaxis_title="시간",
            aspectmode="manual",
            aspectratio=dict(
                x=1,
                y=1,
                z=2
            )
        )
    )

    st.plotly_chart(
        우주3D,
        use_container_width=True
    )

    st.caption("""
    이 시각화는 우주 크기 척도의 시간 변화를
    원형 공간 단면으로 표현한 교육용 모형입니다.
    실제 시공간의 완전한 수치해석 결과는 아닙니다.
    """)

# =====================================================
# 탭 3 : 추가 차원 실험실
# =====================================================

with 탭3:

    st.subheader("🧬 추가 차원 변화 실험")

    st.write("""
    초끈이론에서는 우리가 경험하는
    3차원 공간 이외의 추가 공간 차원이
    존재할 가능성을 연구합니다.

    아래 그래프는 추가 차원의 상대적 크기 변화를
    가상 매개변수로 표현합니다.
    """)

    차원그래프 = go.Figure()

    차원그래프.add_trace(go.Scatter(
        x=시간,
        y=추가차원,
        name="추가 차원 크기 지표",
        fill="tozeroy",
        line=dict(
            color="#f472b6",
            width=3
        )
    ))

    차원그래프.update_layout(
        template="plotly_dark",
        height=400,
        xaxis_title="시간",
        yaxis_title="상대적 크기",
        hovermode="x unified"
    )

    st.plotly_chart(
        차원그래프,
        use_container_width=True
    )

    st.subheader("추가 차원 상태")

    x, y = st.columns(2)

    with x:
        st.metric(
            "초기 추가 차원 지표",
            f"{추가차원[0]:.3f}"
        )

    with y:
        st.metric(
            "최종 추가 차원 지표",
            f"{추가차원[-1]:.3f}"
        )

    st.info("""
    이 그래프는 추가 차원의 크기를 나타내는
    교육용 장난감 모형입니다.

    실제 끈이론의 칼라비-야우 다양체나
    모듈라이 방정식을 계산한 것은 아닙니다.
    """)

# =====================================================
# 탭 4 : 물리 이론 및 데이터
# =====================================================

with 탭4:

    st.subheader("📚 사용된 물리 모형")

    st.markdown("### 1. 초끈이론에서 영감을 얻은 모형")

    st.latex(
        r"a_s(t)=\cosh\left(\frac{t}{\tau}\right)^p"
    )

    st.write("""
    시간에 따라 우주의 크기가 변화하는
    비특이 바운스 형태의 현상론적 모형입니다.

    p는 우주 팽창 곡선의 모양을 결정합니다.

    정식 초끈이론의 완전한 방정식은 아닙니다.
    """)

    st.divider()

    st.markdown("### 2. 루프 양자우주론 모형")

    st.latex(
        r"a_L(t)=\left[1+\left(\frac{t}{\tau}\right)^2\right]^q"
    )

    st.write("""
    양자 보정으로 인해 우주의 크기가
    0에 도달하지 않고 최소 크기를 갖는
    바운스 형태를 표현한 단순화 모형입니다.
    """)

    st.divider()

    st.markdown("### 3. 고전적인 팽창 우주")

    st.latex(
        r"a_C(t)\propto\sqrt{t},\quad t>0"
    )

    st.write("""
    복사 지배 시대의 고전 우주 팽창을
    나타내는 기준 모형입니다.

    t = 0에서 특이점을 갖습니다.
    """)

    st.divider()

    st.subheader("📊 실험 데이터")

    st.dataframe(
        데이터,
        use_container_width=True,
        hide_index=True
    )

    CSV = 데이터.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="📥 실험 데이터 CSV 다운로드",
        data=CSV,
        file_name="양자_우주_실험_결과.csv",
        mime="text/csv"
    )

# =====================================================
# 하단
# =====================================================

st.divider()

st.markdown("""
<div style="text-align:center; padding:25px; color:#8ca4c8;">

<h3>🌌 양자 우주 실험실</h3>

초끈이론과 루프 양자중력으로 탐구하는 우주

<br><br>

교육용 과학 가상실험 환경

<br>

QUANTUM UNIVERSE LAB

</div>
""", unsafe_allow_html=True)
