from scraper.robots_checker import can_fetch


test_url = (
    "https://this-website-does-not-exist-12345.com/"
)


allowed = can_fetch(
    test_url
)


print("Robots.txt Error Handling Test")
print("=" * 45)

print(
    f"URL: {test_url}"
)

print(
    f"Allowed: {allowed}"
)


if allowed is False:

    print(
        "\nError handled correctly!"
    )

else:

    print(
        "\nUnexpected result!"
    )