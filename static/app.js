const form = document.getElementById("form");

form.addEventListener("submit", (event) => {
  event.preventDefault();

  const formInputValue = form.elements.prompt.value;
  const requestBody = { prompt: formInputValue };

  fetch("/generate-colors", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(requestBody),
  })
    .then((res) => {
      return res.json();
    })
    .then((data) => {
      const colors = data.colors;
      const container = document.querySelector(".container");
      container.innerHTML = "";
      for (const color of colors) {
        const div = document.createElement("div");
        div.classList.add("color");
        div.style.backgroundColor = color;
        div.style.width = `calc(100% / ${colors.length})`;

        div.addEventListener("click", () => {
          navigator.clipboard.writeText(color);
        });

        const span = document.createElement("span");
        span.innerText = color;
        div.appendChild(span);
        container.appendChild(div);
      }
    });
});
