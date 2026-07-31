import numpy as np
import pandas as pd
from enum import Enum
from typing import List
from sklearn.preprocessing import OneHotEncoder


class TargetType(Enum):
    """ The supported target types. """

    RESULT = 'result'
    OVER_UNDER = 'over-under'
    OVER_UNDER_15 = 'over-under-1.5'
    OVER_UNDER_35 = 'over-under-3.5'
    BTTS = 'btts'


BINARY_TARGETS = {
    TargetType.OVER_UNDER,
    TargetType.OVER_UNDER_15,
    TargetType.OVER_UNDER_35,
    TargetType.BTTS,
}


def is_binary_target(target_type: TargetType) -> bool:
    return target_type in BINARY_TARGETS


def class_names(target_type: TargetType) -> List[str]:
    if target_type == TargetType.RESULT:
        return ['H', 'D', 'A']
    if target_type == TargetType.OVER_UNDER:
        return ['U', 'O']
    if target_type == TargetType.OVER_UNDER_15:
        return ['U1.5', 'O1.5']
    if target_type == TargetType.OVER_UNDER_35:
        return ['U3.5', 'O3.5']
    if target_type == TargetType.BTTS:
        return ['No', 'Yes']
    raise TypeError(f'Undefined target type: "{target_type}"')


def construct_targets(df: pd.DataFrame, target_type: TargetType) -> np.ndarray:
    """ Constructs the dataset targets based on the selected classification task """

    if target_type == TargetType.RESULT:
        y = df['Result'].replace({'H': 0, 'D': 1, 'A': 2}).to_numpy(dtype=np.int32)
    elif target_type == TargetType.OVER_UNDER:
        y = ((df['HG'] + df['AG']).ge(2.5)).astype(np.int32).to_numpy()
    elif target_type == TargetType.OVER_UNDER_15:
        y = ((df['HG'] + df['AG']).ge(1.5)).astype(np.int32).to_numpy()
    elif target_type == TargetType.OVER_UNDER_35:
        y = ((df['HG'] + df['AG']).ge(3.5)).astype(np.int32).to_numpy()
    elif target_type == TargetType.BTTS:
        y = ((df['HG'] > 0) & (df['AG'] > 0)).astype(np.int32).to_numpy()
    else:
        raise TypeError(f'Undefined target type: "{target_type.name}"')

    return y


def one_hot_encode(y: np.ndarray, target_type: TargetType) -> np.ndarray:
    """ One-Hot encodes the provided targets. To ensure consistency,
        the target categories are fixed and depend on the target type.
    """

    if target_type == TargetType.RESULT:
        y_encoded = OneHotEncoder(categories=[[0, 1, 2]], sparse_output=False).fit_transform(y.reshape(-1, 1))
    elif is_binary_target(target_type):
        raise TypeError(f'{target_type.value} targets do not support one-hot encoding (binary task).')
    else:
        raise TypeError(f'Not supported target type: "{type(target_type)}"')

    return y_encoded
