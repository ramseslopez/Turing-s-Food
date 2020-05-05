const $addButtons = document.querySelectorAll('.add-to-cart');
const $cartCounts = document.querySelectorAll('.cart-count');

for (const button of $addButtons) {
  button.addEventListener('click', e => {
    button.innerHTML = `
      <span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>
      Agregando...
    `
    const csrftoken = Cookies.get('csrftoken');
    const data = new FormData();
    data.append('id', e.target.dataset.id);
    fetch(addToCartUrl, {
        method: 'POST',
        body: data,
        headers: {
          'X-CSRFToken': csrftoken,
        }
      })
      .then(response => response.json())
      .then(data => {
        button.innerHTML = 'Añadir al Carrito';
        for (const count of $cartCounts) {
          count.classList.remove('d-none')
          count.textContent = data.count;
        }   
        toastr.options = {
          "closeButton": true,
          "debug": false,
          "newestOnTop": true,
          "progressBar": true,
          "positionClass": "toast-bottom-full-width",
          "preventDuplicates": false,
          "onclick": null,
          "showDuration": "300",
          "hideDuration": "1000",
          "timeOut": "5000",
          "extendedTimeOut": "1000",
          "showEasing": "swing",
          "hideEasing": "linear",
          "showMethod": "fadeIn",
          "hideMethod": "fadeOut"
        }
        toastr.success(data.message);
      })

  })
}
