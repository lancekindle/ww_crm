"""
Visual regression tests for the Window Wash CRM application.

These tests capture screenshots of different pages in the application and compare them
against baseline images to detect unintended visual changes in the UI.
"""
import os
import logging
import pytest
from pathlib import Path
from PIL import Image, ImageChops, ImageStat
from playwright.sync_api import Page, expect

from ww_crm.tests.e2e.pages.home_page import HomePage
from ww_crm.tests.e2e.pages.customer_list_page import CustomerListPage
from ww_crm.tests.e2e.pages.customer_create_page import CustomerCreatePage
from ww_crm.tests.e2e.pages.invoice_list_page import InvoiceListPage

# Set up logging
logger = logging.getLogger(__name__)

# Mark all tests in this module as requiring the live_server and as e2e tests
pytestmark = [
    pytest.mark.usefixtures('live_server'),
    pytest.mark.e2e,
    pytest.mark.visual
]

# Configuration for visual regression tests
SCREENSHOT_DIR = Path(__file__).parent / "screenshots"
BASELINE_DIR = SCREENSHOT_DIR / "baseline"
ACTUAL_DIR = SCREENSHOT_DIR / "actual"
DIFF_DIR = SCREENSHOT_DIR / "diff"
THRESHOLD = 0.01  # Threshold for image difference (1%)


class TestVisual:
    """
    Visual regression tests for the Window Wash CRM application.

    These tests capture screenshots of different pages and compare them
    against baseline images to detect unintended visual changes.
    """

    @pytest.fixture(autouse=True)
    def setup(self, page: Page, live_server):
        """Set up page objects and directories for each test."""
        logger.info("Setting up visual regression test")

        # Create screenshot directories if they don't exist
        for directory in [BASELINE_DIR, ACTUAL_DIR, DIFF_DIR]:
            directory.mkdir(parents=True, exist_ok=True)

        # Initialize page objects
        self.home_page = HomePage(page, live_server.url())
        self.customer_list_page = CustomerListPage(page, live_server.url())
        self.customer_create_page = CustomerCreatePage(page, live_server.url())
        self.invoice_list_page = InvoiceListPage(page, live_server.url())

        # Store context for later use
        self.page = page
        self.live_server = live_server

    def take_screenshot(self, name):
        """
        Take a screenshot of the current page.

        Args:
            name: Name of the screenshot (without extension)

        Returns:
            Path to the screenshot
        """
        filepath = ACTUAL_DIR / f"{name}.png"
        self.page.screenshot(path=str(filepath), full_page=True)
        logger.info(f"Captured screenshot: {filepath}")
        return filepath

    def compare_screenshots(self, name):
        """
        Compare the actual screenshot with the baseline.

        Args:
            name: Name of the screenshot (without extension)

        Returns:
            float: Difference ratio (0 to 1)
        """
        baseline_path = BASELINE_DIR / f"{name}.png"
        actual_path = ACTUAL_DIR / f"{name}.png"
        diff_path = DIFF_DIR / f"{name}.png"

        # If baseline doesn't exist, copy actual to baseline and pass the test
        if not baseline_path.exists():
            logger.info(f"Baseline doesn't exist, creating: {baseline_path}")
            import shutil
            shutil.copy(actual_path, baseline_path)
            return 0

        # Compare images
        baseline_img = Image.open(baseline_path)
        actual_img = Image.open(actual_path)

        # Make sure the images are the same size
        if baseline_img.size != actual_img.size:
            logger.warning(f"Image sizes don't match! Baseline: {baseline_img.size}, Actual: {actual_img.size}")
            actual_img = actual_img.resize(baseline_img.size)

        # Calculate difference
        diff_img = ImageChops.difference(baseline_img, actual_img)
        stat = ImageStat.Stat(diff_img)

        # Calculate the average difference across all channels
        if len(stat.mean) >= 3:  # RGB or RGBA
            diff_ratio = sum(stat.mean[:3]) / (3 * 255)
        else:  # Grayscale
            diff_ratio = stat.mean[0] / 255

        # Save the diff image if there's a significant difference
        if diff_ratio > THRESHOLD:
            logger.info(f"Visual difference detected: {diff_ratio:.4f}, saving diff to {diff_path}")
            diff_img.save(diff_path)
        else:
            logger.info(f"Images match within threshold: {diff_ratio:.4f}")

            # Delete the diff file if it exists
            if diff_path.exists():
                diff_path.unlink()

        return diff_ratio

    def assert_visual_match(self, name):
        """
        Assert that the screenshot matches the baseline.

        Args:
            name: Name of the screenshot (without extension)
        """
        # Take screenshot
        self.take_screenshot(name)

        # Compare with baseline
        diff_ratio = self.compare_screenshots(name)

        # Assert difference is below threshold
        assert diff_ratio <= THRESHOLD, f"Visual regression detected: {diff_ratio:.4f} > {THRESHOLD}"

    def test_home_page_visual(self):
        """Test the visual appearance of the home page."""
        logger.info("Running visual test: home_page")

        # Navigate to home page
        self.home_page.navigate()
        self.home_page.assert_page_loaded()

        # Verify visual appearance matches baseline
        self.assert_visual_match("home_page")

    def test_customer_list_visual(self, sample_customer):
        """Test the visual appearance of the customer list page."""
        logger.info("Running visual test: customer_list")

        # Navigate to customer list page
        self.customer_list_page.navigate()
        self.customer_list_page.assert_page_loaded()

        # Verify visual appearance matches baseline
        self.assert_visual_match("customer_list")

    def test_customer_create_visual(self):
        """Test the visual appearance of the customer creation page."""
        logger.info("Running visual test: customer_create")

        # Navigate to customer create page
        self.customer_create_page.navigate()
        self.customer_create_page.assert_page_loaded()

        # Verify visual appearance matches baseline
        self.assert_visual_match("customer_create")

    def test_invoice_list_visual(self, sample_invoice):
        """Test the visual appearance of the invoice list page."""
        logger.info("Running visual test: invoice_list")

        # Navigate to invoice list page
        self.invoice_list_page.navigate()
        self.invoice_list_page.assert_page_loaded()

        # Verify visual appearance matches baseline
        self.assert_visual_match("invoice_list")
