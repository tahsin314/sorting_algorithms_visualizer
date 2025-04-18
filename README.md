# 🔢 Sorting Algorithms Visualizer

An interactive, real-time visualizer for sorting algorithms built with **Streamlit** and **Plotly** — designed to help you compare the time and space complexities of various sorting algorithms both visually and numerically. A demonstration video is available [here](https://www.youtube.com/watch?v=qTFP6tqR7oU)

---

## 🚀 Features

- 🎨 **Animated Sorting Visualization**
  - Watch your data get sorted in real time with colorful bar charts.
  - Toggle animation speed and step through how each algorithm works.

- 🧠 **Algorithms Included**
  - Bubble Sort
  - Insertion Sort
  - Selection Sort
  - Merge Sort
  - Heap Sort
  - Quick Sort
  - Quick Sort (Median of 3)

- 📂 **Flexible Input**
  - Choose from:
    - User-uploaded text files
    - Random numbers
    - Random ascending/descending arrays

- ⚡ **Compare All Algorithms Side-by-Side**
  - Run all algorithms simultaneously using **multithreading**
  - View bar chart comparisons for:
    - Loop counts (approx. time complexity)
    - Temporary space used (space complexity)

- 📥 **Download Support**
  - Export original or sorted arrays as `.txt` files.

---

## ⚠️ Known Bugs / Limitations

- 🐢 **Speed Limitation During Multi-Sort**
  - Changing the speed **during** "Sort Using All Algorithms" may reset progress or cause unexpected visual behavior.
  - Best to set the speed **before** starting.

- 💻 **Heavy Computation**
  - "Sort Using All Algorithms" is **CPU intensive**. Each sort runs in a separate thread, which may slow down performance, especially with large arrays.

---

## 🛠 Installation

### ✅ Prerequisites
- Python 3.8+
- pip
- Git (optional)

### 📦 Install via pip
```bash
git clone https://github.com/your-username/sorting-algorithms-visualizer.git
cd sorting-algorithms-visualizer
pip install -r requirements.txt
```
## 🚀 How to Run

- 💻 On your **local machine**, run:

  ```bash
  streamlit run app.py
  ```
Then click on the generated 🔗 local link shown in the terminal.

- 🌐 If you're using a remote server via SSH, Run:

  ```bash
  streamlit run app.py
  ```
Then, in a new terminal, run:

  ```bash
  ssh -R 80:localhost:8501 serveo.net
  ```
Click on the 🌍 public link generated by Serveo to access the app from any device.
