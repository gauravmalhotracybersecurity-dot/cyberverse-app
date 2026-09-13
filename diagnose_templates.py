import os, re

print("=== DIAGNOSING TEMPLATE STRUCTURE ===\n")

# Check what /learn/index.html extends
learn = open("backend/templates/learn/index.html", encoding="utf-8").read()
print("1. /learn/index.html:")
if "{% extends" in learn:
    match = re.search(r'{% extends ["\']([^"\']+)["\']', learn)
    if match:
        print(f"   Extends: {match.group(1)}")
    print(f"   Has block canonical: {'{% block canonical' in learn}")
    print(f"   Has block head: {'{% block head' in learn}")
else:
    print("   ⚠️  Does NOT extend any template (inline HTML)")
    print(f"   Has <html> tag: {'<html' in learn}")
    print(f"   First 400 chars:\n{learn[:400]}\n")

# Check what /resources.html extends
resources = open("backend/templates/resources.html", encoding="utf-8").read()
print("\n2. /resources.html:")
if "{% extends" in resources:
    match = re.search(r'{% extends ["\']([^"\']+)["\']', resources)
    if match:
        print(f"   Extends: {match.group(1)}")
    print(f"   Has block canonical: {'{% block canonical' in resources}")
    print(f"   Has block head: {'{% block head' in resources}")
else:
    print("   ⚠️  Does NOT extend any template (inline HTML)")
    print(f"   Has <html> tag: {'<html' in resources}")
    print(f"   First 400 chars:\n{resources[:400]}\n")

# Check what /books.html extends (working reference)
books = open("backend/templates/books.html", encoding="utf-8").read()
print("\n3. /books.html (working reference):")
if "{% extends" in books:
    match = re.search(r'{% extends ["\']([^"\']+)["\']', books)
    if match:
        print(f"   Extends: {match.group(1)}")

# Check what /careers.html extends (working reference)
careers = open("backend/templates/careers.html", encoding="utf-8").read()
print("\n4. /careers.html (working reference):")
if "{% extends" in careers:
    match = re.search(r'{% extends ["\']([^"\']+)["\']', careers)
    if match:
        print(f"   Extends: {match.group(1)}")

# Check article.html canonical
article = open("backend/templates/learn/article.html", encoding="utf-8").read()
print("\n5. Article canonical block:")
idx = article.find("{% block canonical %}")
if idx >= 0:
    end = article.find("{% endblock %}", idx)
    print(article[idx:end+14])

# Check if /resources has ebook cards
print("\n6. /resources ebook content:")
has_book_loop = "{% for b in books %}" in resources
has_book_cards = "Breaking Into GRC" in resources or "AI Workflows" in resources
has_see_all = "See All Books" in resources
print(f"   Has book loop: {has_book_loop}")
print(f"   Has individual book cards: {has_book_cards}")
print(f"   Has 'See All Books' link: {has_see_all}")
