document.querySelectorAll('.box').forEach(function(box) {
    box.addEventListener('click', function() {
         // Get data from hidden input fields
        var title = document.getElementById('titleHidden_').value;
        var askValue = document.getElementById('askValueHidden_').value;
        var userLevels = document.getElementById('userLevelsHidden_').value;
        

        // Populate form fields in the popup with the retrieved data
        document.getElementById('title').value = title ;
        document.getElementById('askValue').checked = askValue === 'True';
        document.getElementById('userLevels').checked = userLevels === 'True';

        document.getElementById('popup').classList.remove('hide');
 
        // document.getElementById('saveButton').textContent="Save";
        // document.querySelector('#popup [name="delete"]').classList.remove('hide');
        document.querySelector('.popblur').classList.add('blur');
    });
  });



  function closeForm() {
    const formPopup = document.getElementById('popup');
    // formPopup.style.animation = 'zoomOut 0.3s forwards'; // Apply zoom-out animation
    // formPopup.style.display = 'none';
    formPopup.classList.add('hide');
    document.querySelector('.popblur').classList.remove('blur');
    
    // setTimeout(() => {

    // }, 300); // Delay hiding the form to allow animation to complete
}

document.getElementById('set_float').addEventListener('click', function() {


  const formPopup = document.getElementById('popup');
  formPopup.classList.remove('hide');
  document.querySelector('.popblur').classList.add('blur');


  // visibility of the popup
  // formPopup.style.animation = 'zoomIn 0.3s forwards';
  document.getElementById('saveButton').classList.remove('hide');
  

  var inputs = document.querySelectorAll('#popup input, #popup textarea');
  
  inputs.forEach(function(input) {
    input.disabled = false;
  });

 
 
});