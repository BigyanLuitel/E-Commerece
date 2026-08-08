document.addEventListener('DOMContentLoaded', function () {
    const payForm = document.getElementById('payForm');
    const payBtn = document.getElementById('payBtn');
    if (payForm) {
        payForm.addEventListener('submit', function (e) {
            e.preventDefault();
            payBtn.disabled = true;
            payBtn.textContent = 'Processing...';
            setTimeout(function () {
                payForm.submit();
            }, 1400);
        });
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.getElementById('mobileToggle');
    const nav = document.getElementById('categoryNav');
    if (toggle && nav) {
        toggle.addEventListener('click', function () {
            nav.classList.toggle('open');
        });
    }
});
document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.getElementById('chatToggle');
    const panel = document.getElementById('chatPanel');
    const closeBtn = document.getElementById('chatClose');
    const form = document.getElementById('chatForm');
    const input = document.getElementById('chatInput');
    const messagesEl = document.getElementById('chatMessages');

    if (!toggle) return; // widget not present (user not logged in)

    toggle.addEventListener('click', () => panel.classList.toggle('open'));
    closeBtn.addEventListener('click', () => panel.classList.remove('open'));

    function getCookie(name) {
        const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
        return match ? match[2] : null;
    }

    function addMessage(text, role) {
        const div = document.createElement('div');
        div.className = `chat-msg chat-msg-${role}`;
        div.textContent = text;
        messagesEl.appendChild(div);
        messagesEl.scrollTop = messagesEl.scrollHeight;
        return div;
    }

    function addQrMessage(qrBase64, paymentUrl) {
        const div = document.createElement('div');
        div.className = 'chat-msg chat-msg-assistant chat-msg-qr';
        div.innerHTML = `
            <div>Scan to pay:</div>
            <img src="data:image/png;base64,${qrBase64}" alt="Payment QR code">
            <a href="${paymentUrl}" target="_blank">Or open payment page</a>
        `;
        messagesEl.appendChild(div);
        messagesEl.scrollTop = messagesEl.scrollHeight;
    }

    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        const message = input.value.trim();
        if (!message) return;

        addMessage(message, 'user');
        input.value = '';

        const typing = addMessage('Typing...', 'typing');

        try {
            const response = await fetch("/chat/send/", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({ message }),
            });

            const data = await response.json();
            typing.remove();

            if (!response.ok) {
                addMessage(data.error || 'Something went wrong.', 'assistant');
                return;
            }

            addMessage(data.reply, 'assistant');

            if (data.payment_qr_base64) {
                addQrMessage(data.payment_qr_base64, data.payment_url);
            }
        } catch (err) {
            typing.remove();
            addMessage('Could not reach the assistant. Please try again.', 'assistant');
        }
    });
});
const resetBtn = document.getElementById('chatReset');
    if (resetBtn) {
        resetBtn.addEventListener('click', async function () {
            await fetch("/chat/reset/", {
                method: 'POST',
                headers: { 'X-CSRFToken': getCookie('csrftoken') },
            });
            messagesEl.innerHTML = '<div class="chat-msg chat-msg-assistant">Hi! I can help you find products, answer questions, or place an order. What are you looking for?</div>';
        });
    }