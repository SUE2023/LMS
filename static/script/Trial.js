function handleRoleChange() {
    var role = document.getElementById('role').value;
    var vendorFields = document.getElementById('vendorFields');
    if (role === 'vendor') {
        vendorFields.style.display = 'block';
    } else {
        vendorFields.style.display = 'none';
    }
}

function formSubmit(form){
	console.log("Submit");
	//console.log(form.dname.value);
	console.log(form.fname.value);
	console.log(form.sname.value);
	console.log(form.password.value);
	return false;		//To disable default refreshing behavioiur
}



document.addEventListener("DOMContentLoaded", function() {
  let slideIndex = 1;

  function plusSlides(n) {
    showSlides(slideIndex += n);
  }

  function currentSlide(n) {
    showSlides(slideIndex = n);
  }

  function showSlides(n) {
    let i;
    let slides = document.getElementsByClassName("mySlides");
    let dots = document.getElementsByClassName("dot");
    if (n > slides.length) {slideIndex = 1}    
    if (n < 1) {slideIndex = slides.length}
    for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";  
    }
    for (i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex-1].style.display = "block";  
    dots[slideIndex-1].className += " active";
  }

  // Initial call to display the first slide
  showSlides(slideIndex);
});


