// donations/static/js/profile.js

document.addEventListener('DOMContentLoaded', function() {
    let tabLinks = document.querySelectorAll('.tab-link');
    let tabContents = document.querySelectorAll('.tab-content');

    tabLinks.forEach(function(link) {
        link.addEventListener('click', function() {
            let tabId = this.getAttribute('data-tab');

            tabLinks.forEach(function(link) {
                link.classList.remove('active');
            });

            tabContents.forEach(function(content) {
                content.classList.remove('active');
            });

            this.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        });
    });
});
