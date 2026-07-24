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