/**
 * Declencheur de l'ouverture d'un appel d'offre
 */
function ouvrir_appel() {
    showDialog(gettext('Êtes-vous certains de vouloir ouvrir l\'appel d\'offre'), 'ouvrir');
}

/**
 * Declencheur de l'analyse d'un appel d'offre
 */
function analyser_appel() {
    showDialog(gettext('Êtes-vous certains de vouloir débuter la période d\'analyse'), 'analyser');
}

/**
 * Declencheur de l'evaluation d'un appel d'offre
 */
function evaluer_appel() {
    showDialog(gettext('Êtes-vous certains de vouloir débuter la période d\'évaluation'), 'evaluer');
}

/**
 * Declencheur de la selection d'un appel d'offre
 */
function selectionner_appel() {
    showDialog(gettext('Êtes-vous certains de vouloir débuter la période de sélection'), 'selectionner');
}

/**
 * Declencheur de la notification d'un appel d'offre
 */
function notifier_appel() {
    showDialog(gettext('Êtes-vous certains de vouloir débuter la période de notification'), 'notifier');
}

/**
 * Declencheur du suivie d'un appel d'offre
 */
function suivre_appel() {
    showDialog(gettext('Êtes-vous certains de vouloir débuter la période de suivie'), 'suivre');
}

/**
 * Declencheur de la fermeture d'un appel d'offre
 */
function fermer_appel() {
    showDialog(gettext('Êtes-vous certains de vouloir fermer l\'appel d\'offre'), 'fermer');
}
