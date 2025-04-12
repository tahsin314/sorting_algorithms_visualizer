import time
import random
import uuid
import threading
import queue
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

from sorting import (
    bubble_sort,
    insertion_sort,
    selection_sort,
    merge_sort,
    heap_sort,
    quick_sort,
    quick_sort_median3,
)

from utils import draw_altair_bars, visualize_sorting

# --- CONFIG ---
draw_bar_function = draw_altair_bars
BASE_SPEED = 1e7
RANGE = 1000

# --- UI Setup ---
st.set_page_config(layout="wide", page_title="Sorting Visualizer")
st.title("Sorting Visualizer")
st.markdown("DAA Project: Comparison Among Sorting Algorithms")
st.markdown("")

# --- Initialize Session State ---
if 'arr' not in st.session_state:
    st.session_state.arr = None
if 'original_data' not in st.session_state:
    st.session_state.original_data = None
if 'speed' not in st.session_state:
    st.session_state.speed = BASE_SPEED  # Initial value, will be updated by slider

# --- Algorithm Options ---
ALGORITHMS = [
    "Bubble Sort",
    "Insertion Sort",
    "Selection Sort",
    "Merge Sort",
    "Heap Sort",
    "Quick Sort",
    "Quick Sort (Median of 3)"
]

# --- Controls ---
N_COL, T_COL = st.columns([3, 2], gap="large")
with N_COL:
    N = st.slider("Number of Elements: ", 10, 1000, 50, 5)
with T_COL:
    ALGO = st.selectbox("Sorting Algorithm", ALGORITHMS)

A_COL, T_COL = st.columns([2.5, 2], gap="large")
with A_COL:
    st.markdown("### Data Source")
    data_option = st.selectbox("Choose Data Source:", [
        "User Input",
        "Random Numbers",
        "Random Ascending Numbers",
        "Random Descending Numbers"
    ])
    
    # Generate or update arr only if needed
    if data_option == "User Input":
        uploaded_file = st.file_uploader("Upload a text file with numbers (one per line)", type=["txt"])
        if uploaded_file is not None:
            try:
                # Read numbers from file
                numbers = uploaded_file.read().decode("utf-8").strip().split("\n")
                new_arr = [int(num) for num in numbers if num.strip()]
                # Update session state only if new file is uploaded
                st.session_state.arr = new_arr
                st.session_state.original_data = "\n".join(str(x) for x in new_arr)
            except ValueError:
                st.error("File must contain valid integers, one per line.")
                st.session_state.arr = None
                st.session_state.original_data = None
    elif st.session_state.arr is None or st.session_state.get('last_data_option') != data_option:
        # Generate new data for random options only if no data exists or option changed
        if data_option == "Random Numbers":
            st.session_state.arr = [random.randint(1, RANGE) for _ in range(N)]
        elif data_option == "Random Ascending Numbers":
            st.session_state.arr = sorted([random.randint(1, RANGE) for _ in range(N)])
        elif data_option == "Random Descending Numbers":
            st.session_state.arr = sorted([random.randint(1, RANGE) for _ in range(N)], reverse=True)
        st.session_state.original_data = "\n".join(str(x) for x in st.session_state.arr)
        st.session_state.last_data_option = data_option

    # Reset button
    if st.button("Reset Data"):
        st.session_state.arr = None
        st.session_state.original_data = None
        st.session_state.pop('last_data_option', None)

    animate_option = st.selectbox("Enable Sorting Animation", ["Yes", "No"])
    animate = animate_option == "Yes"

with T_COL:
    slider_value = st.slider("Speed: ", 1, 10, 5)
    exponent = -7.0 + (slider_value - 1) * 6 / 9
    st.session_state.speed = BASE_SPEED * (10 ** exponent)

# --- Initial plot ---
plot_spot = st.empty()
if st.session_state.arr is not None:
    draw_bar_function(st.session_state.arr, plot_spot)

# --- Single sort execution ---
if st.session_state.arr is not None and st.button("SORT!", use_container_width=True):
    sort_func_map = {
        "Bubble Sort": bubble_sort,
        "Insertion Sort": insertion_sort,
        "Selection Sort": selection_sort,
        "Merge Sort": merge_sort,
        "Heap Sort": heap_sort,
        "Quick Sort": quick_sort,
        "Quick Sort (Median of 3)": quick_sort_median3,
    }

    sort_func = sort_func_map[ALGO]
    arr, time_c, space_c = sort_func(
        st.session_state.arr,
        st.session_state.speed,
        visualization=animate,
        plot_spot=plot_spot,
        draw_func=draw_bar_function,
        beep_func=None,
    )

    st.session_state.arr = arr  # Update stored array
    draw_bar_function(arr, plot_spot)
    # Original Data download
    st.download_button(
        label="Download Original Data",
        data=st.session_state.original_data,
        file_name="original_data.txt",
        mime="text/plain"
    )
    # Update sorted data for download
    sorted_data = "\n".join(str(x) for x in arr)
    st.download_button(
        label="Download Sorted Data",
        data=sorted_data,
        file_name="sorted_data.txt",
        mime="text/plain",
        key="sorted_download_updated"
    )
    time.sleep(0.5)
    st.markdown("### Complexity Analysis")
    st.markdown(f"**Loop Count (Approximate Time Complexity):** `{time_c}`")
    st.markdown(f"**Temporary Space Used (Space Complexity):** `{space_c}`")

# --- Sort using all algorithms ---
if st.session_state.arr is not None and st.button("SORT USING ALL ALGORITHMS", use_container_width=True):
    algorithms = {
        "Bubble Sort": bubble_sort,
        "Insertion Sort": insertion_sort,
        "Selection Sort": selection_sort,
        "Merge Sort": merge_sort,
        "Heap Sort": heap_sort,
        "Quick Sort": quick_sort,
        "Quick Sort (Median of 3)": quick_sort_median3,
    }

    algo_names = list(algorithms.keys())
    # Use the same input array (user-provided or random based on data_option)
    arr_for_visual = st.session_state.arr.copy()
    if len(arr_for_visual) > 500:
        arr_for_visual = arr_for_visual[:500]

    if animate:
        st.markdown("### 🔄 Visual Comparison (Animated)")

        all_placeholders = []
        plot_queues = []
        last_drawn = [None] * len(algorithms)

        for row in range(4):
            cols = st.columns(2)
            for col in cols:
                chart_area = col.empty()
                all_placeholders.append({
                    "title": col.markdown(""),
                    "chart": chart_area
                })
                plot_queues.append(queue.Queue())

        def run_sort_thread(func, q, arr_copy, speed_value):
            def custom_draw(arr_frame, plot_spot, hi):
                q.put((arr_frame.copy(), hi))

            func(
                arr_copy,
                speed_value,  # Pass speed explicitly
                visualization=True,
                plot_spot=q,
                draw_func=custom_draw,
                beep_func=None,
            )
            q.put("__DONE__")

        threads = []
        current_speed = st.session_state.speed  # Snapshot current speed
        for i, (name, func) in enumerate(algorithms.items()):
            all_placeholders[i]["title"].markdown(f"### {name}")
            arr_clone = arr_for_visual.copy()
            t = threading.Thread(
                target=run_sort_thread,
                args=(func, plot_queues[i], arr_clone, current_speed)
            )
            threads.append(t)
            t.start()

        completed = [False] * len(algorithms)
        while not all(completed):
            for i, q in enumerate(plot_queues):
                try:
                    msg = q.get_nowait()
                    if msg == "__DONE__":
                        completed[i] = True
                        continue
                    arr_frame, hi = msg
                    if last_drawn[i] != arr_frame:
                        draw_bar_function(arr_frame, all_placeholders[i]["chart"], hi)
                        last_drawn[i] = arr_frame
                except queue.Empty:
                    continue
            time.sleep(0.015)

        for t in threads:
            t.join()

    # --- Complexity Comparison ---
    st.markdown("## 📊 Complexity Comparison")

    results = {}
    for name, func in algorithms.items():
        test_arr = st.session_state.arr.copy()  # Use the same input data
        sorted_arr, loop_count, space_count = func(
            test_arr,
            speed=1e12,
            visualization=False,
            plot_spot=None,
            draw_func=None,
            beep_func=None,
        )
        results[name] = {
            "time": loop_count,
            "space": space_count,
        }

    time_vals = [results[algo]["time"] for algo in algo_names]
    space_vals = [results[algo]["space"] for algo in algo_names]

    def get_colors(values):
        min_val, max_val = min(values), max(values)
        return [
            'green' if v == min_val else 'red' if v == max_val else 'lightgray'
            for v in values
        ]


    time_colors = get_colors(time_vals)
    space_colors = get_colors(space_vals)

    fig_time = go.Figure(
        data=[go.Bar(
            x=algo_names, y=time_vals, marker_color=time_colors,
            text=time_vals, textposition="outside"
        )],
        layout=go.Layout(title="Loop Count (Time Complexity)", height=400)
    )
    st.plotly_chart(fig_time, use_container_width=True)

    fig_space = go.Figure(
        data=[go.Bar(
            x=algo_names, y=space_vals, marker_color=space_colors,
            text=space_vals, textposition="outside"
        )],
        layout=go.Layout(title="Temporary Space Used (Space Complexity)", height=400)
    )
    st.plotly_chart(fig_space, use_container_width=True)