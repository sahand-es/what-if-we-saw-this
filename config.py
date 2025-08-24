DETECTION = {
    'threshold': 150,
    'min_area': 10,
    'max_area': 100000000,
    'max_subjects': 30,
}

TRACKING = {
    'max_subjects': 30,
    'smoothing': 0.7,
    'search_radius': 50,
}

OVERLAY = {
    'enabled': True,
    'ring_size': 10,
    'colors': [(0, 255, 0), (255, 0, 0), (0, 0, 255)],
}

WEBCAM = {
    'width': 640,
    'height': 480,
}
