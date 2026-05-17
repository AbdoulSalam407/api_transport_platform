export interface Reservation {
  id: number;
  passager: number;
  passager_detail?: any;
  trajet: number;
  trajet_detail?: any;
  nombre_places: number;
  numero_siege?: string;
  sieges_affichage?: string;
  prix_total: string;
  statut: 'en_attente' | 'confirmee' | 'annulee' | 'terminee';
  statut_affichage?: string;
  recupere?: boolean;
  date_reservation?: string;
}

export interface ReservationCreateRequest {
  trajet: number;
  nombre_places: number;
}
