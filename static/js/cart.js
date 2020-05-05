const $removeButtons = document.querySelectorAll('.remove-button');
const $cartCounts = document.querySelectorAll('.cart-count');
const $total = document.querySelector('#total');
const $infoText = document.querySelector('#info-text');

for (const button of $removeButtons) {
  button.addEventListener('click', e => {
    button.innerHTML = `
      <span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>
      Eliminando...
    `
    const id = e.target.dataset.id
    const csrftoken = Cookies.get('csrftoken');
    const data = new FormData();
    data.append('id', id);
    fetch(removeFromCartUrl, {
        method: 'POST',
        body: data,
        headers: {
          'X-CSRFToken': csrftoken,
        }
      })
    .then(response => response.json())
    .then(data => {
      button.innerHTML = 'Eliminar del Carrito';
      const article = document.querySelector(`#item-${id}`)
      article.remove()
      for (const count of $cartCounts) {
        if (count.classList.contains('mobile')) {
          count.textContent = `(${data.count})`;
        } else {
          count.textContent = data.count;
        }
        if (!data.count) {
          count.classList.add('d-none');
          $total.remove();
          $infoText.textContent = 'Aún no hay artículos, puedes volver al menú a agregar productos al carrito'
        } else {
          $total.textContent = `Total: $${data.total}`
        }
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
      toastr.error(data.message);
    })
    .catch(() => {
      toastr.error('Ha ocurrido un error al eliminar el producto');
    })
  });
}
