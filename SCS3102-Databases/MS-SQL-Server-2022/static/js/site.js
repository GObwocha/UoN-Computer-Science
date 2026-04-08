document.addEventListener("DOMContentLoaded", () => {
  const flashCards = document.querySelectorAll("[data-autodismiss='true']");

  flashCards.forEach((card) => {
    window.setTimeout(() => {
      card.style.opacity = "0";
      card.style.transform = "translateY(-6px)";
      window.setTimeout(() => card.remove(), 400);
    }, 5000);
  });
});
