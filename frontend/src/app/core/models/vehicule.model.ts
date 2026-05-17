export interface Vehicule {
  id: number;
  modele: number;
  modele_detail?: {
    id: number;
    nom: string;
    marque_nom?: string;
    nombre_places: number;
  };
  immatriculation: string;
  nombre_places?: number | null;
  capacite_places: number;
  couleur?: string;
  annee?: number;
  disponible?: boolean;
  en_maintenance?: boolean;
}
