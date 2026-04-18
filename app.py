import streamlit as st

st.set_page_config(
    page_title="投資機長箱 | Captain Albert Fan",
    page_icon="✈️",
    layout="wide"
)

# ==========================================
# 密碼保護
# ==========================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Noto+Sans+TC:wght@300;400;500&display=swap');

    * { margin: 0; padding: 0; box-sizing: border-box; }

    .stApp {
        background: #0a0f1e;
        min-height: 100vh;
    }

    .login-wrap {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 80vh;
        gap: 24px;
    }

    .login-logo {
        font-family: 'Playfair Display', serif;
        font-size: 3.2rem;
        font-weight: 900;
        color: #fff;
        letter-spacing: -1px;
        text-align: center;
    }

    .login-logo span {
        color: #c8a84b;
    }

    .login-sub {
        font-family: 'Noto Sans TC', sans-serif;
        font-size: 0.95rem;
        color: #8899bb;
        letter-spacing: 4px;
        text-transform: uppercase;
        text-align: center;
    }

    .login-plane {
        font-size: 4rem;
        margin-bottom: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="login-wrap">
        <div class="login-plane">✈️</div>
        <div class="login-logo">Captain Albert Fan<br><span>投資機長箱</span></div>
        <div class="login-sub">Internal Tools Portal · 內部工具平台</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        pwd = st.text_input("", placeholder="輸入授權碼", type="password", label_visibility="collapsed")
        if pwd:
            if pwd == st.secrets.get("PORTAL_PASSWORD", "5428"):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("密碼錯誤")
    st.stop()

# ==========================================
# 主介面樣式
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Noto+Sans+TC:wght@300;400;500;700&display=swap');

* { box-sizing: border-box; }

.stApp {
    background: #07090f;
    min-height: 100vh;
}

/* 隱藏 Streamlit 預設元素 */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem !important; max-width: 1400px !important; }

/* 頂部標題列 */
.portal-header {
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 28px 0 32px 0;
    border-bottom: 1px solid #1e2a42;
    margin-bottom: 36px;
}

.portal-icon {
    font-size: 2.8rem;
    filter: drop-shadow(0 0 12px rgba(200,168,75,0.4));
}

.portal-title {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 900;
    color: #ffffff;
    line-height: 1.1;
    letter-spacing: -0.5px;
}

.portal-title span {
    color: #c8a84b;
}

.portal-subtitle {
    font-family: 'Noto Sans TC', sans-serif;
    font-size: 0.78rem;
    color: #4a6080;
    letter-spacing: 3px;
    margin-top: 4px;
    text-transform: uppercase;
}

/* 分類標題 */
.section-label {
    font-family: 'Noto Sans TC', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #c8a84b;
    padding: 0 0 10px 2px;
    border-bottom: 1px solid #1e2a42;
    margin-bottom: 16px;
    margin-top: 32px;
}

/* 工具卡片 */
.tool-card {
    background: linear-gradient(135deg, #0d1525 0%, #111827 100%);
    border: 1px solid #1e2d42;
    border-radius: 12px;
    padding: 20px 22px;
    margin-bottom: 14px;
    transition: all 0.25s ease;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    text-decoration: none;
    display: block;
}

.tool-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: #c8a84b;
    opacity: 0;
    transition: opacity 0.25s;
}

.tool-card:hover {
    border-color: #c8a84b55;
    background: linear-gradient(135deg, #111d30 0%, #151f2e 100%);
    transform: translateX(4px);
    box-shadow: 0 4px 24px rgba(200,168,75,0.08);
    text-decoration: none;
}

.tool-card:hover::before {
    opacity: 1;
}

.tool-card-inner {
    display: flex;
    align-items: center;
    gap: 16px;
}

.tool-emoji {
    font-size: 1.8rem;
    min-width: 40px;
    text-align: center;
    filter: drop-shadow(0 0 6px rgba(200,168,75,0.2));
}

.tool-info { flex: 1; }

.tool-name {
    font-family: 'Noto Sans TC', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: #e8edf5;
    margin-bottom: 4px;
}

.tool-desc {
    font-family: 'Noto Sans TC', sans-serif;
    font-size: 0.75rem;
    color: #4a6080;
    line-height: 1.5;
}

.tool-arrow {
    font-size: 1rem;
    color: #2a3a50;
    transition: color 0.2s, transform 0.2s;
}

.tool-card:hover .tool-arrow {
    color: #c8a84b;
    transform: translateX(3px);
}

/* 底部 */
.portal-footer {
    margin-top: 48px;
    padding-top: 20px;
    border-top: 1px solid #1e2a42;
    text-align: center;
    font-family: 'Noto Sans TC', sans-serif;
    font-size: 0.72rem;
    color: #2a3a50;
    letter-spacing: 2px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 頂部 Header
# ==========================================
st.markdown("""
<div class="portal-header">
    <div class="portal-icon">✈️</div>
    <div>
        <div class="portal-title">Captain Albert Fan &nbsp;<span>投資機長箱</span></div>
        <div class="portal-subtitle">Internal Tools Portal · 富邦西湖財管 · 僅供內部使用</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 工具清單
# ==========================================
def tool_card(emoji, name, desc, url):
    st.markdown(f"""
    <a href="{url}" target="_blank" class="tool-card">
        <div class="tool-card-inner">
            <div class="tool-emoji">{emoji}</div>
            <div class="tool-info">
                <div class="tool-name">{name}</div>
                <div class="tool-desc">{desc}</div>
            </div>
            <div class="tool-arrow">→</div>
        </div>
    </a>
    """, unsafe_allow_html=True)

# ── ELN 工具 ──
st.markdown('<div class="section-label">⚡ ELN 工具</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    tool_card("🔍", "ELN 掃描器",
              "快速篩選符合條件的 ELN 標的，支援多維度過濾",
              "https://elnscreener-nwbrypd3slur3sqpq8yj8p.streamlit.app/")
    tool_card("📊", "ELN 劃線工具",
              "ELN 標的 ST/KI/KO 視覺化劃線分析",
              "https://eln-with-st-ki-ko-line-d53qyt9jwzrokyymhcjnqw.streamlit.app/")
    tool_card("📊", "ELN 劃線工具（含發行機構簡介）",
              "ELN 劃線 + 各發行機構背景資訊",
              "https://eln-with-issuer-st-ki-ko-line-4oinddsyfkb2os8a3qoydq.streamlit.app/")

with col2:
    tool_card("📱", "ELN 追蹤 · LINE 通知",
              "ELN 部位自動追蹤，觸發條件即時推播至 LINE",
              "https://eln-auto-tracking-notify-from-line-mq2agfcvksg3nvypgsgpjv.streamlit.app/")
    tool_card("📧", "ELN 追蹤 · Mail 通知",
              "ELN 部位自動追蹤，觸發條件寄送 Email 通知",
              "https://eln-auto-tracking-b67rpsggez8my2adgfdt3t.streamlit.app/")

# ── 債券工具 ──
st.markdown('<div class="section-label">📈 債券工具</div>', unsafe_allow_html=True)
col3, col4 = st.columns(2)

with col3:
    tool_card("📉", "常賣債券績效比較",
              "本行常見債券歷史績效走勢比較，含息總報酬分析",
              "https://bond-backtest-dnubuhdxkunvwf6fdhsnv3.streamlit.app/")

with col4:
    tool_card("💰", "雙元貨幣 (DCI) 回測",
              "DCI 歷史勝率與各情境回測分析",
              "https://edltm57vf5rtwkpeewcsb7.streamlit.app/")

# ── 投資組合工具 ──
st.markdown('<div class="section-label">📐 投資組合分析</div>', unsafe_allow_html=True)
col5, col6 = st.columns(2)

with col5:
    tool_card("📐", "最適投資組合優化器",
              "債券＋基金＋股票混合配置，蒙地卡羅模擬有效前緣",
              "https://efvudphrxax7qkpdxjiutj.streamlit.app/")
    tool_card("💼", "基金投組匯率避險分析",
              "基金組合匯率風險評估與避險策略試算",
              "https://5bhfmyrz5pyzymrzd68tfk.streamlit.app/")

with col6:
    tool_card("🎲", "投組優化＋滾動＋蒙地卡羅",
              "進階投組回測，含滾動勝率與蒙地卡羅未來情境模擬",
              "https://my-profolio-plus-rolling-tvbxtfnzzazebity7k8uxp.streamlit.app/")
    tool_card("💰", "金開心現金流試算",
              "債券＋基金＋ELN 混搭，試算每月配息現金流",
              "https://happy-asset-allocation-a2rrv3yrvfcb37ndnqbhec.streamlit.app/")
    tool_card("💰", "金開心強化版",
              "金開心現金流試算強化版，功能更完整",
              "https://jeqqkxvlpgljdeyxf8kuuh.streamlit.app/")

# ── 回測工具 ──
st.markdown('<div class="section-label">🔬 回測分析</div>', unsafe_allow_html=True)
col7, col8 = st.columns(2)

with col7:
    tool_card("📉", "動態鎖利回測",
              "設定動態停利條件，回測不同市場環境下的鎖利效益",
              "https://dynamic-take-profit-7hzznb5ki425dlgrsqptl9.streamlit.app/")

with col8:
    tool_card("📊", "A 跌多少後進場勝率分析",
              "指數/個股下跌 X% 後進場，各天期持有勝率統計",
              "https://sp500-backtest-lq7ryyzwnbgtvh2es6zhzv.streamlit.app/")

# ── 底部 ──
st.markdown("""
<div class="portal-footer">
    ✈️ &nbsp; CAPTAIN ALBERT FAN · 投資機長箱 &nbsp; · &nbsp;
    富邦銀行西湖分行財富管理 &nbsp; · &nbsp;
    僅供內部教育訓練使用，請勿外流
</div>
""", unsafe_allow_html=True)
