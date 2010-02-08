/**
 * Mise a jour de la liste des expert selon une region et une discipline
 * pour le dialog d'assignation des experts
 * 
 * @param id_region
 * @param id_discipline
 */
function update_expert_list(id_region, id_discipline) {
    if(id_discipline=='') {
	id_discipline=0;
    }
    if(id_region=='') {
	id_region=0;
    }
    var url = "/experts/json/" + id_region + "/" + id_discipline;
    var expert_list = $("#id_expert");

    $(expert_list).empty();

    $.getJSON(url, 
	      function(data) {
		  $(expert_list).append("<option selected='selected' value=''>---------</option>");
		  $.each(data, 
			 function(i,exp) {
			     var label = exp.fields.nom + ", " + exp.fields.prenom;
			     $(expert_list).append("<option value='"+exp.pk+"'>"+label+"</option>");
			 });
	      });
}

/**
 * Lorsqu'on change la region du dialog d'assignation des experts
 * 
 * @param event
 */
function on_region_changed(event) {
    var id_region = $(this).val();
    var id_discipline = $("#id_discipline").val();

    update_expert_list(id_region, id_discipline);
}

/**
 * Lorsqu'on change de discipline du dialog d'assignation des experts
 * 
 * @param event
 */
function on_discipline_changed(event) {
    var id_region = $("#id_region").val();
    var id_discipline = $(this).val();
    
    update_expert_list(id_region, id_discipline);
}

/**
 * Lors de l'intialisation du dialog d'assignation d'un expert a une candidature
 * 
 * @param event
 */
function candidature_expert_init(event) {
    var region_field = $("#id_region");
    var discipline_field = $("#id_discipline");
    var candidature_field = $("#candidature_id");

    var tabs = $("#tabs");
    var url_can = "/candidatures/json/" + $(candidature_field).val() + "/";

    $(region_field).bind('change', on_region_changed);
    $(discipline_field).bind('change', on_discipline_changed);

    $(tabs).tabs();

    $.getJSON(url_can, 
	      function(can) {
		  if(can[0].fields.origine_etabl != null) {
		      var url_etab = "/etablissements/json/" + can[0].fields.origine_etabl + "/";
		      $.getJSON(url_etab, 
				function(etab) {
				    var id_region = etab[0].fields.region;
				    var id_discipline = can[0].fields.discipline;

				    $(region_field).val(id_region);
				    $(discipline_field).val(id_discipline);

				    update_expert_list(id_region, id_discipline);
				});
		  } 
		  else {
		      var id_discipline = can[0].fields.discipline;

		      $(discipline_field).val(id_discipline);

		      update_expert_list(0, id_discipline);
		  }
	      });
}