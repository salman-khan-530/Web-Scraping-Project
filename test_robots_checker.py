from scraper.robots_checker import can_fetch


base_url = "https://books.toscrape.com/"

target_url = (
    "https://books.toscrape.com/"
)


allowed = can_fetch(
    base_url,
    target_url
)


print("Robots.txt Test")
print("=" * 40)

print(
    f"URL: {target_url}"
)

print(
    f"Allowed: {allowed}"
)


if allowed:

    print(
        "\nRobots.txt check passed!"
    )

else:

    print(
        "\nAccess is not allowed."
    )