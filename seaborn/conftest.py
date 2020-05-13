import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import pytest


@pytest.fixture(autouse=True)
def close_figs():
    yield
    plt.close("all")


@pytest.fixture(autouse=True)
def random_seed():
    seed = sum(map(ord, "seaborn random global"))
    np.random.seed(seed)


@pytest.fixture()
def rng():
    seed = sum(map(ord, "seaborn random object"))
    return np.random.RandomState(seed)


@pytest.fixture
def wide_df(rng):

    columns = list("abc")
    index = pd.Int64Index(np.arange(10, 50, 2), name="wide_index")
    values = rng.normal(size=(len(index), len(columns)))
    return pd.DataFrame(values, index=index, columns=columns)


@pytest.fixture
def wide_array(wide_df):

    # Requires panads >= 0.24
    # return wide_df.to_numpy()
    return np.asarray(wide_df)


@pytest.fixture
def flat_series(rng):

    index = pd.Int64Index(np.arange(10, 30), name="t")
    return pd.Series(rng.normal(size=20), index, name="s")


@pytest.fixture
def flat_array(flat_series):

    # Requires panads >= 0.24
    # return flat_series.to_numpy()
    return np.asarray(flat_series)


@pytest.fixture
def flat_list(flat_series):

    # Requires panads >= 0.24
    # return flat_series.to_list()
    return flat_series.tolist()


@pytest.fixture
def wide_list_of_series(rng):

    return [pd.Series(rng.normal(size=20), np.arange(20), name="a"),
            pd.Series(rng.normal(size=10), np.arange(5, 15), name="b")]


@pytest.fixture
def wide_list_of_arrays(wide_list_of_series):

    # Requires pandas >= 0.24
    # return [s.to_numpy() for s in wide_list_of_series]
    return [np.asarray(s) for s in wide_list_of_series]


@pytest.fixture
def wide_list_of_lists(wide_list_of_series):

    # Requires pandas >= 0.24
    # return [s.to_list() for s in wide_list_of_series]
    return [s.tolist() for s in wide_list_of_series]


@pytest.fixture
def wide_dict_of_series(wide_list_of_series):

    return {s.name: s for s in wide_list_of_series}


@pytest.fixture
def wide_dict_of_arrays(wide_list_of_series):

    # Requires pandas >= 0.24
    # return {s.name: s.to_numpy() for s in wide_list_of_series}
    return {s.name: np.asarray(s) for s in wide_list_of_series}


@pytest.fixture
def wide_dict_of_lists(wide_list_of_series):

    # Requires pandas >= 0.24
    # return {s.name: s.to_list() for s in wide_list_of_series}
    return {s.name: s.tolist() for s in wide_list_of_series}


@pytest.fixture
def long_df(rng):

    n = 100
    df = pd.DataFrame(dict(
        x=rng.uniform(0, 20, n).round().astype("int"),
        y=rng.normal(size=n),
        a=rng.choice(list("abc"), n),
        b=rng.choice(list("mnop"), n),
        c=rng.choice([0, 1], n),
        t=np.repeat(np.datetime64('2005-02-25'), n),
        s=rng.choice([2, 4, 8], n),
        f=rng.choice([0.2, 0.3], n),
    ))
    df["s_cat"] = df["s"].astype("category")
    return df


@pytest.fixture
def long_dict(long_df):

    return long_df.to_dict()


@pytest.fixture(params=[
    dict(x="x", y="y"),
    dict(x="t", y="y"),
    dict(x="x", y="y", hue="a"),
    dict(x="x", y="y", hue="a", style="a"),
    dict(x="x", y="y", hue="a", style="b"),
    dict(x="x", y="y", hue="a", size="b"),
])
def long_semantics(request):
    return request.param

@pytest.fixture
def repeated_df(rng):

    n = 100
    return pd.DataFrame(dict(
        x=np.tile(np.arange(n // 2), 2),
        y=rng.normal(size=n),
        a=rng.choice(list("abc"), n),
        u=np.repeat(np.arange(2), n // 2),
    ))


@pytest.fixture
def missing_df(rng, long_df):

    df = long_df.copy()
    for col in df:
        idx = rng.permutation(df.index)[:10]
        df.loc[idx, col] = np.nan
    return df


@pytest.fixture
def null_column():

    return pd.Series(index=np.arange(20), dtype='float64')
