$(document).ready(function () {
  // Handling the Contact Form in ajax

  var contactform = $('.contact')
  var contactformmethod = contactform.attr('method')
  var contactformendpoint = contactform.attr('action')
  contactform.submit(function (event) {
    event.preventDefault()
    var contactformdata = contactform.serialize()
    var thisform = $(this)
    $.ajax({
      method: contactformmethod,
      url: contactformendpoint,
      data: contactformdata,
      success: function (data) {
        console.log('hello')
        // if this is we need to refresh the form
        contactform[0].reset()
        $.alert({
          title: 'Success!',
          content: data.message, // "Thank for Your Submission",
          theme: 'modern'
        })
      },
      error: function (errorData) {
        $.alert({
          title: 'Oops!',
          content: 'An error Occured',
          theme: 'modern'
        })
      }
    })
  })
  // Auto Search function goes here
  var searchform = $('.search-form')
  var searchinput = searchform.find("[name='q']")// this gives the input in the URL ?q
  var typingTimer
  var typingInterval = 2000// 1.5sec
  var searchBtn = searchform.find("[type='submit']")
  searchinput.keyup(function (_event) {
    // key is released
    clearTimeout(typingTimer)
    typingTimer = setTimeout(performSearch, typingInterval)
  })
  // searchinput.keyup(function(event){
  // key is pressed
  //      clearTimeout(typingTimer)

  // })
  function doSearch () {
    searchBtn.addClass('disabled')
    searchBtn.html("<i class='fa fa-spin fa-spinner'></i>Searching....")
  }
  function performSearch () {
    doSearch()
    var query = searchinput.val()
    setTimeout(function () {
      window.location.href = '/search/?q=' + query
    }, 2000)
  }
  // Cart - adding products and refreshing
  var productForm = $('.product-add-ajax')
  productForm.submit(function (event) {
    event.preventDefault()
    console.log('I made the form not to submit')
    var thisform = $(this)
    var actionEndpoint = thisform.attr('data-endpoint')
    var httpMethod = thisform.attr('method')
    var formData = thisform.serialize()
    $.ajax({
      url: actionEndpoint,
      method: httpMethod,
      data: formData,
      success: function (data) {
        var submitSpan = thisform.find('.submit-span')
        if (data.added) {
          submitSpan.html("In Cart<button type='submit' class='btn btn-link'>Remove??</button>")
        } else {
          submitSpan.html("<button type='submit' class='btn btn-success'>Add to cart</button>")
        }
        var navbarcartcount = $('.navbar-cart-count')
        navbarcartcount.text(data.cartItemCount)
        if (window.location.href.indexOf('carts') != -1) {
          refreshCart()
        }
      },
      error: function (errorData) {
        console.log('error')
        console.log(errorData)
      }
    })
  })
  function refreshCart () {
    console.log('Inside the cart')
    var cartTable = $('.cart-home')
    var cartBody = cartTable.find('.cart-body')
    // cartBody.html("<h1> Changed</h1>")
    var productRows = cartBody.find('.cart-products')
    var refreshCartUrl = window.location.href
    var updateCartUrl = 'api/cart/'
    var updateCartMethod = 'GET'
    var data = {}
    $.ajax({
      url: updateCartUrl,
      method: updateCartMethod,
      data: data,
      success: function (data) {
        var hiddenproduct = $('.cart-item-removeform')
        if (data.products.length > 0) {
          productRows.html('')
          i = data.products.length
          $.each(data.products, function (index, value) {
            var newCart = hiddenproduct.clone()
            newCart.css('display', 'block')
            newCart.find('.remove-product-id').val(value.id)
            cartBody.prepend("<tr><th scope='row'>" + i + "</th><td><a href='" + value.url + "'>" + value.name + '</a>' + newCart.html() + '</td>' + " <td colspan='2'>" + value.price + '</td></tr>')
            i--
          })
          cartBody.find('.carttotal').text(data.total)
        } else {
          window.location.href = refreshCartUrl
        }
      },
      error: function (errorData) {
        console.log('error')
        console.log(errorData)
      }
    })
  }
})
