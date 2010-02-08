/**
 * Fonction d'affichage du dialog de confirmation de changement de statut
 * 
 * @param message Message a afficher
 * @param formulaire Nom du formulaire a soumettre
 */
function showDialog(message, formulaire) {
    $("#dialog").dialog( 'destroy' );

    $.ui.dialog.defaults.bgiframe = true;
    $("#dialog p.message").html(message);
    $("#form_comment").val('');
    $("#dialog p.comments_fields").show();

    params = {'Annuler': function() {
		  $("#dialog").dialog('close');
	      },
	      'Ok': function() {
		  commentaires = $("#form_comment").val();
		  $('form[name='+formulaire+'] input[name=commentaires]').val(commentaires);
		  $('form[name='+formulaire+']').submit();
		  $("#dialog").dialog('close');
	      }};

    $("#dialog").dialog({ modal: true, 
			  title: 'Confirmation', 
			  buttons :  params}
		       );
    $("#dialog").dialog('open');
}


/**
 * Assignation d'un expert et d'une note à une candidature
 * 
 * @param candidature_id Identificateur de la candidature
 */
function addExpert(candidature_id){
    $("#dialog").dialog( 'destroy' );

    $.ui.dialog.defaults.bgiframe = true;
    $("#dialog p.comments_fields").hide();

    var content = "<iframe id='expert_frame' class='expert' src='/candidatures/expert/add/";
    content += candidature_id;
    content += ">";
    content += "</iframe>";

    $("#dialog p.message").html(content);

    params = {'Annuler': function() {
		  $("#dialog").dialog('close');
	      },
	      'Ok': function() {
		  $(document).ready(
		      function(){
			  var frm_content = $('#expert_frame').contents();
			  var form_expert = $(frm_content).find("form[name='expert_mod']");
			  $(form_expert).submit();
		      });
	      }};
    $("#dialog").dialog({ modal: true, 
			  title: 'Assigner un expert à une candidature', 
			  width: 480,
			  height: 450,
			  buttons :  params
			});
    $("#dialog").dialog('open');
}


/**
 * Assignation d'une note a une candidature pour un expert
 * 
 * @param candidature_id Identificateur de la candidature 
 * @param candidature_expert_id Identificateur d'expert de candidature
 */
function noterCandidature(candidature_id, candidature_expert_id) {
    $("#dialog").dialog( 'destroy' );

    $.ui.dialog.defaults.bgiframe = true;
    $("#dialog p.comments_fields").hide();

    var content = "<iframe id='note_frame' class='note' src='/candidatures/expert/note/";
    content += candidature_id;
    content += "/";
    content += candidature_expert_id;
    content += "></iframe>";

    $("#dialog p.message").html(content);

    params = {'Annuler': function() {
		  $("#dialog").dialog('close');
	      },
	      'Ok': function() {
		  $(document).ready(
		      function(){
			  var frm_content = $('#note_frame').contents();
			  var form_note = $(frm_content).find("form[name='note_mod']");
			  $(form_note).submit();
		      });
	      }};
    $("#dialog").dialog({ modal: true, 
			  title: 'Noter une candidature', 
			  width: 480,
			  height: 410,
			  buttons :  params
			});
    $("#dialog").dialog('open');
}


/**
 * Ajout d'un nouveau critere a un appel d'offre 
 */
function addCriteria() {
    $("#dialog").dialog( 'destroy' );

    $.ui.dialog.defaults.bgiframe = true;
    $("#dialog p.comments_fields").hide();

    var content = "<iframe id='criteria_frame' class='criteria' src='/appels/criteria/></iframe>";
    $("#dialog p.message").html(content);


    params = {'Annuler': function() {
		  $("#dialog").dialog('close');
	      },
	      'Ok': function() {
		  $(document).ready(
		      function(){			 
			  var frm_content = $('#criteria_frame').contents();
			  var form_criteria = $(frm_content).find("form[name='criteria_mod']");
			  $(form_criteria).submit();
		      });
	      }};

    $("#dialog").dialog({ modal: true, 
			  title: 'Ajouter un nouveau critère', 
			  width: 480,
			  buttons :  params}
		       );
    $("#dialog").dialog('open');
}


/**
 * Mise a jour du widget des criteres supplementaires suite a l'ajout
 * d'une nouveau critere a un appel d'offre
 * 
 * @param id_criteria Identificateur du nouveau critere
 * @param criteria_description Description du critere
 */
function after_add_criteria_update(id_criteria, criteria_description) {
    var new_criteria = document.createElement('option');
    new_criteria.value = id_criteria;
    new_criteria.innerHTML = criteria_description;
    $("#id_criteres").append(new_criteria);
    $(new_criteria).attr('selected', 'selected');
    $("#dialog").dialog('close');
}


/**
 * Mise a jour du widget des experts d'une candidature suite a l'assignation
 * d'un nouvel expert pour cette derniere 
 */
function after_add_candidature_expert_update() {
    var frm_content = $('#expert_frame').contents();
    var frm_content_expert_list = $(frm_content).find("#expert_list");
    var parent_expert_list = $("#expert_list");
    $(parent_expert_list).replaceWith(frm_content_expert_list);
    $("#dialog").dialog('close');
}


/**
 * 
 */
function after_noter_candidature_expert_update() {
    var frm_content = $('#note_frame').contents();
    var frm_content_expert_list = $(frm_content).find("#expert_list");
    var parent_expert_list = $("#expert_list");
    $(parent_expert_list).replaceWith(frm_content_expert_list);
    $("#dialog").dialog('close');
}

