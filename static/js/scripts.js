document.addEventListener('DOMContentLoaded', () => {
    console.log('Custom JavaScript loaded for South Peake');

    const carousel = document.querySelector('#carouselExampleIndicators');
    const videos = carousel.querySelectorAll('video');

    // Pause and reset videos on slide change
    carousel.addEventListener('slide.bs.carousel', () => {
        videos.forEach(video => {
            video.pause();
            video.currentTime = 0; // Reset video playback
        });
    });

    // Ensure only the active slide's video is visible
    carousel.addEventListener('slid.bs.carousel', () => {
        const activeItem = carousel.querySelector('.carousel-item.active');
        videos.forEach(video => {
            video.style.display = 'none'; // Hide all videos
        });

        const activeVideo = activeItem.querySelector('video');
        if (activeVideo) {
            activeVideo.style.display = 'block'; // Show active video
        }
    });

    // Handle video interaction disabling carousel controls
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

        // Prevent propagation of click events on the video to carousel controls
        video.addEventListener('click', (event) => {
            event.stopPropagation(); // Prevent click from triggering carousel controls
        });
    });
});
