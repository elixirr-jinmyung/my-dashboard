import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import base64
from io import BytesIO

# 페이지 설정
st.set_page_config(
    page_title="여수 화학사고 대시보드",
    page_icon="⚠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 스타일 (보라색 톤)
st.markdown("""
    <style>
    /* 페이지 배경 */
    .stApp {
        background-color: #F8F6FC;
    }
    
    .stMainBlockContainer {
        background-color: transparent;
    }
    
    /* 제목 스타일 */
    .title-style {
        font-size: 2.5rem;
        font-weight: 700;
        color: #6C3FA0;
        margin-bottom: 0.2rem;
    }
    
    /* 설명 스타일 */
    .subtitle-style {
        font-size: 1.1rem;
        color: #888888;
        font-weight: 400;
        margin-bottom: 1rem;
    }
    
    /* 섹션 컨테이너 - 글래스모피즘 */
    [data-testid="column"] {
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        box-shadow: 0 8px 32px rgba(108, 63, 160, 0.1) !important;
        margin-bottom: 1rem !important;
    }
    
    /* 메트릭 카드 - 글래스모피즘 */
    [data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        box-shadow: 0 8px 32px rgba(108, 63, 160, 0.12) !important;
    }
    
    /* 서브헤더 스타일 */
    .stSubheader {
        color: #6C3FA0 !important;
        font-weight: 600 !important;
        padding-top: 1rem !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 1px solid rgba(224, 213, 245, 0.5) !important;
    }
    
    /* 사이드바 - 글래스모피즘 */
    .stSidebar {
        background: rgba(245, 240, 251, 0.7) !important;
        backdrop-filter: blur(10px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.3) !important;
    }
    
    .stSidebar [data-testid="stHeader"] {
        color: #6C3FA0 !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        text-shadow: 0 2px 4px rgba(108, 63, 160, 0.1) !important;
    }
    
    /* 선택 버튼 배경 - 글래스모피즘 */
    .stSidebar .stMultiSelect [data-baseweb="tag"] {
        background: rgba(108, 63, 160, 0.8) !important;
        backdrop-filter: blur(8px) !important;
    }
    
    .stSidebar .stSelectbox [data-baseweb="select"] {
        border: 1px solid rgba(108, 63, 160, 0.5) !important;
    }
    
    /* 탭 - 글래스모피즘 */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.6) !important;
        backdrop-filter: blur(10px) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 12px 12px 0 0 !important;
        padding: 0.5rem !important;
        gap: 0.3rem !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.5) !important;
        backdrop-filter: blur(8px) !important;
        border-radius: 8px 8px 0 0 !important;
        color: #666666 !important;
        font-weight: 500 !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(108, 63, 160, 0.8) !important;
        backdrop-filter: blur(10px) !important;
        color: white !important;
        border: 1px solid rgba(108, 63, 160, 0.5) !important;
    }
    
    /* 차트 컨테이너 - 글래스모피즘 */
    .stPlotly {
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        padding: 1rem !important;
        box-shadow: 0 8px 32px rgba(108, 63, 160, 0.1) !important;
    }
    
    /* 데이터프레임 - 글래스모피즘 */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }
    
    /* 버튼 - 글래스모피즘 */
    .stButton > button {
        background: rgba(108, 63, 160, 0.8) !important;
        backdrop-filter: blur(8px) !important;
        color: white !important;
        border: 1px solid rgba(108, 63, 160, 0.4) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        box-shadow: 0 8px 16px rgba(108, 63, 160, 0.2) !important;
    }
    
    .stButton > button:hover {
        background: rgba(108, 63, 160, 0.9) !important;
        box-shadow: 0 12px 24px rgba(108, 63, 160, 0.3) !important;
    }
    
    /* 구분선 */
    hr {
        border-color: rgba(224, 213, 245, 0.5) !important;
    }
    
    /* 경고 및 정보 메시지 - 글래스모피즘 */
    .stAlert {
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 8px 32px rgba(108, 63, 160, 0.1) !important;
    }
    </style>
""", unsafe_allow_html=True)

# 데이터 로딩 함수
@st.cache_data
def load_chemical_accident_data():
    """화학 사고 정보 데이터 로드"""
    try:
        df = pd.read_csv("data/4. 화학 사고 정보.csv", encoding="cp949")
    except UnicodeDecodeError:
        df = pd.read_csv("data/4. 화학 사고 정보.csv", encoding="utf-8")
    return df

@st.cache_data
def load_ghg_data():
    """GHG 배출량 데이터 로드"""
    return pd.read_csv("data/processed/ghg_emission_by_chemical_industry.csv", encoding="utf-8-sig")

@st.cache_data
def load_pollution_data():
    """공기 오염 상관계수 데이터 로드"""
    return pd.read_csv("data/processed/yeosu_pollution_correlation.csv", index_col=0)

@st.cache_data
def load_water_data():
    """수질 분석 데이터 로드"""
    return pd.read_csv("data/processed/yeosu_water_quality_analysis.csv")

def filter_accident_data(df, province, districts, year_min, year_max):
    """
    조건에 따라 사고 데이터 필터링
    
    Parameters:
    - df: 원본 데이터프레임
    - province: 선택한 시도
    - districts: 선택한 시군구 리스트
    - year_min: 최소 연도
    - year_max: 최대 연도
    
    Returns:
    - 필터링된 데이터프레임
    """
    filtered = df[
        (df['시도'] == province) &
        (df['시군구'].isin(districts)) &
        (df['연도'] >= year_min) &
        (df['연도'] <= year_max)
    ].copy()
    return filtered

@st.cache_data
def get_watermark_logo():
    """반투명한 로고 이미지를 Base64로 반환"""
    try:
        img = Image.open("data/yspetchem-logo.webp").convert("RGBA")
        # 투명도 15% 적용 (255 * 0.15 = 약 38)
        alpha = img.split()[3]
        alpha = alpha.point(lambda p: int(p * 0.15))
        img.putalpha(alpha)
        
        # Base64로 인코딩
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode()
        return f"data:image/png;base64,{img_base64}"
    except:
        return None

# 배경 워터마크 설정
watermark = get_watermark_logo()
if watermark:
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url('{watermark}');
        background-attachment: fixed;
        background-repeat: no-repeat;
        background-position: center;
        background-size: 500px 500px;
    }}
    </style>
    """, unsafe_allow_html=True)

# 제목
st.markdown('<div class="title-style">여수 화학사고 대시보드</div>', unsafe_allow_html=True)

# 한 줄 설명
st.markdown('<div class="subtitle-style">여수 지역 화학 산업 사고 데이터 분석 및 안전 모니터링 시스템</div>', unsafe_allow_html=True)

# 데이터 로드
df = load_chemical_accident_data()
df['연도'] = pd.to_datetime(df['사고일자']).dt.year

# ==================== 사이드바: 조회 조건 ====================
with st.sidebar:
    st.header("🔍 조회 조건")
    
    # 시도 선택
    provinces = sorted(df['시도'].unique())
    
    # 전남을 기본값으로 설정
    default_index = list(provinces).index('전남') if '전남' in provinces else 0
    
    selected_province = st.selectbox(
        "시도 선택",
        provinces,
        index=default_index
    )
    
    # 선택한 시도의 시군구 목록
    province_districts = sorted(df[df['시도'] == selected_province]['시군구'].unique())
    
    # 시군구 다중 선택
    selected_districts = st.multiselect(
        "시군구 선택 (여러 개 선택 가능)",
        province_districts,
        default=province_districts  # 기본값: 모두 선택
    )
    
    # 시군구가 선택되지 않았을 경우 처리
    if not selected_districts:
        selected_districts = province_districts
    
    # 연도 범위 선택
    year_range = st.slider(
        "연도 범위 선택",
        min_value=2014,
        max_value=2025,
        value=(2014, 2025),
        step=1
    )
    
    st.divider()
    
    # 선택된 조건 표시
    st.subheader("📋 선택된 조건")
    st.write(f"**시도**: {selected_province}")
    st.write(f"**시군구**: {', '.join(selected_districts) if selected_districts else '선택 없음'}")
    st.write(f"**연도**: {year_range[0]} ~ {year_range[1]}")

# 필터링된 데이터프레임 생성
filtered_df = filter_accident_data(
    df,
    selected_province,
    selected_districts,
    year_range[0],
    year_range[1]
)

# ==================== 데이터 유효성 검사 ====================
st.write(f"**필터링 결과**: {len(filtered_df)}건의 데이터")

if len(filtered_df) == 0:
    st.warning("⚠️ 선택한 조건에 해당하는 데이터가 없습니다. 조건을 변경하여 다시 시도해주세요.")
    st.stop()

# 계산에 사용할 컬럼의 빈 값 처리
work_df = filtered_df.copy()

# 인명피해 관련 컬럼: NaN을 0으로 변환
casualty_columns = ['사망_직접', '사망_기타', '부상_직접', '부상_기타']
for col in casualty_columns:
    work_df[col] = work_df[col].fillna(0)

st.divider()

# ==================== 지표 카드 4개 ====================
st.subheader("📊 핵심 지표")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("사고 건수", f"{len(work_df):,} 건")

with col2:
    total_casualties = (work_df['사망_직접'].fillna(0) + 
                       work_df['사망_기타'].fillna(0) + 
                       work_df['부상_직접'].fillna(0) + 
                       work_df['부상_기타'].fillna(0)).sum()
    st.metric("인명 피해", f"{int(total_casualties):,} 명")

with col3:
    most_common_cause = work_df['사고원인'].dropna().value_counts().index[0] if len(work_df[work_df['사고원인'].notna()]) > 0 else "-"
    st.metric("주요 원인", most_common_cause)

with col4:
    latest_date = work_df['사고일자'].max() if len(work_df) > 0 else "-"
    st.metric("최근 사고", str(latest_date))

st.divider()

# ==================== 2:1 레이아웃: 차트와 연도별 집계표 ====================
col_chart, col_table = st.columns([2, 1], gap="medium")

with col_chart:
    # 연도별 사고 건수 추이 (Bar Chart)
    yearly_accidents = work_df.groupby('연도').size().reset_index(name='사고건수')
    
    fig_bar = go.Figure(data=[
        go.Bar(
            x=yearly_accidents['연도'],
            y=yearly_accidents['사고건수'],
            text=yearly_accidents['사고건수'],
            textposition='auto',
            marker=dict(color='#6C3FA0', opacity=0.8),
            hovertemplate='연도: %{x}<br>사고 건수: %{y}건<extra></extra>'
        )
    ])
    
    fig_bar.update_layout(
        title="연도별 사고 발생 추이",
        xaxis_title="연도",
        yaxis_title="사고 건수 (건)",
        template='plotly_white',
        paper_bgcolor='rgba(255, 255, 255, 0.85)',
        height=400,
        showlegend=False,
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    st.plotly_chart(fig_bar, width='stretch')

with col_table:
    # 연도별 집계표 (상세 데이터)
    st.markdown("**상세 데이터**")
    
    yearly_stats = work_df.groupby('연도').size().reset_index(name='건수')
    yearly_stats = yearly_stats.sort_values('연도', ascending=False)
    
    # 변화율 계산
    yearly_stats['변화율'] = yearly_stats['건수'].diff(periods=-1)
    yearly_stats['변화율(%)'] = (yearly_stats['변화율'] / yearly_stats['건수'].shift(-1) * 100).round(1)
    
    # 표시 용 데이터
    display_stats = yearly_stats[['연도', '건수', '변화율(%)']].copy()
    display_stats['연도'] = display_stats['연도'].astype(int).astype(str)
    display_stats['건수'] = display_stats['건수'].astype(int)
    
    # 변화율(%)을 문자열로 변환하고 마지막 행은 '-'으로 설정
    display_stats['변화율(%)'] = display_stats['변화율(%)'].astype(str)
    display_stats.loc[display_stats.index[-1], '변화율(%)'] = '-'
    
    # 스타일링
    def color_change(val):
        if val == '-':
            return 'color: gray'
        elif val == 'nan':
            return 'color: gray'
        else:
            try:
                num_val = float(val)
                if num_val > 0:
                    return 'color: red'
                else:
                    return 'color: green'
            except:
                return 'color: gray'
    
    styled_table = display_stats.style.map(color_change, subset=['변화율(%)'])
    st.dataframe(styled_table, use_container_width=True, hide_index=True)

st.divider()

# ==================== 추가 분석 탭 ====================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🔄 유형",
    "⚖️ 원인×유형",
    "🏭 산업 배경",
    "💨 공기",
    "💧 물",
    "📋 데이터"
])

# ==================== TAB 1: 유형 ====================
with tab1:
    st.subheader("사고유형별 비율")
    
    accident_type = work_df['사고유형'].dropna().value_counts().reset_index()
    accident_type.columns = ['사고유형', '건수']
    
    fig_pie = px.pie(
        accident_type,
        values='건수',
        names='사고유형',
        title="사고유형 분포",
        color_discrete_sequence=px.colors.sequential.Purples_r
    )
    fig_pie.update_layout(paper_bgcolor='rgba(255, 255, 255, 0.85)')
    
    st.plotly_chart(fig_pie, width='stretch')

# ==================== TAB 2: 원인×유형 ====================
with tab2:
    st.subheader("사고원인별 사고유형 분포")
    
    cause_type = work_df[work_df['사고원인'].notna() & work_df['사고유형'].notna()].groupby(['사고원인', '사고유형']).size().reset_index(name='건수')
    
    fig_stacked = px.bar(
        cause_type,
        x='사고원인',
        y='건수',
        color='사고유형',
        barmode='stack',
        title="사고원인별 사고유형 구성",
        labels={'건수': '건수 (건)', '사고원인': '사고원인'},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    fig_stacked.update_layout(template='plotly_white', paper_bgcolor='rgba(255, 255, 255, 0.85)')
    st.plotly_chart(fig_stacked, width='stretch')

# ==================== TAB 3: 산업 배경 ====================
with tab3:
    st.subheader("화학 산업 GHG 배출량 추이")
    
    ghg_df = load_ghg_data()
    
    fig_ghg = px.line(
        ghg_df,
        x='연도',
        y='배출량',
        color='항목',
        markers=True,
        title="연도별 GHG 배출량 추이",
        labels={'배출량': '배출량 (톤)', '연도': '연도'},
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig_ghg.update_layout(template='plotly_white', paper_bgcolor='rgba(255, 255, 255, 0.85)', hovermode='x unified')
    st.plotly_chart(fig_ghg, width='stretch')

# ==================== TAB 4: 공기 ====================
with tab4:
    st.subheader("여수 대기 오염 물질 상관계수")
    
    pollution_df = load_pollution_data()
    
    fig_heatmap = px.imshow(
        pollution_df,
        labels=dict(x="오염물질", y="오염물질", color="상관계수"),
        title="대기 오염 물질 상관관계 히트맵",
        color_continuous_scale="RdBu",
        zmin=-1,
        zmax=1
    )
    
    fig_heatmap.update_layout(width=700, height=700, paper_bgcolor='rgba(255, 255, 255, 0.85)')
    st.plotly_chart(fig_heatmap, width='stretch')

# ==================== TAB 5: 물 ====================
with tab5:
    st.subheader("여수 수질 지표 비교")
    
    water_df = load_water_data()
    water_display = water_df[['수질지표', '여수값', '대한해협평균']].copy()
    
    fig_water = go.Figure(data=[
        go.Bar(name='여수값', x=water_display['수질지표'], y=water_display['여수값']),
        go.Bar(name='대한해협평균', x=water_display['수질지표'], y=water_display['대한해협평균'])
    ])
    
    fig_water.update_layout(
        barmode='group',
        title="여수 vs 대한해협 평균 수질 지표 비교",
        xaxis_title="수질지표",
        yaxis_title="수치",
        template='plotly_white',
        paper_bgcolor='rgba(255, 255, 255, 0.85)',
        hovermode='x'
    )
    
    st.plotly_chart(fig_water, width='stretch')

# ==================== TAB 6: 데이터 ====================
with tab6:
    st.subheader("화학 사고 정보 필터링된 데이터")
    st.dataframe(work_df, use_container_width=True, height=600)
