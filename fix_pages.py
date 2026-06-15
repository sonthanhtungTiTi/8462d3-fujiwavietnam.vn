import os
import re

files = ['index.html', 'page2.html', 'page3.html', 'page4.html', 'page5.html', 'page6.html']

for page_num, file in enumerate(files, start=1):
    if not os.path.exists(file): continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update product cards with animation and hover classes
    # We will search for the card div by its classes, allowing flexible whitespace
    card_pattern = r'class="bg-white\s+border\s+rounded-xl\s+overflow-hidden\s+shadow-sm\s*[\r\n]*\s*hover:shadow-md\s+transition\s+flex\s+flex-col\s+justify-between"'
    new_card_class = 'class="bg-white border rounded-xl overflow-hidden shadow-sm hover:shadow-2xl transition-all duration-300 flex flex-col justify-between product-card animate-slide-up hover:-translate-y-2 cursor-pointer"'
    
    # We also need to add style="animation-delay: Xms; opacity: 0;" to each card.
    # Because we want staggering, we'll replace them one by one.
    cards = list(re.finditer(card_pattern, content))
    for i, match in enumerate(cards):
        delay = (i % 8) * 100
        replacement = f'{new_card_class} style="animation-delay: {delay}ms; opacity: 0;"'
        content = content.replace(match.group(0), replacement, 1)

    # 2. Update pagination
    # The pagination block starts with <!-- 5. ... PHÂN TRANG ... --> and ends with </div>
    pagination_pattern = r'(<!--\s*5\.\s*PHÂN TRANG.*?<div\s+class="flex\s+justify-center\s+items-center\s+space-x-2\s+mt-12">)(.*?)(</div>)'
    
    # Generate new pagination HTML
    pag_html = '\n'
    prev_link = f'page{page_num-1}.html' if page_num > 1 else '#'
    if prev_link == 'page1.html': prev_link = 'index.html'
    prev_class = "px-4 py-2 border rounded-lg text-gray-400 pointer-events-none" if page_num == 1 else "px-4 py-2 border border-gray-300 text-gray-600 hover:bg-gray-100 rounded-lg transition"
    
    pag_html += f'            <a href="{prev_link}" class="{prev_class}"><i class="fa-solid fa-chevron-left"></i></a>\n'
    
    for i in range(1, 7):
        link = 'index.html' if i == 1 else f'page{i}.html'
        if i == page_num:
            pag_html += f'            <a href="#" class="px-4 py-2 bg-fuji-blue text-white rounded-lg font-bold">{i}</a>\n'
        else:
            pag_html += f'            <a href="{link}" class="px-4 py-2 border border-gray-300 text-gray-600 hover:bg-gray-100 rounded-lg transition">{i}</a>\n'

    next_link = f'page{page_num+1}.html' if page_num < 6 else '#'
    next_class = "px-4 py-2 border rounded-lg text-gray-400 pointer-events-none" if page_num == 6 else "px-4 py-2 border border-gray-300 text-gray-600 hover:bg-gray-100 rounded-lg transition"
    pag_html += f'            <a href="{next_link}" class="{next_class}"><i class="fa-solid fa-chevron-right"></i></a>\n        '
    
    content = re.sub(pagination_pattern, r'\1' + pag_html + r'\3', content, flags=re.DOTALL | re.IGNORECASE)

    # Also update "Trang X / Y" text
    content = re.sub(r'Trang\s+\d+\s+/\s+\d+', f'Trang {page_num} / 6', content)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print('Updated all files successfully.')
