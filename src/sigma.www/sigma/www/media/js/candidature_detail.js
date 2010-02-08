/**
 * Declencheur de l'ouverture du rejet d'une candidature
 */
function rejeter_candidature() {
    showDialog(gettext('Êtes-vous certains de vouloir rejeter cette candidature?'), 'rejeter');
}

/**
 * Declencheur de l'ouverture de l'acceptation d'une candidature
 */
function accepter_candidature(candidature_id) {
    $.getJSON("/candidatures/json/warning_messages/"+candidature_id+"/Accepter/", 
	      function(data) {
		  message = gettext('Êtes-vous certains de vouloir accepter cette candidature?');

		  criteres = "";

		  $.each(data, function(i,item) {
			     criteres += "<li class='error_message'>" + item + "</li>";
			 });
		  if (criteres.length > 0) {		      
		      message += "<p class='error_message'>Attention:";
		      message += "<ul class='error_message'>";
		      message += criteres;
		      message += "</ul>";
		      message += "</p>";
		  }
		 
		  showDialog(message, 'accepter');
	      });
}

/**
 * Declencheur de l'ouverture du classement d'une candidature
 */
function classer_candidature() {
    showDialog(gettext('Êtes-vous certains de vouloir classer cette candidature?'), 'classer');
}

/**
 * Declencheur de l'ouverture du declassement d'une candidature
 */
function declasser_candidature() {
    showDialog(gettext('Êtes-vous certains de vouloir déclasser cette candidature?'), 'declasser');
}

/**
 * Declencheur de l'ouverture de la selection d'une candidature
 */
function selectionner_candidature() {
    showDialog(gettext('Êtes-vous certains de vouloir sélectionner cette candidature?'), 'selectionner');
}

/**
 * Declencheur de l'ouverture de la mise en attente d'une candidature
 */
function attendre_candidature() {
    showDialog(gettext('Êtes-vous certains de vouloir mettre en attente cette candidature?'), 'attendre');
}

/**
 * Declencheur de l'ouverture du reveille d'une candidature
 */
function reveiller_candidature() {
    showDialog(gettext('Êtes-vous certains de vouloir sélectionner cette candidature en attente?'), 'reveiller');
}

/**
 * Declencheur de la desistion d'une candidature
 */
function desister_candidature() {
    showDialog(gettext('Êtes-vous certains que ce candidat s\'est désisté?'), 'desister');
}

/**
 * Declencheur de l'attribution d'une bourse a une candidature
 */
function boursier_candidature() {
    showDialog(gettext('Êtes-vous certains de vouloir attribuer à ce candidat une bourse?'), 'boursier');
}

/**
 * Declencheur de la completude d'une candidature
 */
function completer_candidature() {
    showDialog(gettext('Êtes-vous certains que cette candidature est complète?'), 'completer');
}