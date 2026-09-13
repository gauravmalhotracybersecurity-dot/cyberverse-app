import urllib.request
req = urllib.request.Request("https://grcwithgaurav.com/books", headers={"User-Agent": "Mozilla/5.0"})
h = urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "ignore")

links = ["l/GRC", "l/Promptlibrary", "l/cyberhustle", "l/wxhxoo", "l/Gapanalysis", "l/Cybersecuritybundle"]
for l in links:
    print(f"  {'YES' if l in h else 'NO '} : {l}")
print(f"  Bundle price $35 shown: {'$35' in h}")
print(f"  Save $10 badge:         {'SAVE $10' in h}")
print(f"  Total gumroad links:    {h.count('malhotra72.gumroad.com/l/')}")
