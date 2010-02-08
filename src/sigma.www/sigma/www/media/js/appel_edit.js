/**
 * Soumission du formulaire de mise a jour et d'enregistrement
 * d'un appel d'offre
 */
function appel_edit() {
  document.forms.appel_mod.submit();
}

/**
 * Gestion des dependances entre certains champs
 *
 * Exemple:
 *   - Une case a coche: is_renouvellement
 *   - Un champs nombre de renouvellements
 */
function appel_field_dependencies() {
  $.getJSON("/appels/json/field_dependencies/", function(data) {
      $.each(data[0].fields, function(i,item) {
	  fathe_name = "id_" + i;
	  child_name = "id_" + item;

	  $("#"+fathe_name).bind("change", appel_field_dependencies);
	  
	  empty = false;

	  if($("#"+fathe_name).attr('type')=='select-one') {
	    empty = $("#"+fathe_name).val() != '';
	  }
	  else{
	    empty = !$("#"+fathe_name).is(':checked');
	  }

	  if(empty) {
	    $("#"+child_name).hide();
	    $("label[for='"+child_name+"']").hide();
	  } else {
	    $("#"+child_name).show();
	    $("label[for='"+child_name+"']").show();
	  }
	});
    });
}

/**
 * Remplissage des champs selon les parametres des projets et 
 * vidage si aucun projet n'est selectionne
 *
 * @param projet_id L'identificateur du projet selectionne
 */
function fill_data(projet_id) {
    if(projet_id) {
	$.getJSON("/projets/categorie/json/" +projet_id+ "/", 
		  function(data, textStatus) {
		      override = data[0].fields["exception_possible"]
		      $.each(data[0].fields, function(i,item) {
				 widget = $("#id_" + i);
				 if($(widget).attr('type')=='checkbox') {
    				     $(widget).attr('checked', item);
				     if(!override) {
					 $(widget).attr('onclick', 'return false');
				     }
				 }
			     else {
				 if(item == null){
				     item = "";
				 }  
				 $(widget).val(item);
				 
				 if(!override) {
				     $(widget).attr('readonly', 'readonly');
				 }
			     }
			     });
		  });
    }
    else
    {
	$.getJSON("/categories/json/", 
		  function(data, textStatus) {
		      $.each(data[0].fields, function(i, item) {
				 widget = $("#id_" + i);
				 if($(widget).attr('type')=='checkbox'){ 
				     $(widget).attr('checked', false);
				 }
				 else {
				     $(widget).val("");
				 }
		    });
		  });
    }
}

/**
 * Mise a jour des blocs de champs selon le projet, donc la categorie selectionnee
 *
 * @param projet_id L'identificateur du projetposte choisit
 */
function update_blocs_champs(projet_id) {
    blocwidget = $("#bloc");
    blocwidget.empty();
      if(projet_id) {
	// on récupère les blocs de champs
	$.getJSON("/blocs/blocs/json/" +projet_id+ "/",
          function(data) {
            $.each(data, function(i,blocchamps) {
                // on récupère les champs
                $.get("/champs/appel/json/" + blocchamps.pk + "/",
                    function(champs) {
                    blocwidget.append("<div id=bloc_" + blocchamps.pk + "><h2>" + blocchamps.fields.libelle + "</h2>");
                    bloc = $("#bloc_" + blocchamps.pk);
                    bloc.append("<ul>" + champs + "</ul>");
                    blocwidget.append("</div>");
                }, "html");
              });
          });
      }
}

/*******************************************************************************
 * Bloc principal lance lorsque la page est completement rendue
 */
function appel_main() {
    // Ajout d'un datepicker qui facilite l'entree d'une date de fin d'inscription
    $("#id_inscription_date_debut").datepicker({ dateFormat: 'yy-mm-dd' });
    $("#id_inscription_date_fin").datepicker({ dateFormat: 'yy-mm-dd' });
    $("#id_mobilite_date_debut").datepicker({ dateFormat: 'yy-mm-dd' });
    $("#id_mobilite_date_fin").datepicker({ dateFormat: 'yy-mm-dd' });
    
    // La langue par defaut
    $.datepicker.setDefaults($.datepicker.regional['fr']);

    // Gestion des dependances entre les champs
    appel_field_dependencies();

    // Procedure de mise a jour des champs correspondant a la categorie
    // du projet qui a ete selectionne.
    // @triggers Par le selecteur #id_projet
    $("#id_projetposte").bind("change", 
			      function() {
				  projet_id = this.value;
				  
				  update_blocs_champs(projet_id);
				  
				  fill_data(projet_id);
				  
				  appel_field_dependencies();
			      }
			     );
}
