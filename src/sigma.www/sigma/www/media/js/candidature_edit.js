/**
 * Soumet la candidature a la sauvegarde en passant
 * par la validation de donnees
 * 
 * @param appel_id Identificateur unique d'une appel d'offre
 * @param candidature_id Identificateur unique d'une candidature
 */
function candidature_save(appel_id, candidature_id) {
    document.forms.candidature_mod.action = "/candidatures/save/";
    document.forms.candidature_mod.action += appel_id;
    document.forms.candidature_mod.action += "/";

    if (candidature_id != 'None') {	
	document.forms.candidature_mod.action += candidature_id;
	document.forms.candidature_mod.action += "/";
    }
    document.forms.candidature_mod.submit();
}


/**
 * Soumet la candidature a la sauvegarde sans passer par la
 * validation de donnees
 * 
 * @param appel_id Identificateur unique d'une appel d'offre
 * @param candidature_id Identificateur unique d'une candidature
 */
function candidature_validate(appel_id, candidature_id) {
    document.forms.candidature_mod.action = "/candidatures/validate/";
    document.forms.candidature_mod.action += appel_id;
    document.forms.candidature_mod.action += "/";

    if (candidature_id != 'None') {	
	document.forms.candidature_mod.action += candidature_id;
	document.forms.candidature_mod.action += "/";
    }
    document.forms.candidature_mod.submit();
}


/**
 * Gestion des dependances entre certains champs
 *
 * Exemple:
 *   - Une case a coche: is_renouvellement
 *   - Un champs nombre de renouvellements
 */
function candidature_field_dependencies() {
  $.getJSON("/candidatures/json/field_dependencies/", function(data) {
      $.each(data[0].fields, function(i,item) {
	  fathe_name = "id_" + i;
	  child_name = "id_" + item;

	  $("#"+fathe_name).bind("change", candidature_field_dependencies);

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
 *  Suppresion d'un expert assigné à une candidature
 * 
 *  @param candidature_id Identificateur unique d'une candidature
 *  @param candidature_expert_id Idenfiticateur unique d'un assignation d'un expert
 *                               a une candidature    
 */
function candidature_delete_expert(candidature_id, candidature_expert_id) {
    var url = '/candidatures/expert/delete/';
    url += candidature_id;
    url += '/';
    url += candidature_expert_id; 
    url += '/';

    $.post(url, function() {
	       $('#expert_'+candidature_expert_id).remove();
	   });
}


/**
 * Initialisation du formulaire d'édition d'une candidature
 */
function candidature_main() {
  // La langue par defaut est le francais
  $.datepicker.setDefaults($.datepicker.regional['fr']);

  $("#id_date_naissance").datepicker({ dateFormat: 'yy-mm-dd' });
  $("#id_date_reception").datepicker({ dateFormat: 'yy-mm-dd' });
  $("#id_mobilite_debut").datepicker({ dateFormat: 'yy-mm-dd' });
  $("#id_diplome_date").datepicker({ dateFormat: 'yy-mm-dd' });
  $("#id_mobilite_fin").datepicker({ dateFormat: 'yy-mm-dd' });

  candidature_field_dependencies();
}
