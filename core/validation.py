"""Constantes et filtres pour la validation administrative."""

VALIDATION_EN_ATTENTE = 'en_attente'
VALIDATION_APPROUVE = 'approuve'
VALIDATION_REJETE = 'rejete'

VALIDATION_STATUT_CHOICES = [
    (VALIDATION_EN_ATTENTE, 'En attente de validation'),
    (VALIDATION_APPROUVE, 'Approuvé'),
    (VALIDATION_REJETE, 'Rejeté'),
]

VALIDATION_STATUT_LABELS = {
    VALIDATION_EN_ATTENTE: 'En attente de validation admin',
    VALIDATION_APPROUVE: 'Approuvé par l\'admin',
    VALIDATION_REJETE: 'Rejeté par l\'admin',
}
