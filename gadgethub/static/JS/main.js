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