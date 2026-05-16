export interface Trajet {
  id: number;
  transporteur: number;
  transporteur_detail?: any;
  depart: string;
  destination: string;
  date_depart: string;
  date_arrivee_estimee?: string;
  places_totales: number;
  places_disponibles: number;
  places_reservees?: number;
  prix_base: string;
  distance_km?: number;
  statut: 'actif' | 'complet' | 'annule' | 'termine';
  description?: string;
  taux_remplissage?: number;
  date_creation?: string;
}

export interface TrajetSearchParams {
  depart?: string;
  destination?: string;
  date?: string;
}
