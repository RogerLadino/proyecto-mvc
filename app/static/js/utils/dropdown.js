export function toggleDropdown(event) {
  const header = event.target.closest('.test-header');
  const content = header.nextElementSibling;

  if (content.style.display === 'none' || !content.style.display) {
    content.style.display = 'block';
    event.target.classList.add('expanded');
  } else {
    content.style.display = 'none';
    event.target.classList.remove('expanded');
  }
}

window.toggleDropdown = toggleDropdown; // Make the function globally accessible