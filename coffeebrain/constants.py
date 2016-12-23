DATASETS = ['training', 'testing']

SIDES = ['left', 'right']

UNKNOWN = 0
EMPTY = 1
LITTLE = 2
PLENTY = 3
FULL = 4

LABELS = {
    'unknown': 0,
    'empty': 1,
    'little': 2,
    'plenty': 3,
    'full': 4
}

REVERSE_LABELS = {v: k for k, v in LABELS.items()}
