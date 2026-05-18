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
