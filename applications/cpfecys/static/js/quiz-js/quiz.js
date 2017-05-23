function EliminarPregunta(objeto)
{
    var id = objeto.substr(17,objeto.length);
    var liaeliminar = "Pregunta_"+id;
    $("#"+liaeliminar).remove();
}

function DeshabilitarPregunta(id)
{
    document.getElementById("Guardar_Pregunta"+id).setAttribute("disabled", true);
    document.getElementById("Campo_Pregunta"+id).setAttribute("disabled", true);
}

function GruardarQuiz()
{
    if(preguntas.length>0)
    {
        //alert("hay: "+preguntas.length+" preguntas registradas");
        var corr_quiz = submitLoad("quiz","obtenerQuiz",""); 
        JsonCorretaltivo = JSON.parse(corr_quiz);
        //var JsonQuiz = '{"id":"'+JsonCorretaltivo.value+'", "curso": "curso","seccion": "A", "propietario":"auxiliar/catedratico", "preguntas":[ ';
        var JsonQuiz = '{[';
        
        for (var i = 0; i < preguntas.length; i++) {

            if(i!=0)
            {
                JsonQuiz += ', '+preguntas[i];
            }
            else
            {
                JsonQuiz += preguntas[i];
            }
            
        }

        userid = document.getElementById("userid").name;
        projectid = document.getElementById("project_id").name;
        periodo_id = document.getElementById("period_id").name;
        idproject = document.getElementById("id_project").name;
        JsonQuiz += ']}';
        var parametros = "?id="+JsonCorretaltivo.value+"&jsonquiz="+JsonQuiz+"&uid="+userid+"&project="+projectid;
        submitLoad("quiz","GuardarQuiz",parametros);
        alert("Se ha guardado el cuestionario con id: "+JsonCorretaltivo.value);
        var par = "?period="+periodo_id+"&project="+idproject;
        
        window.location.href = "http://"+document.domain+":8000/cpfecys/quiz/home_quiz"+par;
    }
    else
    {
        alert("No hay preguntas");
    }
    
}

function DeshabilitarRespuesta(i, cabecera)
{
    cabecera.childNodes[i].childNodes[0].setAttribute("disabled", true);
    cabecera.childNodes[i].childNodes[1].setAttribute("disabled", true);
    cabecera.childNodes[i].childNodes[3].setAttribute("disabled", true);
}

function GuardarPregunta(objeto)
{
   //Declaracion de valirbales
   var id = objeto.substr(16,objeto.length);
   var valor = document.getElementById("Campo_Pregunta"+id).value;
   var cabecera = document.getElementById("Respuestas_P"+id);
   var tipo = cabecera.getAttribute("name");
   var respuestas = cabecera.childNodes.length ;
   var jsonPregunta = '{"id_pregunta":"pregunta_'+id+'", "value":"'+valor+'", "tipo":"'+tipo+'","respuesta":';
   var tmprespuesta = "";

   if (valor != "")
   {

    switch(tipo)
    {
        case "multiple":
            jsonPregunta += '[';
            var vacias = 0
            
            for (var i = 0; i < respuestas; i++) 
            {
                if (cabecera.childNodes[i].childNodes[0].value=="")
                vacias++;
            }

            if(vacias!=0)
            {
                alert("Llene todas las casilla de preguntas");
            }
            else
            {
                for (var i = 0; i < respuestas; i++) 
                {
                    if (cabecera.childNodes[i].childNodes[0].value!="")
                    {
                        /*
                        Sintaxis respuesta a armar
                        {
                        "value": "respuesta1",
                        "correcta": "true"
                         }
                        */
                        var prefijo="";
                        if (tmprespuesta!="")
                            prefijo=", "
                        
                        tmprespuesta = prefijo + '{"value":"'+cabecera.childNodes[i].childNodes[0].value+'", "correcta":"'+cabecera.childNodes[i].childNodes[1].checked+'"}';
                        DeshabilitarRespuesta(i,cabecera);
                    }
                     jsonPregunta += tmprespuesta; 
                }
                jsonPregunta += ']}';
                preguntas.push(jsonPregunta);     
            }
            DeshabilitarPregunta(id);
            document.getElementById("btAddRespuesta"+id).setAttribute("disabled", true);
            break;

        case "directa":
            //alert("directa");
            if (cabecera.childNodes[2].value!="")
            {
                tmprespuesta = '"'+cabecera.childNodes[2].value+'"';
                jsonPregunta += tmprespuesta;
                jsonPregunta += '}';
                preguntas.push(jsonPregunta);
                DeshabilitarPregunta(id);
                cabecera.childNodes[2].setAttribute("disabled", true);
            }
            else
            {
                alert("Debe ingresar la respuesta antes de guardar");
            }
            break;

        case "veracidad":
            //alert("veracidad");
            if(cabecera.childNodes[2].childNodes[0].checked)
            {
                tmprespuesta = '"true"';
            }
            else
            {
                tmprespuesta = '"false"';
            }
            jsonPregunta += tmprespuesta;
            jsonPregunta += '}';
            preguntas.push(jsonPregunta);
            DeshabilitarPregunta(id);
            cabecera.childNodes[2].childNodes[0].setAttribute("disabled", true);
            cabecera.childNodes[3].childNodes[0].setAttribute("disabled", true);
            break;
    }
    //alert("La pregunta es: "+jsonPregunta);
    //alert("Todas sus respuestas estan ingresadas");
    //alert("Hay "+preguntas.length+" registradas");
     
   }
   else
   {   
     alert("Debe ingresar la informacion de la pregunta para poder guardarla");
   }
}

function EliminarRespuesta(objeto)
{
    var id = objeto.substr(18,objeto.length);
    //alert(id);
    //alert(objeto);
    var liaeliminar = "Respuesta_"+id;
    //alert(liaeliminar);
    $("#"+liaeliminar).remove();
}

function AgregarRespuesta(objeto)
{
    var id = objeto.substr(14,objeto.length);
    var idlo = "Respuestas_P"+id;
    respuesta =      '<li id="Respuesta_'+idr+'"><input type="text">'
                        +'<input type="checkbox"> Correcta '
                        +'<button id="Eliminar_Respuesta'+idr+'" type="button" class="btn btn-danger" onclick="EliminarRespuesta(this.id)">X</button>'
                        +'</li>';
    $("#"+idlo).append(respuesta);
    GetIDR();

}

$(document).ready(

    function()
    {

    var Pregunta;
    //var respuesta;

    function CrearRespuesta()
    {
        respuesta =      '<li id="Respuesta_'+idr+'"><input type="text">'
                        +'<input type="checkbox"> Correcta '
                        +'<button id="Eliminar_Respuesta'+idr+'" type="button" class="btn btn-danger" onclick="EliminarRespuesta(this.id)">X</button>'
                        +'</li>';
        

    }



    function CrearEncabezado()
    {
        var contenido = '<form id="Formulario_1" class="form-inline">'
                        +'<a style="cursor:pointer;"><h4>Ingrese la pregunta:</h4></a>'
                        +'<textarea class="estilotextarea2" cols="1" rows="1"></textarea>'
                        +'<button id="Guardar_Pregunta'+idp+'" type="button" class="btn btn-primary" onclick="GuardarPregunta(this.id)"><i class="icon-ok-sign icon-white"></i></button>'
                        +'<button id="Eliminar_Pregunta'+idp+'" type="button" class="btn btn-danger" onclick="EliminarPregunta(this.id)"><i class="icon-trash icon-white"></i></button>'
                        +'</form>';

                        //alert(contenido);
        return(contenido);

    }

    function CrearPregunta(tipo)
    {                                //Creamos la función que recoje los dos parámetros
               if (tipo==1)
               {
                //alert(encabezado);
                
                var encabezado = '<form id="Formulario_P'+idp+'" class="form-inline">'
                        +'<a style="cursor:pointer;"><h4>Ingrese la pregunta:</h4></a>'
                        +'<textarea id="Campo_Pregunta'+idp+'"class="estilotextarea2" cols="1" rows="1"></textarea>'
                        +'<button id="Guardar_Pregunta'+idp+'" type="button" class="btn btn-primary" onclick="GuardarPregunta(this.id)"><i class="icon-ok-sign icon-white"></i></button>'
                        +'<button id="Eliminar_Pregunta'+idp+'" type="button" class="btn btn-danger" onclick="EliminarPregunta(this.id)"><i class="icon-trash icon-white"></i></button>'
                        +'</form>';

                pregunta=        '<li id="Pregunta_'+idp+'" name="tipo1"><div class="navbar" data-intro="Pregunta de opcion multiple" {{pass}} >'
                                +'<div class="navbar-inner">'
                                + encabezado
                                +'</br>'
                                +'</div>'
                                +'<div class="well" id="div_repuestas">'
                                +'<fieldset>'
                                    +'<a style="cursor:pointer;">Respuestas:</a><br>'
                                    +'<ol id="Respuestas_P'+idp+'" type=A name="multiple">'
                                    +'</ol>'
                                +'</fieldset>'
                                +'<button id="btAddRespuesta'+idp+'" type="button" class="btn btn-primary" onclick="AgregarRespuesta(this.id)">+ Agregar una nueva respuesta</button>'
                                +'</div>'
                                +'</div>'
                                +'</li>';
                                 
                              }
               else if (tipo==2)
               {
                    var encabezado = '<form id="Formulario_P'+idp+'" class="form-inline">'
                        +'<a style="cursor:pointer;"><h4>Ingrese la pregunta:</h4></a>'
                        +'<textarea id="Campo_Pregunta'+idp+'"class="estilotextarea2" cols="1" rows="1"></textarea>'
                        +'<button id="Guardar_Pregunta'+idp+'" type="button" class="btn btn-primary" onclick="GuardarPregunta(this.id)"><i class="icon-ok-sign icon-white"></i></button>'
                        +'<button id="Eliminar_Pregunta'+idp+'" type="button" class="btn btn-danger" onclick="EliminarPregunta(this.id)"><i class="icon-trash icon-white"></i></button>'
                        +'</form>';

                    pregunta = '<li id="Pregunta_'+idp+'" name="tipo2"><div class="navbar" data-intro="Pregunta de opcion multiple" {{pass}} >'
                                +'<div class="navbar-inner">'
                                + encabezado
                                +'<br>'
                                +'</div>'
                                +'<div class="well" id="div_repuestas">'
                                +'<fieldset id="Respuestas_P'+idp+'" name="directa">'
                                    +'<a style="cursor:pointer;">Ingrese respuesta corta:</a><br>'
                                    +'<input type="text">'
                                +'</fieldset>'
                                +'</div>'
                                +'</div>';
               }

               else
               {
                var encabezado = '<form id="Formulario_P'+idp+'" class="form-inline">'
                        +'<a style="cursor:pointer;"><h4>Ingrese la pregunta:</h4></a>'
                        +'<textarea id="Campo_Pregunta'+idp+'"class="estilotextarea2" cols="1" rows="1"></textarea>'
                        +'<button id="Guardar_Pregunta'+idp+'" type="button" class="btn btn-primary" onclick="GuardarPregunta(this.id)"><i class="icon-ok-sign icon-white"></i></button>'
                        +'<button id="Eliminar_Pregunta'+idp+'" type="button" class="btn btn-danger" onclick="EliminarPregunta(this.id)"><i class="icon-trash icon-white"></i></button>'
                        +'</form>';

                pregunta = '<li id="Pregunta_'+idp+'" name="tipo3"><div class="navbar" data-intro="Pregunta falso o verdadero" {{pass}} >'
                            +'<div class="navbar-inner">'
                            + encabezado
                            +'<br>'
                            +'</div>'
                            +'<div class="well" id="div_repuestas">'
                            +'<fieldset id="Respuestas_P'+idp+'" name="veracidad">'
                            +'<a style="cursor:pointer;">Seleccione el valor de verdad:</a><br>'
                            +'<label><input type="radio" name="Opcion'+idp+'" value="verdadero" checked> Verdadero</input></label>'
                            +'<label><input type="radio" name="Opcion'+idp+'" value="falso" checked> Falso</input></label>'
                            +'</fieldset></div></div>';
               }
                
    }

    $("#btAddTipo1").click(function(){
        //$("#contenedorDePreguntas").append(multiple);
        CrearPregunta(1);
        $("#contenedorDePreguntas").append(pregunta);  
        
        var idPreg ="Respuestas_P"+idp;
        for (var i = 0; i < 5; i++) {
            CrearRespuesta();
            $("#"+idPreg).append(respuesta);
            GetIDR();
        }
             
        GetID();
        
    });

    $("#btAddTipo2").click(function(){
        CrearPregunta(3);
        $("#contenedorDePreguntas").append(pregunta);
        GetID();
    });

    $("#btAddTipo3").click(function(){
        CrearPregunta(2);
        $("#contenedorDePreguntas").append(pregunta);
        GetID();
    });

    $("#btnContinuar").click(function(){
        GruardarQuiz();
    });

});