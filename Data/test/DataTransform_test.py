
import pandas as pd
from pandas._testing import assert_frame_equal
from ..lib.DataTransform import DataTransform
import datetime as dt


def test_normalise_returns_valid_data():
    # Setup input
    stats = pd.DataFrame([[1.073594e+01, 5.287401e+00],
                          [1.073594e+01, 5.287401e+00]], columns=['mean', 'std'])
    x = pd.DataFrame([[1, 2], [3, 4], [1, 2], [3, 4]])

    # Run function under test
    result = DataTransform.normalise(x, stats)

    # Validate output
    expectedResult = pd.DataFrame(
        [[-1.841347, -1.652218], [-1.463089, -1.273960], [-1.841347, -1.652218], [-1.463089, -1.273960]])
    assert_frame_equal(expectedResult, result)


def test_get_unix():
    x = '2020-01-01T10:11:12.00Z'

    result = DataTransform.get_unix(x)

    assert result == 1577873472


def test_no_days_ago():
    x = (dt.datetime.now() - dt.timedelta(days=10)
         ).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    print(x)
    result = DataTransform.no_days_ago(x)
    assert result == 10

def test_get_hour():
    x = '2020-01-01T10:11:12.00Z'
    
    result = DataTransform.get_hour(x)

    assert result == 10

def test_get_month():
    x = '2020-01-01T10:11:12.00Z'
    
    result = DataTransform.get_month(x)

    assert result == 1
