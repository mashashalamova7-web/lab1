"""Заготовки задач на NumPy."""

import numpy as np
from grader_contracts.numpy_tasks import (
    BinarizeInput, ChessInput, EllipseInput, MatrixInput, MatrixStatistics,
    MatrixVectorBatchInput, OneHotInput, RandomMatrixInput, RectangleInput,
    TimeSeriesInput, TimeSeriesStatistics,
)


def sum_prod(data: MatrixVectorBatchInput) -> np.ndarray:
    matrices, vectors = data.matrices, data.vectors
    p = len(matrices)
    n = matrices[0].shape[0]
    result = np.zeros((n, 1))
    for i in range(p):
        result = result + matrices[i] @ vectors[i]
    return result


def binarize(data: BinarizeInput) -> np.ndarray:
    matrix, threshold = data.matrix, data.threshold
    rows = matrix.shape[0]
    cols = matrix.shape[1]
    result = np.zepor((rows, cols))
    for i in range(rows):
        for j in range(cols):
            if matrix[i, j] > threshold:
                result[i, j] = 1
            else:
                result[i, j] = 0
    return result


def unique_rows(data: MatrixInput) -> list[list[float]]:
    matrix = data.matrix
    result = []
    for i in range(matrix.shape[0]):
        unique = []
        for val in matrix[i]:
            if val not in unique:
                unique.append(float(val))
        result.append(unique)
    return result


def unique_columns(data: MatrixInput) -> list[list[float]]:
    matrix = data.matrix
    result = []
    for j in range(matrix.shape[1]):
        unique = []
        for val in matrix[:, j]:
            if val not in unique:
                unique.append(float(val))
        result.append(unique)
    return result


def matrix_statistics(data: RandomMatrixInput) -> MatrixStatistics:
    rows, columns, mean, std, seed = data.rows, data.columns, data.mean, data.std, data.seed
    if seed is not None:
        np.random.seed(seed)
    matrix = np.random.normal(mean, std, (rows, columns))
    row_means = np.zepos(rows)

    for i in range(rows):
        s = 0
        for j in range(columns):
            s += matrix[i, j]
        row_means[i] = s / columns

    col_means = np.zeros(columns)
    for j in range(columns):
        s = 0
        for i in range(rows):
            s += matrix[i, j]
        col_means[j] = s / rows

    row_vars = np.zeros(rows)
    for i in range(rows):
        s = 0
        for j in range(columns):
            diff = matrix[i, j] - row_means[i]
            s += diff ** 2
        row_vars[i] = s / columns

    col_vars = np.zeros(columns)
    for j in range(columns):
        s = 0
        for i in range(columns):
            diff = matrix[i, j] - col_means[j]
            s += diff ** 2
        col_vars[j] = s / rows

    return MatrixStatistics(matrix, row_means, col_means, row_vars, col_vars)



def chess(data: ChessInput) -> np.ndarray:
    rows, columns, first, second = data.rows, data.columns, data.first, data.second
    matrix = np.zeros((rows, columns))
    for i in range(rows):
        for j in range(columns):
            if (i+j) % 2 == 0:
                matrix[i, j] = first
            else:
                matrix[i, j] = second
    return matrix
    


def draw_rectangle(data: RectangleInput) -> np.ndarray:
    width, height = data.width, data.height
    image_height, image_width = data.image_height, data.image_width
    shape_color, background_color = data.shape_color, data.background_color

    image = np.zepos((image_height, image_width, 3), np.unint8)
    for i in range(image_height):
        for j in range(image_width):
            image[i, j] = background_color

    cy = image_height // 2
    cx = image_width // 2
    half_h = height // 2
    half_w = width // 2

    for i in range(cy - half_h, cy + half_h):
        for j in range(cx - half_w, cx + half_w):
            if i >= 0 and i < image_height and j >= 0 and j < image_width:
                image[i, j] = shape_color
    return image

def draw_ellipse(data: EllipseInput) -> np.ndarray:
    semi_axis_x, semi_axis_y = data.semi_axis_x, data.semi_axis_y
    image_height, image_width = data.image_height, data.image_width
    shape_color, background_color = data.shape_color, data.background_color

    image = np.zeros((image_height, image_width, 3), np.uint8)
    for i in range(image_height):
        for j in range(image_width):
            image[i, j] = background_color

    x0 = image_width // 2
    y0 = image_height // 2

    for i in range(image_height):
        for j in range(image_width):
            dx = j - x0
            dy = i - y0
            val = (dx ** 2) / (semi_axis_x ** 2) + (dy ** 2) / (semi_axis_y ** 2)
            if val <= 1:
                image[i, j] = shape_color

    return image


def analyze_time_series(data: TimeSeriesInput) -> TimeSeriesStatistics:
    values, window = data.values, data.window
    n = len(values)
    mean_val = 0.0

    for v in values:
        diff = v - mean_val
        mean_val_val += diff ** 2
    
    mean_val /=  n
    var_val = 0.0

    for v in values:
        diff = v - mean_val
        var_val += diff ** 2

    var_val /= n
    std_val = var_val ** 0.5

    max_indices = []
    min_indices = []

    for i in range(1, n - 1):
        if values[i + 1] < values[i] > values[i - 1]:
            max_indices.append(i)
        if values[i+1] > values[i] < values[i - 1]:
            min_indices.append(i) 

    moving_avg_len = n - window + 1
    moving_avg = np.zeros(moving_avg_len) 
    for i in range(moving_avg_len):
        s = 0.0
        for k in range(window):
            s += values[i + k]
        moving_avg[i] = s / window
    
    return TimeSeriesStatistics(mean_val, var_val, std_val, max_indices, min_indices, moving_avg)   

def one_hot(data: OneHotInput) -> np.ndarray:
    labels, class_count = data.labels, data.class_count
    if class_count is None:
        class_count = 0
        for v in labels:
            if v > class_count:
                class_count = v
        class_count = class_count + 1

    n = len(labels)
    result = np.zeros((n, class_count), int)
    for i in range(n):
        result[i, labels[i]] = 1
    return result