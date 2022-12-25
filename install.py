import launch

if not launch.is_installed("shortcodes"):
    launch.run_pip("install shortcodes", "requirement for using Gekiryuu86/sdwebui-mvar-plot")