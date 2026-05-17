export interface Trajet {
  id: number;
  transporteur: number;
  vehicule?: number | null;
  transporteur_detail?: any;
  depart: string;
  destination: string;
  date_depart: string;
  date_arrivee_estimee?: string;
  places_totales: number;
  places_disponibles: number;
  /** Places déjà réservées (calculé : totales − disponibles). */
  places_reservees?: number;
  prix_base: string;
  distance_km?: number;
  statut: 'actif' | 'complet' | 'annule' | 'termine';
  validation_statut?: 'en_attente' | 'approuve' | 'rejete';
  validation_statut_affichage?: string;
  motif_rejet?: string;
  description?: string;
  taux_remplissage?: number;
  date_creation?: string;
}

export interface TrajetSearchParams {
  depart?: string;
  destination?: string;
  date?: string;
}
