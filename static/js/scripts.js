document.addEventListener('DOMContentLoaded', () => {
    console.log('Custom JavaScript loaded for South Peake');

    const carousel = document.querySelector('#carouselExampleIndicators');
    const videos = carousel.querySelectorAll('video');
    const controls = carousel.querySelectorAll('.carousel-control-prev, .carousel-control-next');

    // Pause and reset videos on slide change
    carousel.addEventListener('slide.bs.carousel', () => {
        videos.forEach(video => {
            video.pause();
            video.currentTime = 0; // Reset video playback
        });
    });

    // Show only the active video's content
    carousel.addEventListener('slid.bs.carousel', () => {
        const activeItem = carousel.querySelector('.carousel-item.active');
        videos.forEach(video => (video.style.display = 'none')); // Hide all videos

        const activeVideo = activeItem.querySelector('video');
        if (activeVideo) {
            activeVideo.style.display = 'block'; // Show the active video
        }
    });

    // Manage control buttons and video interactions
    videos.forEach(video => {
        // Disable carousel navigation controls when interacting with a video
        video.addEventListener('mouseenter', () => {
            controls.forEach(control => (control.style.pointerEvents = 'none'));
        });

        // Re-enable carousel navigation controls when leaving the video
        video.addEventListener('mouseleave', () => {
            controls.forEach(control => (control.style.pointerEvents = 'auto'));
        });

        // Ensure play/pause clicks work without affecting the carousel
        video.addEventListener('click', event => {
            event.stopPropagation(); // Prevent bubbling to carousel
        });

        // Re-enable carousel navigation when video is paused
        video.addEventListener('pause', () => {
            controls.forEach(control => (control.style.pointerEvents = 'auto'));
        });
    });

    // Prevent auto-slide back to the video
    carousel.addEventListener('slid.bs.carousel', () => {
        const activeVideo = carousel.querySelector('.carousel-item.active video');
        if (activeVideo) {
            activeVideo.pause(); // Ensure the video doesn't auto-play if not intended
        }
    });
});
