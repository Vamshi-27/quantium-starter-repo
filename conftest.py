import pytest
from dash.testing.application_runners import import_app
from dash.testing.composite import DashComposite


@pytest.fixture
def dash_duo(dash_duo):
    """Configure dash_duo fixture with proper settings"""
    dash_duo.driver.implicitly_wait(10)
    return dash_duo
