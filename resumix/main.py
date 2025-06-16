# from paddleocr import PaddleOCR
import streamlit as st

# Initialize session state
if "lang" not in st.session_state:
    st.session_state.lang = "en"

import sys
import os
from pathlib import Path
from langchain.agents import initialize_agent, AgentType
from tool.tool import tool_list
from resumix.utils.llm_client import LLMWrapper, LLMClient
from resumix.rewriter.resume_rewriter import ResumeRewriter

from resumix.config.config import Config

from streamlit_option_menu import option_menu

# Import card components
from resumix.components.cards.analysis_card import analysis_card
from resumix.components.cards.polish_card import polish_card
from resumix.components.cards.agent_card import agent_card
from resumix.components.cards.score_card import (
    display_score_card,
)
from resumix.components.cards.compare_card import compare_resume_sections

# Import utilities
from resumix.utils.ocr_utils import OCRUtils
from resumix.utils.llm_client import LLMClient, LLMWrapper
from resumix.utils.session_utils import SessionUtils

import concurrent.futures
from resumix.utils.i18n import LANGUAGES
from resumix.job_parser.resume_rewriter import ResumeRewriter
from resumix.job_parser.jd_parser import JDParser
from resumix.utils.logger import logger
from resumix.components.score_page import ScorePage


# Config setup
CONFIG = Config().config
CURRENT_DIR = Path(__file__).resolve().parent
ASSET_DIR = CURRENT_DIR / "assets" / "logo.png"


T = LANGUAGES[st.session_state.lang]

# card(
#     title=T["title"],
#     text="test",
#     image="assets/logo.png",
#     url="www.resumix.com",
# )


llm_model = LLMClient()
agent = initialize_agent(
    tools=tool_list,
    llm=LLMWrapper(client=llm_model),
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5,
)

RESUME_REWRITER = ResumeRewriter(llm_model)

# Page configuration
st.set_page_config(
    page_title="RESUMIX",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Header section
header_col1, header_col2 = st.columns([1, 3])
with header_col1:
    st.image(ASSET_DIR, width=60)
with header_col2:
    st.title(T["title"])

# Main navigation
tab_names = T["tabs"]
selected_tab = option_menu(
    menu_title=None,
    options=tab_names,
    icons=["file-text", "pencil", "robot", "bar-chart", "file-earmark-break"],
    orientation="horizontal",
)

# Sidebar components
with st.sidebar:
    # Resume upload
    with st.expander(T["upload_resume"], expanded=True):
        uploaded_file = st.file_uploader(T["upload_resume_title"], type=["pdf"])
        SessionUtils.upload_resume_file(uploaded_file)

    # Job description
    with st.expander(T["job_description"], expanded=True):
        jd_url = st.text_input(
            T["job_description_title"],
            placeholder="https://example.com/job-description",
            key="jd_url",
        )

    # Authentication
    with st.expander(T["user_login"], expanded=False):
        if not st.session_state.get("authenticated"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button(T["login_button"]):
                if username == "admin" and password == "123456":
                    st.session_state.authenticated = True
                    st.success(T["login_success"])
        else:
            st.success(T["logged_in"])
            if st.button(T["logout"]):
                st.session_state.authenticated = False

    # Language selection
    with st.expander(T["language"], expanded=False):
        selected_lang = st.selectbox(
            "Global",
            ["en", "zh"],
            index=["en", "zh"].index(st.session_state.lang),
        )
        if selected_lang != st.session_state.lang:
            st.session_state.lang = selected_lang
            st.rerun()


def prefetch_resume_sections():
    try:
        st.session_state.resume_sections = SessionUtils.get_resume_sections()
        logger.info("[后台] Resume section 提取完成")
    except Exception as e:
        logger.warning(f"[后台] 提取 resume_sections 失败: {e}")


def prefetch_jd_sections():
    try:
        st.session_state.jd_sections = SessionUtils.get_jd_sections()
        logger.info("[后台] JD section 提取完成")
    except Exception as e:
        logger.warning(f"[后台] 提取 jd_sections 失败: {e}")


if uploaded_file:
    # Initialize session data if not exists
    if "resume_text" not in st.session_state:
        st.session_state.resume_text = SessionUtils.get_resume_text()

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)

    # 后台启动 section 提取（非阻塞）
    if "resume_sections" not in st.session_state:
        executor.submit(prefetch_resume_sections)

    # if "jd_sections" not in st.session_state:
    #     executor.submit(prefetch_jd_sections)

    text = st.session_state.resume_text
    STRUCTED_SECTIONS = SessionUtils.get_resume_sections()
    jd_content = SessionUtils.get_job_description_content()

    # Tab routing with card components
    with st.container():
        if selected_tab == tab_names[0]:  # Analysis
            pass
            analysis_card(text=text, show_scores=True, show_analysis=True)

        elif selected_tab == tab_names[1]:  # Polish
            pass
            polish_card(text=text, llm_model=llm_model, show_scores=False)

        elif selected_tab == tab_names[2]:  # Agent
            pass
            agent_card(text=text, jd_content=jd_content, agent=agent, show_scores=True)

        elif selected_tab == tab_names[3]:  # Score
            ScorePage().render()

        elif selected_tab == tab_names[4]:  # Compare
            compare_resume_sections(
                sections=STRUCTED_SECTIONS,
                jd_content=jd_content,
                rewriter=RESUME_REWRITER,
                use_card_template=True,
            )
else:
    st.info(T["please_upload"])
