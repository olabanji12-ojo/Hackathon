let updateBtn = document.getElementsByClassName('update-cart')



for(let i=0; i< updateBtn.length; i++){
    updateBtn[i].addEventListener('click', function(){
        let productId = this.dataset.product
        let action = this.dataset.action
        console.log("productId:", productId, "action:", action);

        console.log("USER:", user);

        if(user == 'AnonymousUser'){
            console.log('Not logged in');

        }else{
            updateUserOrder(productId, action)
            
        }
     window.location.reload()
    })
    
}

function updateUserOrder(productId, action) {
  console.log('User is logged in, sending data');

  var url = '/updateItem/'; // Corrected URL syntax

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken, // Make sure csrfToken is correctly defined
    },
    body: JSON.stringify({ productId: productId, action: action }),

    })
    .then((response)=>{
        return response.json()
    })
    .then((data)=>{
        console.log('data:', data);
        window.location.reload();

    })
    

}








