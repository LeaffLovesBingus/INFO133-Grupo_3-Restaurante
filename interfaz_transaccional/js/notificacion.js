
let intervalId = {};

//Función para mostrar la notificación
let showTime = function(id) {

  var myToast = null;
  var barra = null;

  //Switch para determinar el tipo de notificación
  switch(id){
    case 'info':
      myToast = document.getElementById('infocard');
      barra = document.getElementById('infobar');
      break;

    case 'exito':
      myToast = document.getElementById('exitocard');
      barra = document.getElementById('exitobar');
      break;

    case 'alerta':
      myToast = document.getElementById('alertacard');
      barra = document.getElementById('alertabar');
      break;

    case 'error':
      myToast = document.getElementById('errorcard');
      barra = document.getElementById('errorbar');
      break;
  }

  //Mousover y Mouseout para pausar y reanudar la animación
  myToast.addEventListener('mouseover', pauseFrame);
  myToast.addEventListener('mouseout', resumeFrame);

  //Animación de entrada de la notificación
  myToast.classList.add('fade-in');
  myToast.style.display = 'block';

  //Variables para iniciar animación barra
  var width = 100;
  clearInterval(intervalId[id]);
  barra.style.width = "100%";
  intervalId[id] = setInterval(frame, 30);

  //Función animación barra y finalización de la notificación
  function frame() {
    if (width <= 0) {
      clearInterval(intervalId[id]);
      myToast.style.display = "none";

    } else {
      width = width - 0.5;
      barra.style.width = width + "%";
    }
  }

  //Función para pausar el progreso de la barra de la notificación
  function pauseFrame() {
    clearInterval(intervalId[id]);
  }
  
  //Función para reanudar el progreso de la barra de la notificación
  function resumeFrame() {
    clearInterval(intervalId[id]);
    intervalId[id] = setInterval(frame, 40);
  }
}

//Función para cerrar la notificación (Botón X)
let esconder = function(id) {

  var myToast = null;
  var barra = null;

  //Switch para determinar el tipo de notificación
  switch(id){
    case 'info':
      myToast = document.getElementById('infocard');
      barra = document.getElementById('infobar');
      break;

    case 'exito':
      myToast = document.getElementById('exitocard');
      barra = document.getElementById('exitobar');
      break;

    case 'alerta':
      myToast = document.getElementById('alertacard');
      barra = document.getElementById('alertabar');
      break;

    case 'error':
      myToast = document.getElementById('errorcard');
      barra = document.getElementById('errorbar');
      break;
  }

  //Animación de salida de la notificación
  clearInterval(intervalId[id]);
  myToast.style.display = 'none';
  barra.style.width = "100%";

}