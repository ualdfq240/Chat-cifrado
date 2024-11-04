$(document).ready(function () {
  $(".btn-modal").click(function () {
    //alert($(this).attr("title"));
    var idPublicacion = $(this).attr("title");
    var idBoton = $(this).attr("id");
    // si idBoton es igual a publicacion
    if (idBoton == "publicacion") {
      $("#tituloPublicacion").text("Nueva Publicación");
      // el estado de idPublicacion seria "" 
      $("#idPublicacion").val("");
    } else {
      // si no el rexto sera Comentar Publicación
      $("#tituloPublicacion").text("Comentar Publicación");
      $("#idPublicacion").val(idPublicacion);
    }
  });
});
