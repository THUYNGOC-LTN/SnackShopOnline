// to get current year
function getYear() {
  var currentDate = new Date();
  var currentYear = currentDate.getFullYear();
  const yearElement = document.querySelector("#displayYear");
  if (yearElement) {
    yearElement.innerHTML = currentYear;
  }
}

getYear();

// Fix navbar collapse toggle for mobile - FORCE JAVASCRIPT HANDLING
document.addEventListener("DOMContentLoaded", function () {
  const navbarToggler = document.querySelector(".navbar-toggler");
  const navbarCollapse = document.querySelector(".navbar-collapse");

  if (navbarToggler && navbarCollapse) {
    // Remove Bootstrap data attributes and handle manually
    navbarToggler.removeAttribute("data-bs-toggle");
    navbarToggler.removeAttribute("data-bs-target");

    // Add click handler
    navbarToggler.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();

      console.log("Navbar toggler clicked!");
      navbarCollapse.classList.toggle("show");

      const isExpanded = navbarCollapse.classList.contains("show");
      navbarToggler.setAttribute("aria-expanded", isExpanded);
    });

    // Close menu when clicking on a link
    const navLinks = navbarCollapse.querySelectorAll("a");
    navLinks.forEach((link) => {
      link.addEventListener("click", function () {
        navbarCollapse.classList.remove("show");
        navbarToggler.setAttribute("aria-expanded", "false");
      });
    });
  }
});

// Get CSRF token from cookie
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrftoken = getCookie("csrftoken");

// Function to update cart count in navbar
function updateCartCount(count) {
  const cartLink = document.querySelector(".cart_link");
  if (!cartLink) return;

  // Find the badge element
  let badge = cartLink.querySelector(".badge");
  if (!badge) {
    // Create badge if it doesn't exist
    badge = document.createElement("span");
    badge.className = "badge";
    cartLink.appendChild(badge);
  }

  // Update badge content and visibility
  if (count > 0) {
    badge.textContent = count;
    badge.style.display = "inline-block";
  } else {
    badge.style.display = "none";
  }
}

// Add to cart functionality with loading indicator
document.addEventListener("DOMContentLoaded", function () {
  const addToCartButtons = document.querySelectorAll(".add-to-cart-btn");

  addToCartButtons.forEach((button) => {
    button.addEventListener("click", async function (e) {
      e.preventDefault();
      const url = this.getAttribute("data-url");
      const originalText = this.innerText;

      // Disable button and show loading state
      this.disabled = true;
      this.innerText = "⏳ Đang thêm...";

      try {
        const headers = {
          "X-Requested-With": "XMLHttpRequest",
        };
        if (csrftoken) {
          headers["X-CSRFToken"] = csrftoken;
        }

        const response = await fetch(url, {
          method: "GET",
          headers: headers,
          credentials: "same-origin",
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.success) {
          this.innerText = "✅ Đã thêm vào giỏ!";

          // Update cart count in navbar
          if (data.cart_count !== undefined) {
            updateCartCount(data.cart_count);
          }

          setTimeout(() => {
            this.innerText = originalText;
            this.disabled = false;
          }, 2000);
        } else {
          alert(
            "❌ Có lỗi xảy ra: " + (data.message || "Không thể thêm vào giỏ"),
          );
          this.innerText = originalText;
          this.disabled = false;
        }
      } catch (error) {
        console.error("Add to cart error:", error);
        alert("❌ Có lỗi xảy ra: " + error.message);
        this.innerText = originalText;
        this.disabled = false;
      }
    });
  });

  // Cart quantity adjustment (increase/decrease) - Optimize UX
  // Cart quantity adjustment - handled in cart.html template to avoid conflicts

  // Remove item from cart - Optimized UX
  const removeButtons = document.querySelectorAll(".remove-item-btn");

  removeButtons.forEach((button) => {
    button.addEventListener("click", async function () {
      const url = this.getAttribute("data-url");

      if (!confirm("Bạn chắc chắn muốn xóa sản phẩm này khỏi giỏ hàng?")) {
        return;
      }

      // Disable button with visual feedback
      this.disabled = true;
      this.style.opacity = "0.6";

      try {
        const headers = {
          "X-Requested-With": "XMLHttpRequest",
        };
        if (csrftoken) {
          headers["X-CSRFToken"] = csrftoken;
        }

        const response = await fetch(url, {
          method: "GET",
          headers: headers,
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

              // Update cart count in navbar
              if (data.cart_count !== undefined) {
                updateCartCount(data.cart_count);
              }

              // Show empty cart message if all items removed
              const remainingCards = document.querySelectorAll(".cart_card");
              if (remainingCards.length === 0) {
                // Show empty cart message instead of reloading
                const cartSection = document.querySelector(".cart_section");
                if (cartSection) {
                  cartSection.innerHTML = `
                    <div class="container">
                      <div class="empty_cart" style="text-align: center; padding: 60px 20px;">
                        <h3>🛒 Giỏ hàng của bạn trống</h3>
                        <p style="color: #666; font-size: 16px; margin: 15px 0;">Hãy thêm sản phẩm để tiếp tục mua sắm</p>
                        <a href="/" style="display: inline-block; padding: 12px 30px; background: #ffbe33; color: #fff; border-radius: 25px; text-decoration: none; font-weight: 600;">← Quay lại trang chủ</a>
                      </div>
                    </div>
                  `;
                }
              }
            }, 300);
          }
        } else {
          alert(
            "❌ Có lỗi xảy ra: " + (data.message || "Không thể xóa sản phẩm"),
          );
          this.disabled = false;
          this.style.opacity = "1";
        }
      } catch (error) {
        console.error("Error:", error);
        alert("❌ Có lỗi xảy ra");
        this.disabled = false;
        this.style.opacity = "1";
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
