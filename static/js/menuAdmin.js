const $form = document.querySelector('form');
const $deletedItemInput = document.querySelector('#deleted-item');
const $deleteButtons = document.querySelectorAll('.delete-button');

for (const deleteButton of $deleteButtons) {
  deleteButton.addEventListener('click', () => {
    $deletedItemInput.value = deleteButton.dataset.id;
    $form.submit();
  });
}