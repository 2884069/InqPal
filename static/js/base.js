function setActiveNavLink() {
    const currentUrl = window.location.pathname;
    const header_links = document.querySelectorAll('.header_links a');

    for (let link of header_links) {
        const isActive = link.getAttribute('href') === currentUrl;
        if (isActive) link.classList.add('active'); 
    }
}

document.addEventListener('DOMContentLoaded', setActiveNavLink);