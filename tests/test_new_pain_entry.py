import os
import pytest
import re
from playwright.sync_api import sync_playwright, expect

def test_new_pain_entry_prototype():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Construct file URL
        basedir = os.getcwd()
        file_url = f"file://{basedir}/src/prototype/new-pain-entry.html"
        
        # Open page
        page.goto(file_url)
        
        # Create output directory
        output_dir = f"{basedir}/build/tests/new-pain-entry"
        os.makedirs(output_dir, exist_ok=True)
        
        # 1. Default View (Back)
        expect(page.locator("#body-back")).to_be_visible()
        page.screenshot(path=f"{output_dir}/1_back_view.png")
        
        # 2. Back View
        page.click("#btn-view-back")
        expect(page.locator("#body-back")).to_be_visible()
        expect(page.locator("#body-front")).not_to_be_visible()
        # Verify K&S label
        expect(page.locator("text=K&S")).to_be_visible()
        page.screenshot(path=f"{output_dir}/2_back_view_ks.png")
        
        # 3. Front View
        page.click("#btn-view-front")
        expect(page.locator("#body-front")).to_be_visible()
        page.screenshot(path=f"{output_dir}/3_front_view.png")
        
        # 4. Other View
        page.click("#btn-view-other")
        expect(page.locator("#other-view-container")).to_be_visible()
        # Verify Schmerzfrei icon
        expect(page.locator("#pain-free-item")).to_contain_text("accessibility_new")
        page.screenshot(path=f"{output_dir}/3_other_view.png")
        
        # 4. Settings View
        page.click("#nav-settings")
        expect(page.locator("#settings-view")).to_be_visible()
        page.screenshot(path=f"{output_dir}/4_settings_view.png")
        
        # 5. Add Custom Pain Type
        page.fill("#new-pain-name", "Migräne")
        page.fill("#new-pain-icon", "bolt")
        page.click("button:has-text('add')")
        
        # Verify added in list
        expect(page.locator("#settings-list")).to_contain_text("Migräne")
        page.screenshot(path=f"{output_dir}/5_settings_added.png")
        
        # Close settings and verify in Other view
        page.click("button:has-text('Schließen')")
        expect(page.locator("#other-view-container")).to_be_visible()
        expect(page.locator("#other-pain-list")).to_contain_text("Migräne")
        page.screenshot(path=f"{output_dir}/6_other_view_updated.png")
        
        # 7. Verify Coloring Logic & Reset
        page.click("#btn-view-front")
        # Click Head
        page.click("#front_head")
        # Select Level 3 (Stark - #fb923c)
        page.click("button:has-text('Stark')")
        # Verify style.fill is set
        expect(page.locator("#front_head")).to_have_attribute("style", "fill: rgb(251, 146, 60);")
        page.screenshot(path=f"{output_dir}/7_coloring_verified.png")
        
        # Reset to No Pain
        page.click("#front_head")
        page.click("button:has-text('Kein Schmerz')")
        # Verify style.fill is reset (default #E6E0E9 -> rgb(230, 224, 233))
        # Or check if data-level is 0
        expect(page.locator("#front_head")).to_have_attribute("data-level", "0")
        # Check style is default
        expect(page.locator("#front_head")).to_have_attribute("style", "fill: rgb(230, 224, 233);")
        page.screenshot(path=f"{output_dir}/8_color_reset_verified.png")

        # 8. Verify Edit Functionality
        page.click("#nav-settings")
        # Edit "Migräne" (assuming it's the last one added)
        # Find the edit button for Migräne. It's in the same container.
        # We can look for the row containing "Migräne" and then the edit button.
        migrane_row = page.locator("#settings-list > div", has_text="Migräne")
        migrane_row.locator("button:has-text('edit')").click()
        
        # Verify inputs populated
        expect(page.locator("#new-pain-name")).to_have_value("Migräne")
        expect(page.locator("#new-pain-icon")).to_have_value("bolt")
        # Verify button icon changed
        expect(page.locator("#add-btn-icon")).to_have_text("check")
        
        # Change values
        page.fill("#new-pain-name", "Cluster")
        page.fill("#new-pain-icon", "flash_on")
        page.click("button:has(#add-btn-icon)") # Click the update button
        
        # Verify updated in list
        expect(page.locator("#settings-list")).to_contain_text("Cluster")
        expect(page.locator("#settings-list")).not_to_contain_text("Migräne") # Old name gone
        page.screenshot(path=f"{output_dir}/9_edit_verified.png")
        
        # Verify in Other view
        page.click("button:has-text('Schließen')")
        page.click("#btn-view-other")
        expect(page.locator("#other-pain-list")).to_contain_text("Cluster")
        # Verify layout classes
        expect(page.locator("#other-pain-list")).to_have_class(re.compile(r"grid-cols-2"))
        page.screenshot(path=f"{output_dir}/10_other_view_updated_edit.png")

        print(f"Screenshots saved to {output_dir}")
        browser.close()
