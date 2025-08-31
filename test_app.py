import pytest
import time
from dash.testing.application_runners import import_app
from selenium.common.exceptions import TimeoutException


def test_header_present(dash_duo):
    """Test 1: Verify that the header is present"""
    try:
        # Import and start the app
        app = import_app("app")
        dash_duo.start_server(app)
        
        # Wait for the page to load and find the header
        dash_duo.wait_for_element("h1", timeout=10)
        header = dash_duo.find_element("h1")
        
        # Verify header contains expected text
        assert "Pink Morsel Sales Dashboard" in header.text
        print("✅ TEST 1 PASSED: Header is present with correct text")
        
    except Exception as e:
        print(f"❌ TEST 1 FAILED: {str(e)}")
        raise


def test_visualization_present(dash_duo):
    """Test 2: Verify that the sales chart visualization is present"""
    try:
        # Import and start the app
        app = import_app("app")
        dash_duo.start_server(app)
        
        # Wait for chart element to be present
        dash_duo.wait_for_element("#sales-chart", timeout=15)
        
        # Find the chart container
        chart_container = dash_duo.find_element("#sales-chart")
        assert chart_container is not None
        
        # Wait for plotly chart to render
        dash_duo.wait_for_element(".js-plotly-plot", timeout=15)
        chart = dash_duo.find_element(".js-plotly-plot")
        assert chart is not None
        
        print("✅ TEST 2 PASSED: Sales chart visualization is present")
        
    except Exception as e:
        print(f"❌ TEST 2 FAILED: {str(e)}")
        raise


def test_region_picker_present(dash_duo):
    """Test 3: Verify that the region picker (radio buttons) is present"""
    try:
        # Import and start the app
        app = import_app("app")
        dash_duo.start_server(app)
        
        # Wait for region filter to load
        dash_duo.wait_for_element("#region-filter", timeout=10)
        
        # Find the region filter container
        region_filter = dash_duo.find_element("#region-filter")
        assert region_filter is not None
        
        # Find all radio button inputs
        radio_buttons = dash_duo.find_elements("#region-filter input[type='radio']")
        
        # Verify we have the expected number of options (5 total)
        assert len(radio_buttons) == 5, f"Expected 5 radio options, found {len(radio_buttons)}"
        
        # Check for radio button labels in the DOM instead of values
        # The actual text content is in labels
        region_filter_text = region_filter.text
        
        # Verify expected region options are present in the text
        expected_regions = ["All", "North", "East", "South", "West"]
        for expected in expected_regions:
            assert expected in region_filter_text, f"Missing region option: {expected}"
        
        # Verify one radio button is selected by default
        selected_buttons = dash_duo.find_elements("#region-filter input[type='radio']:checked")
        assert len(selected_buttons) == 1, "Exactly one radio button should be selected by default"
        
        print("✅ TEST 3 PASSED: Region picker is present with all expected options")
        
    except Exception as e:
        print(f"❌ TEST 3 FAILED: {str(e)}")
        raise


def test_interactive_functionality(dash_duo):
    """Bonus Test: Verify that region filtering functionality works"""
    try:
        # Import and start the app
        app = import_app("app")
        dash_duo.start_server(app)
        
        # Wait for initial load
        dash_duo.wait_for_element("#region-filter", timeout=10)
        dash_duo.wait_for_element(".js-plotly-plot", timeout=15)
        
        # Wait for chart to fully render
        time.sleep(2)
        
        # Get initial chart (should show "All Regions")
        initial_chart_title = dash_duo.find_element(".gtitle").text
        assert "All" in initial_chart_title or "Regions" in initial_chart_title
        
        # Find and click the "North" radio button
        north_radio = None
        radio_buttons = dash_duo.find_elements("#region-filter input[type='radio']")
        labels = dash_duo.find_elements("#region-filter label")
        
        # Find the radio button for North region
        for i, label in enumerate(labels):
            if "North" in label.text:
                radio_buttons[i].click()
                break
        
        # Wait for chart to update
        time.sleep(3)
        
        # Verify chart title changed to reflect North region
        updated_chart_title = dash_duo.find_element(".gtitle").text
        assert "North" in updated_chart_title
        
        print("✅ BONUS TEST PASSED: Interactive region filtering works correctly")
        
    except Exception as e:
        print(f"❌ BONUS TEST FAILED: {str(e)}")
        raise


def test_kpi_cards_present(dash_duo):
    """Bonus Test: Verify KPI cards are present and display data"""
    try:
        # Import and start the app
        app = import_app("app")
        dash_duo.start_server(app)
        
        # Wait for page to load
        dash_duo.wait_for_element("h1", timeout=10)
        
        # Look for KPI card headers and values
        kpi_headers = dash_duo.find_elements("h4")
        kpi_values = dash_duo.find_elements("h2")
        
        # Should have KPI cards for Total Sales, Avg Daily Sales, Peak Sales
        expected_kpi_texts = ["Total Sales", "Avg Daily Sales", "Peak Sales"]
        
        kpi_texts = [header.text for header in kpi_headers]
        
        for expected_text in expected_kpi_texts:
            assert any(expected_text in text for text in kpi_texts), f"Missing KPI: {expected_text}"
        
        # Verify KPI values contain currency symbols
        value_texts = [h2.text for h2 in kpi_values]
        currency_values = [text for text in value_texts if "$" in text]
        assert len(currency_values) >= 3, "Should have at least 3 KPI values with currency"
        
        print("✅ BONUS TEST PASSED: KPI cards are present and display proper data")
        
    except Exception as e:
        print(f"❌ BONUS TEST FAILED: {str(e)}")
        raise
