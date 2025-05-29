import streamlit as st  # type: ignore
from pathlib import Path
from streamlit_option_menu import option_menu  # type: ignore

# Set up paths for logo
logo_path_svg = Path("src/resources/logo/remorph.svg")
logo_path_png = Path("src/resources/logo/remorph.png")
st.set_page_config(page_title="Reconcile", page_icon=logo_path_png, layout="wide")


def load_svg_inline(svg_path):
    with open(svg_path, "r") as file:
        return file.read()


def render_homepage():
    logo_svg_content = load_svg_inline(logo_path_svg)

    with st.sidebar:
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; margin-bottom: 20px;">
                <div style="width: 60px; height: 60px; display: flex; justify-content: center; align-items: center;">
                    {logo_svg_content}
                </div>
                <h1 style="margin: 0 0 0 15px; font-size: 2rem; color: #FFFFFF; margin-top: 5px;">Reconcile</h1>
            </div>
            """,
            unsafe_allow_html=True,
        )

        menu_options = {
            "Home": None,
            "Recon Executor": "recon_executor",
            "Secret Manager": "secret_manager",
            "Config Manager": "config_manager",
            "Dashboard": "dashboard",
            "About": "about",
        }

        query_params = st.query_params.get("page", None)

        default_index = list(menu_options.values()).index(query_params) if query_params in menu_options.values() else 0
        selected_option = option_menu(
            menu_title=None,
            options=list(menu_options.keys()),
            icons=["house", "play-circle", "key", "wrench", "bar-chart", "info-circle"],
            menu_icon="cast",
            default_index=default_index,
            styles={
                "container": {"padding": "0", "background-color": "#f8f9fa"},
                "icon": {"color": "blue", "font-size": "20px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "color": "black",
                    "--hover-color": "#eeeeee",
                },
                "nav-link-selected": {"background-color": "#4CAF50", "color": "white"},
            },
        )

    # Update the URL **only if the selected page has changed** (avoiding unnecessary rerun)
    new_page = menu_options[selected_option]
    if new_page != query_params:
        if new_page is None:
            st.query_params.clear()
        else:
            st.query_params["page"] = new_page
        st.rerun()

    return selected_option
