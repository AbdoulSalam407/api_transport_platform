import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, of, throwError } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { Reservation, ReservationCreateRequest } from '../models/reservation.model';

export interface PaginatedResponse<T> {
  count?: number;
  next?: string;
  previous?: string;
  results?: T[];
}

export interface ReservationCreateResponse {
  message: string;
  reservation: Reservation;
}

/**
 * Service pour gérer les réservations
 * Inclut caching, pagination et gestion d'erreurs
 */
@Injectable({ providedIn: 'root' })
export class ReservationService {
  private readonly API = 'http://127.0.0.1:8000';
  private reservationsCache: Map<string, { data: any; timestamp: number }> = new Map();
  private cacheDuration = 5 * 60 * 1000; // 5 minutes

  constructor(private http: HttpClient) {}

  /**
   * Créer une réservation
   */
  creer(data: ReservationCreateRequest): Observable<ReservationCreateResponse> {
    this.clearCache();
    return this.http.post<ReservationCreateResponse>(`${this.API}/reservations/creer/`, data).pipe(
      tap(() => {
        this.clearCache();
      }),
      catchError((error) => {
        console.error('Erreur lors de la création de réservation', error);
        throw error;
      }),
    );
  }

  /**
   * Récupérer mes réservations (avec cache et pagination)
   */
  getMesReservations(
    page = 1,
    pageSize = 20,
    statut?: string,
  ): Observable<PaginatedResponse<Reservation>> {
    const cacheKey = `mes-reservations-${page}-${pageSize}-${statut || 'all'}`;

    // Vérifier le cache
    const cached = this.reservationsCache.get(cacheKey);
    if (cached && Date.now() - cached.timestamp < this.cacheDuration) {
      return of(cached.data);
    }

    let params = new HttpParams()
      .set('page', page.toString())
      .set('page_size', pageSize.toString());

    if (statut) {
      params = params.set('statut', statut);
    }

    return this.http
      .get<PaginatedResponse<Reservation>>(`${this.API}/reservations/mes-reservations/`, {
        params,
      })
      .pipe(
        tap((result) => {
          this.reservationsCache.set(cacheKey, {
            data: result,
            timestamp: Date.now(),
          });
        }),
        catchError((error) => {
          console.error('Erreur lors du chargement des réservations', error);
          return throwError(() => error);
        }),
      );
  }

  /**
   * Récupérer une réservation par ID
   */
  getReservation(id: number): Observable<Reservation> {
    return this.http.get<Reservation>(`${this.API}/reservations/reservations/${id}/`).pipe(
      catchError((error) => {
        console.error('Erreur lors du chargement de la réservation', error);
        throw error;
      }),
    );
  }

  /**
   * Confirmer une réservation
   */
  confirmer(id: number): Observable<any> {
    this.clearCache();
    return this.http.post(`${this.API}/reservations/reservations/${id}/confirmer/`, {}).pipe(
      tap(() => {
        this.clearCache();
      }),
      catchError((error) => {
        console.error('Erreur lors de la confirmation', error);
        throw error;
      }),
    );
  }

  /**
   * Annuler une réservation
   */
  annuler(id: number): Observable<any> {
    this.clearCache();
    return this.http.post(`${this.API}/reservations/reservations/${id}/annuler/`, {}).pipe(
      tap(() => {
        this.clearCache();
      }),
      catchError((error) => {
        console.error("Erreur lors de l'annulation", error);
        throw error;
      }),
    );
  }

  /**
   * Générer un billet
   */
  genererBillet(id: number): Observable<any> {
    return this.http.post(`${this.API}/reservations/reservations/${id}/generer-billet/`, {}).pipe(
      catchError((error) => {
        console.error('Erreur lors de la génération du billet', error);
        throw error;
      }),
    );
  }

  /**
   * Effacer le cache
   */
  private clearCache(): void {
    this.reservationsCache.clear();
  }

  /**
   * Forcer le rafraîchissement du cache
   */
  clearCacheManually(): void {
    this.clearCache();
  }
}
