// Add here all your JS customizations
 




const copyRight = document.querySelector(".footer__copyright")
copyRight.innerHTML=`Copyright © ${new Date().getFullYear()}. All Rights Reserved.`


const checkIfNumber=(event)=> {

    const phoneInput = document.getElementsByClassName('contact__input_phone');
    const phoneError = document.getElementById('phone-error');
    let timeout;
    
    phoneInput[0].addEventListener('input', () => {
        const phone = phoneInput[0].value.replace(/\D/g, ''); // remove non-digits
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            if (phone.length !== 10) {
            phoneInput[0].setCustomValidity('Please enter a 10-digit phone number.');
            phoneError.textContent = 'Please enter a 10-digit phone number.';
            phoneError.className = 'error-message active';
            } else {
            phoneInput[0].setCustomValidity('');
            phoneError.textContent = '';
            phoneError.className = 'error-message';
            }
        }, 500);
    })

    phoneInput[0].addEventListener('keydown', () => {
        phoneError.textContent = '';
        phoneError.className = 'error-message';
      });
}

const searchClick = (event) => {
  
    const parent = event.currentTarget.closest(".titSearch")
    const searchInput = parent.querySelector(".search-input")
     if (searchInput.classList.contains("active")) {
         searchInput.classList.remove("active")  
         searchInput.style.display="none"

    } else {
         searchInput.classList.add("active") 
         searchInput.style.display="block"
    }
}


const signupClick = (event) => {
    const nameInput = document.querySelector(".contact__input_name")
     window.scrollTo({ top: 0, behavior: 'smooth', });
    
    setTimeout(()=>nameInput.focus(), 700)
    
}





const form = document.querySelector("#contactForm")




function recaptchaCallback() {
    // $('#submitBtn').removeAttr('disabled');
    const button = form.querySelector(".btn-lg")
    button.removeAttribute("disabled")
    button.classList.remove("btn__disabled")
    console.log('done');
};


 
form.addEventListener("change", (event) => {
 

    const name = form.name.value
    const email = form.email.value
    const number = form.phone.value
    const subject = form.subject.value
    const message = form.message.value
    const checkbox = form.check.checked
    const rechapta=form.querySelector(".rechapta")


     // const rechaptaCheckbox = rechapta.querySelector("iframe") 
    // var elmnt = rechaptaCheckbox.contentWindow.document
 


    if (name && email && number && subject  &&  checkbox) {
        rechapta.classList.remove("d-none")
    }

 

    


 })







