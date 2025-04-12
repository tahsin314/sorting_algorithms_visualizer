import pandas as pd
import altair as alt
import time

def visualize_sorting(arr, index, speed=0.1, plot_spot=None, draw_func=None, beep_func=None):
    if draw_func is not None:
        draw_func(arr, plot_spot, index)
    if beep_func is not None:
        beep_func()
    time.sleep(1/speed)

# --- Beep sound (optional async JS beep) ---
def play_beep_async(frequency=440, duration=0.05):
    def _beep():
        beep_script = f"""
        <script>
        const context = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = context.createOscillator();
        oscillator.type = "sine";
        oscillator.frequency.setValueAtTime({frequency}, context.currentTime);
        oscillator.connect(context.destination);
        oscillator.start();
        oscillator.stop(context.currentTime + {duration});
        </script>
        """
        st.components.v1.html(beep_script, height=0)
    threading.Thread(target=_beep).start()

# --- Plotting function ---
def draw_plotly_bars(arr, plot_spot, highlight_index=None):
    colors = ['red' if i == highlight_index else 'blue' for i in range(len(arr))]
    fig = go.Figure(
        data=[go.Bar(y=arr, marker_color=colors)],
        layout=go.Layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
    )
    fig.update_layout(xaxis=dict(showticklabels=False), yaxis=dict(showticklabels=False))
    unique_key = str(uuid.uuid4())
    plot_spot.plotly_chart(fig, use_container_width=True, key=unique_key)


def draw_streamlit_bars(arr, plot_spot, highlight_index=None):
    # Create DataFrame with color info
    df = pd.DataFrame({
        'value': arr,
        'highlight': ['highlight' if i == highlight_index else 'normal' for i in range(len(arr))]
    })

    # Streamlit’s bar_chart can’t directly color individual bars, but for speed it’s great
    plot_spot.bar_chart(df['value'])

def draw_altair_bars(arr, plot_spot, highlight_index=None):
    df = pd.DataFrame({
        'index': list(range(len(arr))),
        'value': arr,
        'color': ['Highlighted' if i == highlight_index else 'Normal' for i in range(len(arr))]
    })

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('index:O', axis=None),
        y=alt.Y('value:Q'),
        color=alt.Color('color:N',
            scale=alt.Scale(domain=['Highlighted', 'Normal'], range=['red', 'steelblue']),
            legend=None
        )
    ).properties(height=300)

    plot_spot.altair_chart(chart, use_container_width=True)
