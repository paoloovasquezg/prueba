# laboratorio_1

Primer Laboratorio del curso DBP Sección 1.01


### Primera Pregunta

Crear un Sistema de Información Web que satisfaga los siguientes requerimientos:
<ol>
  <li>Debe tener un formulario con título: Símula tú credito: <b><i>{{nombre del agente enviado desde el servidor.}}</b></i></li>
  <li>El formulario debe tener los siguientes campos como placeholder:
    <ul>Nombres</ul>
    <ul>Apellidos</ul>
    <ul>Sexo</ul>
    <ul>Tipo de documento</ul>
    <ul>Número de documento</ul>
    <ul>Email</ul>
    <ul>Valor del Vehiculo en Soles. En el rango <b>[40000, 100000></b></ul>
    <ul>Monto de cuota Inicial</ul>
  </li>
  <li>Y al final debe estar el botón Simular</li>
  <li>Al hacer click al botón Simular la data debe ser enviado a un servidor web Flask cuyo puerto debe ser <b>5001</b></li>
  <li>La data debe ser guardada en una base de datos relacional <b>postgresql</b> llamada lab10</li>
  <li>La respuesta del servidor al cliente debe ser de forma asincrona (Sin Actualizar la página) mostrando la siguiente información:
    <ul>En caso el resultado de la operación sea mayor o igual a 50000, entonces Mostrar en rojo: No apto para el prestamo.</ul>
    <ul>En caso el resultado de la operación sea menor a 50000, entonces Mostrar todos los datos del usuario y un mensaje en Azul: Usted está apto para el prestamo!</ul>
  </li>
  <li>La operación se calcula de la siguiente forma: 
    <ul>Generar un Número random entre 100 y 1000</ul>
    <ul>El número generado debe ser multiplicado por el Monto de la cuota inicial y a su vez restado de la division del valor del vehiculo entre 500</ul>
  </li>
</ol>

<b>Nota:</b>
<ul>
  <li>Usar flask Migration, el cual implica tener como mínimo un archivo de migración.</li>
  <li>No se aceptará otro servidor de base de datos.</li>
  <li>Subir pruebas de que el código está funcionando a través de screenshots en un caprpeta llamada:  <b>screenshots/</b></li>
  <li>Como mínimo la carpeta screenshots debe 3 imagenes:</li>
  <ol>
    <li>Apto para el prestamo.</li>
    <li>No Apto para el prestamo.</li>
    <li>Screenshot de la base de datos.</li>
  </ol>
  <li>El Laboratorio tiene un tiempo de 2 horas, pasado ese tiempo no se aceptan nuevos commits.</li>
</ul>
![image](https://user-images.githubusercontent.com/106604964/173653302-4ef190d0-51ca-43e8-87bc-fe12c7f40d92.png)
