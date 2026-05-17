export interface User {
  id: number;
  username: string;
  email: string;
  nom: string;
  prenom: string;
  role: 'passager' | 'transporteur' | 'admin';
  telephone: string;
  is_verified: boolean;
  is_actif: boolean;
  date_inscription?: string;
  photo?: string | null;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  token: string;
  user_id: number;
  email: string;
  nom: string;
  prenom: string;
  role: string;
  user: User;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
  nom: string;
  prenom: string;
  role: string;
  telephone?: string;
  nom_entreprise?: string;
  numero_licence?: string;
}

export interface RegisterResponse {
  user: User;
  token: string;
  message?: string;
}
