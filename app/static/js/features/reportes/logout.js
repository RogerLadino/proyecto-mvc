document.addEventListener('DOMContentLoaded', function () {
      const userMenu = document.querySelector('.user-menu');
      if(userMenu) {
        const dropdown = userMenu.querySelector('.dropdown-content');
        userMenu.addEventListener('click', function (event) {
          event.stopPropagation();
          dropdown.classList.toggle('show');
        });
      }
      window.addEventListener('click', function () {
        const shownDropdown = document.querySelector('.dropdown-content.show');
        if (shownDropdown) {
          shownDropdown.classList.remove('show');
        }
      });
    });