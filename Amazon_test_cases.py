from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False) #slow_mo=500
    context = browser.new_context()
    page = context.new_page()
    page.set_default_timeout(100000)

    page.goto("https://www.amazon.in/")
    page.wait_for_load_state("load")
    page.get_by_role("link", name="Sign in", exact=True).click()
    page.get_by_label("Email or mobile phone number").fill("shashwat.jn@gmail.com")
    page.get_by_label("Continue").click()
    page.get_by_label("Password").click()
    page.get_by_label("Password").fill("Xxxxx@xx")
    page.get_by_label("Sign in").click()

    # login assertion
    expect(page.get_by_role("link", name="Hello, Shashwat Account &"))

    page.get_by_placeholder("Search Amazon.in").fill("nike shoes")
    page.get_by_placeholder("Search Amazon.in").press("Enter")
    page.get_by_placeholder("Min").click()
    page.get_by_placeholder("Min").fill("4000")
    page.get_by_placeholder("Max").click()
    page.get_by_placeholder("Max").click()
    page.get_by_placeholder("Max").fill("10000")
    page.get_by_label("Price", exact=True).get_by_label("Go").click() #click(timeout=100)
    page.get_by_label("9", exact=True).click()
    page.get_by_text("70% Off or more").click()
    page.locator("[id=\"p_n_pct-off-with-tax\\/27060457031\"]").click()
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="NIKE Air Winflo 10 Men's").click()
    page1 = page1_info.value
    page1.get_by_text("6,521", exact=True).click()
    page1.get_by_text("-25%").click()
    product_name = page1.get_by_role("heading", name="NIKE Air Winflo 10 Men's").text_content()
    # print(product_name)
    # product_name2 = page1.locator("#productTitle").text_content()
    # print(product_name2)
    page1.get_by_title("Add to Shopping Cart").click()
    page1.close()

    # page.pause()

    page.goto("https://www.amazon.in/ref=nav_logo")
    page.get_by_label("item in cart").click()
    product_name_cart = page.get_by_role("link", name="Nike AIR Winflo 10-White/Wolf GREY-WHITE-DV4022-102-9UK", exact=True).text_content()
    print('product_name_cart', product_name_cart)
    print(page.get_by_text("6,521.00").text_content())

    # Same Item added to cart assertion
    assert product_name.strip == product_name_cart.strip

    page.wait_for_timeout(10)
    page.pause()
    print("Test Completed")
    # ---------------------
    # context.close()
    # browser.close()


with sync_playwright() as playwright:
    run(playwright)
