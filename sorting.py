from utils import visualize_sorting

def bubble_sort(arr, speed=0.1, visualization=False, plot_spot=None, draw_func=None, beep_func=None):
    loop_count = 0
    n = len(arr)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            loop_count += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                if visualization:
                    visualize_sorting(arr, j, speed, plot_spot, draw_func, beep_func)
    return arr, loop_count, 0


def insertion_sort(arr, speed=0.1, visualization=False, plot_spot=None, draw_func=None, beep_func=None):
    loop_count = 0
    for i in range(1, len(arr)):
        while i > 0 and arr[i - 1] > arr[i]:
            loop_count += 1
            arr[i - 1], arr[i] = arr[i], arr[i - 1]
            i -= 1
            if visualization:
                visualize_sorting(arr, i, speed, plot_spot, draw_func, beep_func)
    return arr, loop_count, 0


def selection_sort(arr, speed=0.1, visualization=False, plot_spot=None, draw_func=None, beep_func=None):
    loop_count = 0
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            loop_count += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        if visualization:
            visualize_sorting(arr, i, speed, plot_spot, draw_func, beep_func)
    return arr, loop_count, 0


def heapify(arr, n, i, speed, visualization, plot_spot, draw_func, beep_func, loop_info):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    loop_info['count'] += 1

    if l < n and arr[l] > arr[largest]:
        largest = l
    if r < n and arr[r] > arr[largest]:
        largest = r

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        if visualization:
            visualize_sorting(arr, largest, speed, plot_spot, draw_func, beep_func)
        heapify(arr, n, largest, speed, visualization, plot_spot, draw_func, beep_func, loop_info)


def heap_sort(arr, speed=0.1, visualization=False, plot_spot=None, draw_func=None, beep_func=None):
    n = len(arr)
    loop_info = {'count': 0}
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, speed, visualization, plot_spot, draw_func, beep_func, loop_info)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        if visualization:
            visualize_sorting(arr, i, speed, plot_spot, draw_func, beep_func)
        heapify(arr, i, 0, speed, visualization, plot_spot, draw_func, beep_func, loop_info)
    return arr, loop_info['count'], 0


def quick_sort(arr, speed=0.1, visualization=False, plot_spot=None, draw_func=None, beep_func=None):
    return _generic_quick_sort(
        arr,
        pivot_strategy="last",
        speed=speed,
        visualization=visualization,
        plot_spot=plot_spot,
        draw_func=draw_func,
        beep_func=beep_func,
    )


def quick_sort_median3(arr, speed=0.1, visualization=False, plot_spot=None, draw_func=None, beep_func=None):
    return _generic_quick_sort(
        arr,
        pivot_strategy="median3",
        speed=speed,
        visualization=visualization,
        plot_spot=plot_spot,
        draw_func=draw_func,
        beep_func=beep_func,
    )


def _generic_quick_sort(arr, pivot_strategy="last", speed=0.1, visualization=False, plot_spot=None, draw_func=None, beep_func=None):
    loop_count = {'count': 0}

    def median_of_three_indices(array, low, high):
        mid = (low + high) // 2
        trio = [(array[low], low), (array[mid], mid), (array[high], high)]
        _, idx = sorted(trio)[1]
        return idx

    def partition(array, low, high):
        # Select pivot index based on strategy
        if pivot_strategy == "median3":
            pivot_index = median_of_three_indices(array, low, high)
            array[pivot_index], array[high] = array[high], array[pivot_index]
        # Default is "last" (i.e., array[high])

        pivot = array[high]
        i = low - 1
        for j in range(low, high):
            loop_count['count'] += 1
            if array[j] <= pivot:
                i += 1
                array[i], array[j] = array[j], array[i]
                if visualization:
                    visualize_sorting(array, j, speed, plot_spot, draw_func, beep_func)
        array[i + 1], array[high] = array[high], array[i + 1]
        if visualization:
            visualize_sorting(array, i + 1, speed, plot_spot, draw_func, beep_func)
        return i + 1

    def quicksort(array, low, high):
        if low < high:
            pi = partition(array, low, high)
            quicksort(array, low, pi - 1)
            quicksort(array, pi + 1, high)

    quicksort(arr, 0, len(arr) - 1)
    return arr, loop_count['count'], 0


def merge_sort(arr, speed=0.1, visualization=False, plot_spot=None, draw_func=None, beep_func=None):
    loop_count = {'count': 0}
    space_count = {'count': 0}

    def merge(array, left, mid, right):
        L = array[left:mid + 1]
        R = array[mid + 1:right + 1]
        space_count['count'] += len(L) + len(R)
        i = j = 0
        k = left

        while i < len(L) and j < len(R):
            loop_count['count'] += 1
            if L[i] <= R[j]:
                array[k] = L[i]
                i += 1
            else:
                array[k] = R[j]
                j += 1
            if visualization:
                visualize_sorting(array, k, speed, plot_spot, draw_func, beep_func)
            k += 1

        while i < len(L):
            loop_count['count'] += 1
            array[k] = L[i]
            i += 1
            if visualization:
                visualize_sorting(array, k, speed, plot_spot, draw_func, beep_func)
            k += 1

        while j < len(R):
            loop_count['count'] += 1
            array[k] = R[j]
            j += 1
            if visualization:
                visualize_sorting(array, k, speed, plot_spot, draw_func, beep_func)
            k += 1

    def mergesort(array, left, right):
        if left < right:
            mid = (left + right) // 2
            mergesort(array, left, mid)
            mergesort(array, mid + 1, right)
            merge(array, left, mid, right)

    mergesort(arr, 0, len(arr) - 1)
    return arr, loop_count['count'], space_count['count']
