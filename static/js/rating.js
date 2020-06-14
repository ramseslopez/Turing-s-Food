Vue.component('star-rating', VueStarRating.default);

const vm = new Vue({
  el: '#app',
  data: {
    rating: 0,
  },
});
