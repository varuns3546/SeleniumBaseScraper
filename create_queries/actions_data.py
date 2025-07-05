navigations = [
    {"name": "open(url)", "parameter_count": 1},
    {"name": "go_back()", "parameter_count": 0},
    {"name": "go_forward()", "parameter_count": 0},
    {"name": "refresh()", "parameter_count": 0},
    {"name": "sleep(seconds)", "parameter_count": 1},
    {"name": "set_window_size(width, height)", "parameter_count": 2},
    {"name": "maximize_window()", "parameter_count": 0}
]

interactions = [
    {"name": "click(selector)", "parameter_count": 1},
    {"name": "double_click(selector)", "parameter_count": 1},
    {"name": "type(selector, text)", "parameter_count": 2},
    {"name": "clear(selector)", "parameter_count": 1},
    {"name": "get_text(selector)", "parameter_count": 1},
    {"name": "get_attribute(selector, attribute)", "parameter_count": 2},
    {"name": "is_element_visible(selector)", "parameter_count": 1},
    {"name": "is_element_present(selector)", "parameter_count": 1},
    {"name": "is_selected(selector)", "parameter_count": 1},
    {"name": "select_option_by_text(selector, text)", "parameter_count": 2},
    {"name": "select_option_by_value(selector, value)", "parameter_count": 2}
]

assertions = [
    {"name": "assert_element(selector)", "parameter_count": 1},
    {"name": "assert_text(text, selector)", "parameter_count": 2},
    {"name": "assert_element_visible(selector)", "parameter_count": 1},
    {"name": "assert_title(title)", "parameter_count": 1},
    {"name": "assert_url(url)", "parameter_count": 1}
]

waits = [
    {"name": "wait_for_element(selector)", "parameter_count": 1},
    {"name": "wait_for_text(text, selector)", "parameter_count": 2},
    {"name": "wait_for_ready_state_complete()", "parameter_count": 0},
    {"name": "wait_for_element_visible(selector)", "parameter_count": 1}
]

utilities = [
    {"name": "save_screenshot(name)", "parameter_count": 1},
    {"name": "highlight(selector)", "parameter_count": 1},
    {"name": "highlight_click(selector)", "parameter_count": 1},
    {"name": "execute_script(script)", "parameter_count": 1},
    {"name": "execute_async_script(script)", "parameter_count": 1},
    {"name": "download_file(url)", "parameter_count": 1},
    {"name": "choose_file(selector, file_path)", "parameter_count": 2},
    {"name": "find_element(selector)", "parameter_count": 1},
    {"name": "find_elements(selector)", "parameter_count": 1},
    {"name": "get_page_source()", "parameter_count": 0},
    {"name": "get_current_url()", "parameter_count": 0},
    {"name": "get_title()", "parameter_count": 0}
]

