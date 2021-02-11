var ll = new LazyLoad();

const showHideButton = document.querySelector(".action-button");
const files = document.querySelector(".files");
showHideButton.addEventListener("click", () => {
  files.classList.toggle("hidden");
  showHideButton.classList.toggle("show-button");
  showHideButton.classList.toggle("hide-button");
});

imagesOrVideos = document.querySelectorAll("img, video");
imagesOrVideos.forEach((el) => {
  el.addEventListener("click", () => (window.open(el.src, "_blank")));
});
