// to get current year
function getYear() {
  var currentDate = new Date();
  var currentYear = currentDate.getFullYear();
  document.querySelector("#displayYear").innerHTML = currentYear;
}

getYear();

// Add to cart functionality with loading indicator
document.addEventListener("DOMContentLoaded", function () {
  const addToCartButtons = document.querySelectorAll(".add-to-cart-btn");

  addToCartButtons.forEach((button) => {
    button.addEventListener("click", async function () {
      const url = this.getAttribute("data-url");
      const originalText = this.innerText;

      // Disable button and show loading state
      this.disabled = true;
      this.innerText = "⏳ Đang thêm...";

      try {
        const response = await fetch(url, {
          method: "GET",
          headers: {
            "X-Requested-With": "XMLHttpRequest",
          },
        });

        const data = await response.json();

        if (data.success) {
          this.innerText = "✅ Đã thêm vào giỏ!";
          setTimeout(() => {
            this.innerText = originalText;
            this.disabled = false;
          }, 2000);

          // Update cart count if available
          if (window.updateCartCount) {
            updateCartCount();
          }
        } else {
          alert(
            "❌ Có lỗi xảy ra: " + (data.message || "Không thể thêm vào giỏ"),
          );
          this.innerText = originalText;
          this.disabled = false;
        }
      } catch (error) {
        console.error("Error:", error);
        alert("❌ Có lỗi xảy ra");
        this.innerText = originalText;
        this.disabled = false;
      }
    });
  });

  // Cart quantity adjustment (increase/decrease)
  const qtyButtons = document.querySelectorAll(".qty-btn");

  qtyButtons.forEach((button) => {
    button.addEventListener("click", async function () {
      const url = this.getAttribute("data-url");
      const originalText = this.innerText;

      // Disable button
      this.disabled = true;

      try {
        const response = await fetch(url, {
          method: "GET",
          headers: {
            "X-Requested-With": "XMLHttpRequest",
          },
        });

        const data = await response.json();

        if (data.success) {
          // Update quantity input smoothly
          const cartCard = this.closest(".cart_card");
          const qtyInput = cartCard.querySelector("input[type='number']");
          const totalQtyDiv = cartCard.querySelector(".cart_total_qty");
          const totalPriceDiv = cartCard.querySelector(".cart_total_price");

          if (qtyInput) {
            qtyInput.value = data.quantity;
          }

          // Format currency
          const priceText =
            qtyInput.value +
            " x " +
            new Intl.NumberFormat("vi-VN").format(
              data.item_total / data.quantity,
            ) +
            ".000";

          if (totalQtyDiv) {
            totalQtyDiv.innerText = priceText;
          }

          if (totalPriceDiv) {
            totalPriceDiv.innerText =
              new Intl.NumberFormat("vi-VN").format(data.item_total) +
              ".000 VND";
          }

          // Update cart summary
          const cartTotalPrice = document.getElementById("cart-total-price");
          if (cartTotalPrice) {
            cartTotalPrice.innerText =
              new Intl.NumberFormat("vi-VN").format(data.cart_total) +
              ".000 VND";
          }

          this.disabled = false;
        } else {
          alert(
            "❌ Có lỗi xảy ra: " +
              (data.message || "Không thể cập nhật số lượng"),
          );
          this.disabled = false;
        }
      } catch (error) {
        console.error("Error:", error);
        alert("❌ Có lỗi xảy ra");
        this.disabled = false;
      }
    });
  });

  // Remove item from cart
  const removeButtons = document.querySelectorAll(".remove-item-btn");

  removeButtons.forEach((button) => {
    button.addEventListener("click", async function () {
      const url = this.getAttribute("data-url");

      if (!confirm("Bạn chắc chắn muốn xóa sản phẩm này khỏi giỏ hàng?")) {
        return;
      }

      // Disable button
      this.disabled = true;

      try {
        const response = await fetch(url, {
          method: "GET",
          headers: {
            "X-Requested-With": "XMLHttpRequest",
          },
        });

        const data = await response.json();

        if (data.success) {
          // Remove the cart card smoothly
          const cartCard = this.closest(".cart_card");
          if (cartCard) {
            cartCard.style.transition =
              "opacity 0.3s ease, transform 0.3s ease";
            cartCard.style.opacity = "0";
            cartCard.style.transform = "translateX(20px)";

            setTimeout(() => {
              cartCard.remove();

              // Update cart summary
              const cartTotalPrice =
                document.getElementById("cart-total-price");
              if (cartTotalPrice) {
                cartTotalPrice.innerText =
                  new Intl.NumberFormat("vi-VN").format(data.cart_total) +
                  ".000 VND";
              }

              const cartItemsCount =
                document.getElementById("cart-items-count");
              if (cartItemsCount) {
                const itemCount =
                  document.querySelectorAll(".cart_card").length;
                cartItemsCount.innerText = itemCount + " sản phẩm";
              }

              // Check if cart is empty
              const remainingCards = document.querySelectorAll(".cart_card");
              if (remainingCards.length === 0) {
                location.reload();
              }
            }, 300);
          }
        } else {
          alert(
            "❌ Có lỗi xảy ra: " + (data.message || "Không thể xóa sản phẩm"),
          );
          this.disabled = false;
        }
      } catch (error) {
        console.error("Error:", error);
        alert("❌ Có lỗi xảy ra");
        this.disabled = false;
      }
    });
  });
});

// isotope js
$(window).on("load", function () {
  $(".filters_menu li").click(function () {
    $(".filters_menu li").removeClass("active");
    $(this).addClass("active");

    var data = $(this).attr("data-filter");
    $grid.isotope({
      filter: data,
    });
  });

  var $grid = $(".grid").isotope({
    itemSelector: ".all",
    percentPosition: false,
    masonry: {
      columnWidth: ".all",
    },
  });
});

// nice select
$(document).ready(function () {
  $("select").niceSelect();
});

/** google_map js **/
function myMap() {
  var mapProp = {
    center: new google.maps.LatLng(40.712775, -74.005973),
    zoom: 18,
  };
  var map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
}

// client section owl carousel
$(".client_owl-carousel").owlCarousel({
  loop: true,
  margin: 0,
  dots: false,
  nav: true,
  navText: [],
  autoplay: true,
  autoplayHoverPause: true,
  navText: [
    '<i class="fa fa-angle-left" aria-hidden="true"></i>',
    '<i class="fa fa-angle-right" aria-hidden="true"></i>',
  ],
  responsive: {
    0: {
      items: 1,
    },
    768: {
      items: 2,
    },
    1000: {
      items: 2,
    },
  },
});
