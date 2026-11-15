/* site.js: the only JavaScript on the site. Two small, optional extras:
 *   1. Theme button: switch light/dark and remember the choice on this device.
 *   2. Project filter: show only Done / In progress / Learning projects.
 * If this file does not load, the site still works: it follows the device theme and shows all projects.
 */
(function () {
  // ---- 1. Theme button -------------------------------------------------
  var root = document.documentElement;
  var button = document.querySelector(".theme-toggle");

  function currentTheme() {
    // An explicit choice wins; otherwise follow the device setting.
    if (root.dataset.theme) return root.dataset.theme;
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  function showLabel() {
    var next = currentTheme() === "dark" ? "light" : "dark";
    button.textContent = next === "dark" ? "Dark" : "Light";
    button.setAttribute("aria-label", "Switch to " + next + " theme");
  }

  if (button) {
    button.hidden = false;
    showLabel();
    button.addEventListener("click", function () {
      var next = currentTheme() === "dark" ? "light" : "dark";
      root.dataset.theme = next;
      try { localStorage.setItem("theme", next); } catch (e) { /* private mode: just don't remember */ }
      showLabel();
    });
  }

  // ---- 2. Project filter ----------------------------------------------
  var filter = document.querySelector(".filter");
  if (!filter) return;
  filter.hidden = false;
  var buttons = filter.querySelectorAll("button");
  var entries = document.querySelectorAll(".log .entry[data-status]");

  buttons.forEach(function (b) {
    b.addEventListener("click", function () {
      var wanted = b.dataset.filter;          // "all", "done", "progress" or "learning"
      buttons.forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
      entries.forEach(function (e) {
        e.hidden = wanted !== "all" && e.dataset.status !== wanted;
      });
    });
  });
})();
