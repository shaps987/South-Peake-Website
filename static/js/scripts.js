// Ensure the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('Custom JavaScript loaded for South Peake');

    // Example functionality: Highlight active menu items
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navLinks.forEach(nav => nav.classList.remove('active'));
            link.classList.add('active');
        });
    });
});
