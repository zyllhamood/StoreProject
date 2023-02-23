const themes = [
    {
        background: "#373737",
        color: "#FFFFFF",
        primaryColor: "#515151"
    },
    {
        background: "#373737",
        color: "#FFFFFF",
        primaryColor: "#515151"
    },
    {
        background: "#373737",
        color: "#FFFFFF",
        primaryColor: "#515151"
    },
    {
        background: "#373737",
        color: "#000000",
        primaryColor: "#515151"
    },
    {
        background: "#373737",
        color: "#000000",
        primaryColor: "#515151"
    },
    {
        background: "#373737",
        color: "#FFF",
        primaryColor: "#515151"
    }
];

const setTheme = (theme) => {
    const root = document.querySelector(":root");
    root.style.setProperty("--background", theme.background);
    root.style.setProperty("--color", theme.color);
    root.style.setProperty("--primary-color", theme.primaryColor);
    root.style.setProperty("--glass-color", theme.glassColor);
};

const displayThemeButtons = () => {
    const btnContainer = document.querySelector(".theme-btn-container");
    themes.forEach((theme) => {
        const div = document.createElement("div");
        div.className = "theme-btn";
        div.style.cssText = `background: ${theme.background}; width: 25px; height: 25px`;
        btnContainer.appendChild(div);
        div.addEventListener("click", () => setTheme(theme));
    });
};

displayThemeButtons();
