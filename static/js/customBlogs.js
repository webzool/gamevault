const titles = [];

const tocElement = document.querySelector("#toc");

const HeadersofTocElement = tocElement.querySelectorAll("h2");







HeadersofTocElement.forEach((element) => {
  const id = element.innerHTML.replace(/#| /g, "-");
  element.id = id;
  titles.push({ id, title: element.innerHTML });
});

const ulElement = document.querySelector(".categories__ul");




titles.forEach((titles) => {
  ulElement.insertAdjacentHTML(
    "beforeend",
    `<li class="categories__li">
    <a href="#${titles.id}" class="categories__a">${titles.title}</a>
    </li>`
  );
});

console.log(titles, "titles");

const sidebar = document.querySelector(".categories__table");

const position = document.querySelector(".position");

const categories = document.querySelector(".categories");

window.addEventListener("scroll", () => {
  console.log(position.getBoundingClientRect().top, `position.getBoundingClientRect().top`);
  if (screen.width > 991) {
    if (position.getBoundingClientRect().top < 110 && position.getBoundingClientRect().top > 110-7200) {
      sidebar.classList.add("sticky_sidebar");
      const width = categories.clientWidth;
      const left = categories.getBoundingClientRect().left;
      sidebar.style.width = width + "px";
      sidebar.style.left = left + "px";
    } else {
      sidebar.classList.remove("sticky_sidebar");
      sidebar.style.width = "initial";
    }
  }
});
