# ============================================================
# PYTEST CONFIGURATION / FIXTURES
# ============================================================

import sys
from pathlib import Path

import pytest


# ============================================================
# ADD PROJECT ROOT TO PYTHON PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# NOW IMPORT OUR SPARK UTILITY
# ============================================================

from utilities.spark_utils import create_spark_session


# ============================================================
# SPARK SESSION FIXTURE
# ============================================================

@pytest.fixture(scope="session")
def spark():

    print("\n==========================================")
    print("CREATING SPARK SESSION")
    print("==========================================")

    spark_session = create_spark_session()

    yield spark_session

    print("\n==========================================")
    print("STOPPING SPARK SESSION")
    print("==========================================")

    spark_session.stop()