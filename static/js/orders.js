
const $takeButtons = document.querySelectorAll('.take-button');
const $takeForm = document.querySelector('#take-form');
const $takenOrderInput = document.querySelector('#taken-order');

for (const button of $takeButtons) {
  button.addEventListener('click', () => {
    $takenOrderInput.value = button.dataset.id;
    $takeForm.submit();
  })
}


const $pickupButtons = document.querySelectorAll('.pickup-button');
const $pickupForm = document.querySelector('#pickup-form');
const $pickupOrderInput = document.querySelector('#pickup-order');

for (const button of $pickupButtons) {
  button.addEventListener('click', () => {
    $pickupOrderInput.value = button.dataset.id;
    $pickupForm.submit();
  })
}