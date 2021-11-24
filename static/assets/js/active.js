$(document).ready(() => {
    $('.navbar-nav a').each(function(){
        let location = window.location.protocol + '//' + window.location.host + window.location.pathname
        let link = this.href
        if (location == link) {
            $(this).parent().addClass('active')
        }
    });
    $(function() {

  $("ul.dropdown-menu [data-toggle='dropdown']").on("click", function(event) {
    event.preventDefault();
    event.stopPropagation();

    $(this).siblings().toggleClass("show");


    if (!$(this).next().hasClass('show')) {
      $(this).parents('.dropdown-menu').first().find('.show').removeClass("show");
    }
    $(this).parents('li.nav-item.dropdown.show').on('hidden.bs.dropdown', function(e) {
      $('.dropdown-submenu .show').removeClass("show");
    });

  });

  $("#counter").on("click", function (e) {
      var slug = $(this).attr('data-slug');
      $.ajax({
          url: "counter",
          type: 'get',
          data: {'slug': slug}
      }).done(function (data) {
        console.log('Success');
      }).fail(function (err) {
        console.log('Fail');
      })
  })
});
})