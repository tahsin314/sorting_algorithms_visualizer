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
BASE_SPEED = 1e-7
RANGE = 1000

# --- UI Setup ---
st.set_page_config(layout="wide", page_title="Sorting Visualizer")
st.title("Sorting Visualizer")
st.markdown("DAA Project: Comparison Among Sorting Algorithms")
st.markdown("")

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
    st.markdown("### Number Generator")
    order_option = st.selectbox("Choose Data Distribution:", ["Randomize", "Ascending Order", "Descending Order"])
    if order_option == "Randomize":
        arr = [random.randint(1, RANGE) for _ in range(N)]
    elif order_option == "Ascending Order":
        arr = list(range(1, N + 1))
    elif order_option == "Descending Order":
        arr = list(range(N, 0, -1))

    animate_option = st.selectbox("Enable Sorting Animation", ["Yes", "No"])
    animate = animate_option == "Yes"

with T_COL:
    SPEED = BASE_SPEED / st.slider("Speed: ", 1, 10, 1)

# --- Initial plot ---
plot_spot = st.empty()
draw_bar_function(arr, plot_spot)

# --- Single sort execution ---
if st.button("SORT!", use_container_width=True):
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
        arr,
        SPEED,
        visualization=animate,
        plot_spot=plot_spot,
        draw_func=draw_bar_function,
        beep_func=None,
    )

    draw_bar_function(arr, plot_spot)
    time.sleep(0.5)
    st.markdown("### Complexity Analysis")
    st.markdown(f"**Loop Count (Approximate Time Complexity):** `{time_c}`")
    st.markdown(f"**Temporary Space Used (Space Complexity):** `{space_c}`")

# --- Sort using all algorithms ---
if st.button("SORT USING ALL ALGORITHMS", use_container_width=True):
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
    arr_for_visual = arr.copy()
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

        def run_sort_thread(func, q, arr_copy):
            def custom_draw(arr_frame, plot_spot, hi):
                q.put((arr_frame.copy(), hi))

            func(
                arr_copy,
                speed=SPEED,
                visualization=True,
                plot_spot=q,
                draw_func=custom_draw,
                beep_func=None,
            )
            q.put("__DONE__")

        threads = []
        for i, (name, func) in enumerate(algorithms.items()):
            all_placeholders[i]["title"].markdown(f"### {name}")
            arr_clone = arr_for_visual.copy()
            t = threading.Thread(
                target=run_sort_thread,
                args=(func, plot_queues[i], arr_clone)
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
        test_arr = arr.copy()
        sorted_arr, loop_count, space_count = func(
            test_arr,
            speed=0,
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
