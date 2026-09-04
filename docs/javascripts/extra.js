document$.subscribe(function () {
    document.querySelectorAll(".expandable-code").forEach((box) => {

        if (box.dataset.expandableInitialized === "true") {
            return;
        }

        box.dataset.expandableInitialized = "true";

        const highlight = box.querySelector(".highlight");
        const pre = box.querySelector(".highlight pre");

        // Optional title
        if (box.dataset.title) {
            const title = document.createElement("div");
            title.className = "expand-code-title";
            title.textContent = box.dataset.title;

            box.insertBefore(title, box.firstChild);
        }

        // Number of lines to show
        const lines = parseInt(box.dataset.lines || "6", 10);

        if (highlight && pre) {
            const style = getComputedStyle(pre);

            const lineHeight = parseFloat(style.lineHeight);
            const paddingTop = parseFloat(style.paddingTop) || 0;
            const paddingBottom = parseFloat(style.paddingBottom) || 0;

            const collapsedHeight =
                lines * lineHeight +
                paddingTop +
                paddingBottom;

            box.style.setProperty(
                "--collapsed-height",
                `${collapsedHeight}px`
            );
        }

        const button = document.createElement("button");

        button.className = "expand-code-button";
        button.type = "button";
        button.textContent = "Expand";

        box.appendChild(button);

        button.addEventListener("click", function () {
            const expanded = box.classList.toggle("expanded");

            button.textContent =
                expanded ? "Collapse" : "Expand";
        });
    });
});