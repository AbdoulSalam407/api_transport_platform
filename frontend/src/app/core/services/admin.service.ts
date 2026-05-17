import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class AdminService {
  private readonly API = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient) {}

  getUsers(role?: string): Observable<any> {
    let params = new HttpParams();
    if (role) params = params.set('role', role);
    return this.http.get(`${this.API}/users/`, { params });
  }

  activerUser(id: number): Observable<any> {
    return this.http.post(`${this.API}/users/${id}/activate/`, {});
  }

  desactiverUser(id: number): Observable<any> {
    return this.http.post(`${this.API}/users/${id}/deactivate/`, {});
  }

  verifierUser(id: number): Observable<any> {
    return this.http.post(`${this.API}/users/verify/${id}/`, {});
  }

  getTrajetsEnAttente(): Observable<any> {
    return this.http.get(`${this.API}/trajets/admin/en-attente/`);
  }

  approuverTrajet(id: number): Observable<any> {
    return this.http.post(`${this.API}/trajets/admin/${id}/approuver/`, {});
  }

  rejeterTrajet(id: number, motif = ''): Observable<any> {
    return this.http.post(`${this.API}/trajets/admin/${id}/rejeter/`, { motif });
  }

  getReservationsEnAttente(): Observable<any> {
    return this.http.get(`${this.API}/reservations/admin/en-attente/`);
  }

  confirmerReservation(id: number): Observable<any> {
    return this.http.post(`${this.API}/reservations/reservations/${id}/confirmer/`, {});
  }

  getAllReservations(): Observable<any> {
    return this.http.get(`${this.API}/reservations/reservations/`);
  }

  getAllTrajets(): Observable<any> {
    return this.http.get(`${this.API}/trajets/trajets/`);
  }
}
