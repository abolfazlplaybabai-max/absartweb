(function () {
    "use strict";

    function createMotionLayer() {

        const oldLayer =
            document.getElementById("abs-motion-layer");

        if (oldLayer) {
            oldLayer.remove();
        }

        const layer =
            document.createElement("div");

        layer.id = "abs-motion-layer";

        /* سه هاله */
        const orb1 =
            document.createElement("div");

        orb1.className =
            "abs-motion-orb orb-1";

        const orb2 =
            document.createElement("div");

        orb2.className =
            "abs-motion-orb orb-2";

        const orb3 =
            document.createElement("div");

        orb3.className =
            "abs-motion-orb orb-3";

        layer.appendChild(orb1);
        layer.appendChild(orb2);
        layer.appendChild(orb3);

        /* نورهای کوچک */
        const mobile =
            window.innerWidth <= 700;

        const count =
            mobile ? 8 : 14;

        for (let i = 0; i < count; i++) {

            const glow =
                document.createElement("div");

            glow.className =
                "abs-motion-glow";

            const x =
                Math.random() * 100;

            const y =
                Math.random() * 100;

            const moveX =
                (Math.random() * 180) - 90;

            const moveY =
                (Math.random() * 180) - 90;

            const duration =
                14 + Math.random() * 18;

            glow.style.left =
                x + "vw";

            glow.style.top =
                y + "vh";

            glow.style.setProperty(
                "--move-x",
                moveX + "px"
            );

            glow.style.setProperty(
                "--move-y",
                moveY + "px"
            );

            glow.style.setProperty(
                "--duration",
                duration + "s"
            );

            glow.style.animationDelay =
                (-Math.random() * duration) + "s";

            layer.appendChild(glow);
        }

        document.body.prepend(layer);
    }

    function init() {
        createMotionLayer();
    }

    if (
        document.readyState ===
        "loading"
    ) {
        document.addEventListener(
            "DOMContentLoaded",
            init
        );
    } else {
        init();
    }
})();
