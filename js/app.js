const updateCartCount = () => {
    const cartStr = localStorage.getItem('fujiwa_cart');
    let count = 0;
    if(cartStr) {
        const cart = JSON.parse(cartStr);
        count = cart.reduce((sum, item) => sum + item.quantity, 0);
    } else {
        count = 3; // default UI badge
    }
    const cartBadge = document.querySelector('.fa-basket-shopping').nextElementSibling;
    if(cartBadge) cartBadge.innerText = count;
};

document.addEventListener('DOMContentLoaded', () => {
    updateCartCount();

    // Lắng nghe sự kiện click vào ảnh hoặc tiêu đề sản phẩm để chuyển đến trang chi tiết
    const productCards = document.querySelectorAll('.grid > div.bg-white.border');
    productCards.forEach(card => {
        const img = card.querySelector('img');
        const title = card.querySelector('h3');
        if(img && title) {
            [img, title].forEach(el => {
                el.style.cursor = 'pointer';
                el.addEventListener('click', (e) => {
                    // Nếu click vào nút "Thêm vào giỏ" thì bỏ qua
                    if(e.target.tagName.toLowerCase() === 'button' || e.target.closest('button')) return;

                    const name = title.innerText;
                    const price = card.querySelector('.text-red-600').innerText;
                    const oldPriceEl = card.querySelector('.line-through');
                    const oldPrice = oldPriceEl ? oldPriceEl.innerText : '';
                    const imgSrc = img.src;
                    const descEl = card.querySelector('p.text-gray-400');
                    const desc = descEl ? descEl.innerText : '';
                    
                    const productData = { name, price, oldPrice, img: imgSrc, desc };
                    localStorage.setItem('selectedProduct', JSON.stringify(productData));
                    window.location.href = 'product-detail.html';
                });
            });
        }
    });

    // Lắng nghe sự kiện thêm vào giỏ hàng ngay tại danh sách
    const addToCartBtns = document.querySelectorAll('button');
    addToCartBtns.forEach(btn => {
        if(btn.id === 'btn-add-to-cart-detail') return; // Bỏ qua nút ở trang chi tiết
        if(btn.innerText.includes('Thêm vào giỏ') || btn.innerText.includes('Đặt đổi bình')) {
            btn.addEventListener('click', (e) => {
                const card = e.target.closest('.bg-white.border');
                if(!card) return;
                const name = card.querySelector('h3').innerText;
                const priceStr = card.querySelector('.text-red-600').innerText;
                const price = parseInt(priceStr.replace(/[^0-9]/g, '')) || 0;
                const imgSrc = card.querySelector('img').src;

                let cart = JSON.parse(localStorage.getItem('fujiwa_cart') || '[]');
                const existing = cart.find(i => i.name === name);
                if(existing) {
                    existing.quantity += 1;
                } else {
                    cart.push({ name, price, img: imgSrc, quantity: 1 });
                }
                localStorage.setItem('fujiwa_cart', JSON.stringify(cart));
                updateCartCount();
                alert('Đã thêm "' + name + '" vào giỏ hàng!');
            });
        }
    });
});
