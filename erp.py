import streamlit as st
import pandas as pd

st.set_page_config(page_title="簡易製造業進銷存", layout="wide")

st.title("🏭 簡易 ERP 原型 - 成本計算系統")

# 1. 模擬資料庫：原物料清單 (包含最近一次採購價)
if 'materials' not in st.session_state:
    st.session_state.materials = pd.DataFrame({
        '物料編號': ['M001', 'M002', 'M003', 'M004', 'M005'],
        '品名': ['鋼板', '馬達', '風扇葉片', '控制模組', '緊固件'],
        '最近採購單價': [100.0, 500.0, 150.0, 300.0, 10.0]
    })

# 2. 模擬資料庫：成品 BOM (5種原料組成)
bom_data = {
    '成品名稱': '工業級風機',
    '結構': [
        {'編號': 'M001', '用量': 2},
        {'編號': 'M002', '用量': 1},
        {'編號': 'M003', '用量': 1},
        {'編號': 'M004', '用量': 1},
        {'編號': 'M005', '用量': 20},
    ]
}

# 介面分欄
col1, col2 = st.columns(2)

with col1:
    st.header("📦 原物料價格管理")
    st.write("在此更新最近一次採購價格：")
    
    # 建立一個簡單的編輯表單
    edited_df = st.data_editor(st.session_state.materials, num_rows="fixed")
    if st.button("儲存採購價更新"):
        st.session_state.materials = edited_df
        st.success("價格已同步到系統！")

with col2:
    st.header("💰 成品成本分析")
    st.subheader(f"產品：{bom_data['成品名稱']}")
    
    # 計算成本邏輯
    total_cost = 0
    details = []
    
    for item in bom_data['結構']:
        # 從資料庫找最新的單價
        price = st.session_state.materials.loc[st.session_state.materials['物料編號'] == item['編號'], '最近採購單價'].values[0]
        subtotal = price * item['用量']
        total_cost += subtotal
        details.append({
            '物料': item['編號'],
            '單價': price,
            '用量': item['用量'],
            '小計': subtotal
        })
    
    # 顯示成本明細表
    st.table(pd.DataFrame(details))
    
    st.metric(label="預估總材料成本 (最新採購價)", value=f"${total_cost:,.2f}")

st.info("💡 管理員提示：當您在左側修改『鋼板』的單價後點擊儲存，右側的成品成本會立即自動重新計算。")
