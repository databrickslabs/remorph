from src.resources.web_components.homepage import render_homepage
from src.services.spark_service import initialize_app

selected_option = render_homepage()
initialize_app()

# Routing
if selected_option == "Home":
    from src.routes.home import main as page_main
elif selected_option == "Recon Executor":
    from src.routes.recon_executor import main as page_main
elif selected_option == "Secret Manager":
    from src.routes.secret_manager import main as page_main
elif selected_option == "Config Manager":
    from src.routes.config_manager import main as page_main
elif selected_option == "Dashboard":
    from src.routes.dashboard import main as page_main
elif selected_option == "About":
    from src.routes.about import main as page_main

page_main()
