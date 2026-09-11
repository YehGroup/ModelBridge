function smoothScrollTo(targetY, duration = 800) {
    const startY = window.scrollY;
    const distance = targetY - startY;
    const startTime = performance.now();

    function easeInOut(t) {
        return t < 0.5
            ? 2 * t * t
            : 1 - Math.pow(-2 * t + 2, 2) / 2;
    }

    function step(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);

        window.scrollTo(
            0,
            startY + distance * easeInOut(progress)
        );

        if (progress < 1) {
            requestAnimationFrame(step);
        }
    }

    requestAnimationFrame(step);
}

document.addEventListener("click", function (event) {
    const link = event.target.closest("a");

    if (!link || !link.hash) return;

    const id = decodeURIComponent(link.hash.substring(1));
    const target = document.getElementById(id);

    if (!target || !target.classList.contains("math-target")) return;

    // Completely suppress normal/Zensical anchor navigation
    event.preventDefault();
    event.stopPropagation();
    event.stopImmediatePropagation();

    // Change the URL without causing a browser anchor jump
    history.replaceState(null, "", "#" + id);

    // Wait until other page processing has finished,
    // then explicitly center the target.
    requestAnimationFrame(function () {
        requestAnimationFrame(function () {

            const rect = target.getBoundingClientRect();

            const targetY =
                window.scrollY +
                rect.top -
                (window.innerHeight - rect.height) / 2;

            smoothScrollTo(targetY, 400);

            // Restart highlight every click
            target.getAnimations().forEach(animation => animation.cancel());

            target.animate(
                [
                    { backgroundColor: "rgba(255, 235, 59, 0.26)" },
                    { backgroundColor: "transparent" }
                ],
                {
                    duration: 1500,
                    easing: "ease-out"
                }
            );
        });
    });

}, true);