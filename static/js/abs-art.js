(function () {
    "use strict";

    /*
     * Static background only.
     * No animation.
     * No canvas.
     * No parallax.
     */

    const oldCanvas = document.getElementById("abs-art-canvas");
    if (oldCanvas) {
        oldCanvas.remove();
    }

    const oldVisual = document.querySelector(".abs-art-visual");
    if (oldVisual) {
        oldVisual.remove();
    }

    const oldBackground = document.getElementById("abs-art-static-bg");
    if (oldBackground) {
        oldBackground.remove();
    }

    const bg = document.createElement("div");
    bg.id = "abs-art-static-bg";
    bg.setAttribute("aria-hidden", "true");

    /* Static waves */
    for (let i = 1; i <= 3; i++) {
        const wave = document.createElement("div");
        wave.className = "abs-art-wave wave-" + i;
        bg.appendChild(wave);
    }

    /* Very small static particles */
    const particles = [
        [8, 17], [15, 31], [22, 13], [29, 44],
        [36, 22], [43, 64], [51, 18], [57, 38],
        [64, 14], [70, 56], [77, 27], [84, 43],
        [91, 19], [12, 72], [19, 86], [31, 77],
        [48, 91], [59, 73], [68, 88], [79, 76],
        [88, 91], [94, 65], [5, 53], [40, 35]
    ];

    particles.forEach(function (position, index) {
        const particle = document.createElement("span");

        particle.className = "abs-art-particle";

        particle.style.left = position[0] + "%";
        particle.style.top = position[1] + "%";

        if (index % 5 === 0) {
            particle.style.width = "1px";
            particle.style.height = "1px";
        }

        bg.appendChild(particle);
    });

    document.body.insertBefore(bg, document.body.firstChild);
})();
