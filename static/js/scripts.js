document.addEventListener('DOMContentLoaded', () => {
    console.log('Custom JavaScript loaded for South Peake');

    // Highlight active menu items
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navLinks.forEach(nav => nav.classList.remove('active'));
            link.classList.add('active');
        });
    });

    // Carousel logic
    const carousel = document.querySelector('#carouselExampleIndicators');
    const videos = carousel.querySelectorAll('video');

    // Disable carousel controls when hovering over video
    videos.forEach(video => {
        video.addEventListener('mouseenter', () => {
            carousel.querySelectorAll('.carousel-control-prev, .carousel-control-next').forEach(control => {
                control.style.pointerEvents = 'none';
            });
        });

        video.addEventListener('mouseleave', () => {
            carousel.querySelectorAll('.carousel-control-prev, .carousel-control-next').forEach(control => {
                control.style.pointerEvents = 'auto';
            });
        });
    });

    // Pause videos on slide change
    carousel.addEventListener('slide.bs.carousel', () => {
        videos.forEach(video => {
            video.pause();
            video.currentTime = 0; // Reset playback to the start
        });
    });

    // Ensure proper visibility of videos
    const updateVideoVisibility = () => {
        const items = carousel.querySelectorAll('.carousel-item');
        items.forEach(item => {
            const video = item.querySelector('video');
            if (video) {
                if (!item.classList.contains('active')) {
                    video.style.display = 'none'; // Hide videos not in the active slide
                } else {
                    video.style.display = 'block'; // Show video for active slide
                }
            }
        });
    };

    // Run on initialization and slide change
    carousel.addEventListener('slid.bs.carousel', updateVideoVisibility);
    updateVideoVisibility(); // Initial call to set visibility correctly
});
