import numpy as np
import matplotlib.pyplot as plt
import threading
from copy import deepcopy
from tqdm import tqdm
from sorting import *

def generate_plot():
    algorithms = {
        "Bubble Sort": bubble_sort,
        "Insertion Sort": insertion_sort,
        "Selection Sort": selection_sort,
        "Merge Sort": merge_sort,
        "Heap Sort": heap_sort,
        "Quick Sort": quick_sort,
        "Quick Sort (Median of 3)": quick_sort_median3,
    }

    complexities = {
        "Bubble Sort": "O(n²)",
        "Insertion Sort": "O(n²)",
        "Selection Sort": "O(n²)",
        "Merge Sort": "O(n log n)",
        "Heap Sort": "O(n log n)",
        "Quick Sort": "O(n log n)",
        "Quick Sort (Median of 3)": "O(n log n)",
    }

    sizes = np.logspace(1, 6, num=10, dtype=int)

    def evaluate_case(case_name, generator_func, filename):
        results = {name: [] for name in algorithms}
        total_tasks = len(algorithms) * len(sizes)
        progress = tqdm(total=total_tasks, desc=f"Evaluating {case_name}", ncols=100)
        lock = threading.Lock()

        def evaluate_algorithm(name, func):
            for n in sizes:
                if "O(n²)" in complexities[name] and n > 10000:
                    results[name].append(None)
                else:
                    try:
                        arr = generator_func(n)
                        _, loops, _ = func(deepcopy(arr), speed=0, visualization=False)
                        results[name].append(loops)
                    except Exception:
                        results[name].append(None)
                with lock:
                    progress.update(1)

        threads = []
        for name, func in algorithms.items():
            t = threading.Thread(target=evaluate_algorithm, args=(name, func))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
        progress.close()

        # Plot results
        plt.figure(figsize=(28, 16), dpi=300)
        for name in algorithms:
            y_vals = results[name]
            plt.plot(sizes, y_vals, label=f"{name} ({complexities[name]})", linewidth=2.5)

        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel("Input Size (N)", fontsize=28)
        plt.ylabel("Loop Count", fontsize=28)
        plt.title(f"{case_name} Case: Runtime Complexity vs Input Size", fontsize=24)
        plt.legend(fontsize=20)
        plt.grid(True, which="both", linestyle="--", linewidth=2.5)
        plt.xticks(fontsize=24)
        plt.yticks(fontsize=24)
        plt.tight_layout()
        plt.savefig(filename)

    # Define data generators
    def average_case(n):
        return np.random.randint(0, 1000000, size=n).tolist()

    def best_case(n):
        return list(range(n))

    def worst_case(n):
        return list(range(n, 0, -1))

    # Run all three plots
    evaluate_case("Average", average_case, "complexity_average.png")
    evaluate_case("Best", best_case, "complexity_best.png")
    evaluate_case("Worst", worst_case, "complexity_worst.png")

# ------------------ Run the Plot ------------------

if __name__ == "__main__":
    generate_plot()
