import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, shareReplay, tap } from 'rxjs/operators';
import { Trajet, TrajetSearchParams } from '../models/trajet.model';

export interface PaginatedResponse<T> {
  count?: number;
  next?: string;
  previous?: string;
  results?: T[];
  data?: T[];
}

/**
 * Service pour gérer les trajets
 * Inclut caching, pagination et gestion d'erreurs
 */
@Injectable({ providedIn: 'root' })
export class TrajetService {
  private readonly API = 'http://127.0.0.1:8000';
  private trajetsCache = new Map<string, { data: Observable<any>; timestamp: number }>();
  private cacheDuration = 5 * 60 * 1000; // 5 minutes

  constructor(private http: HttpClient) {}

  /**
   * Récupérer tous les trajets (avec pagination)
   */
  getTrajets(page = 1, pageSize = 20): Observable<PaginatedResponse<Trajet>> {
    let params = new HttpParams()
      .set('page', page.toString())
      .set('page_size', pageSize.toString());

    return this.http.get<PaginatedResponse<Trajet>>(`${this.API}/trajets/trajets/`, {
      params,
    });
  }

  /**
   * Récupérer un trajet par ID
   */
  getTrajet(id: number): Observable<Trajet> {
    return this.http.get<Trajet>(`${this.API}/trajets/trajets/${id}/`);
  }

  /**
   * Lister les trajets disponibles sur la plateforme (tous ou filtrés).
   */
  listerTrajetsDisponibles(
    params: TrajetSearchParams = {},
    page = 1,
    pageSize = 50,
    reservableOnly = false,
  ): Observable<PaginatedResponse<Trajet>> {
    let httpParams = new HttpParams()
      .set('page', page.toString())
      .set('page_size', pageSize.toString());

    if (params.depart) {
      httpParams = httpParams.set('depart', params.depart);
    }
    if (params.destination) {
      httpParams = httpParams.set('destination', params.destination);
    }
    if (params.date) {
      httpParams = httpParams.set('date', params.date);
    }
    if (reservableOnly) {
      httpParams = httpParams.set('reservable_only', 'true');
    }

    return this.http.get<PaginatedResponse<Trajet>>(`${this.API}/trajets/rechercher/`, {
      params: httpParams,
    });
  }

  /**
   * Rechercher des trajets (avec cache)
   */
  rechercher(
    params: TrajetSearchParams,
    page = 1,
    pageSize = 20,
  ): Observable<PaginatedResponse<Trajet>> {
    const cacheKey = JSON.stringify({ ...params, page, pageSize });

    // Vérifier le cache
    const cached = this.trajetsCache.get(cacheKey);
    if (cached && Date.now() - cached.timestamp < this.cacheDuration) {
      return cached.data;
    }

    let httpParams = new HttpParams()
      .set('page', page.toString())
      .set('page_size', pageSize.toString());

    if (params.depart) httpParams = httpParams.set('depart', params.depart);
    if (params.destination) httpParams = httpParams.set('destination', params.destination);
    if (params.date) httpParams = httpParams.set('date', params.date);

    const request$ = this.http
      .get<PaginatedResponse<Trajet>>(`${this.API}/trajets/rechercher/`, {
        params: httpParams,
      })
      .pipe(
        tap((result) => {
          // Mettre en cache
          this.trajetsCache.set(cacheKey, {
            data: of(result),
            timestamp: Date.now(),
          });
        }),
        catchError((error) => {
          console.error('Erreur lors de la recherche de trajets', error);
          return of({ results: [] });
        }),
        shareReplay(1),
      );

    return request$;
  }

  /**
   * Vérifier les places disponibles
   */
  verifierPlaces(id: number): Observable<any> {
    return this.http.get(`${this.API}/trajets/trajets/${id}/places/`);
  }

  /**
   * Créer un nouveau trajet
   */
  creerTrajet(data: Partial<Trajet>): Observable<Trajet> {
    this.clearCache();
    return this.http.post<Trajet>(`${this.API}/trajets/trajets/`, data).pipe(
      tap(() => {
        // Effacer le cache après création
        this.clearCache();
      }),
    );
  }

  /**
   * Modifier un trajet
   */
  modifierTrajet(id: number, data: Partial<Trajet>): Observable<Trajet> {
    this.clearCache();
    return this.http.patch<Trajet>(`${this.API}/trajets/trajets/${id}/`, data).pipe(
      tap(() => {
        this.clearCache();
      }),
    );
  }

  /**
   * Supprimer un trajet
   */
  supprimerTrajet(id: number): Observable<any> {
    this.clearCache();
    return this.http.delete(`${this.API}/trajets/trajets/${id}/`).pipe(
      tap(() => {
        this.clearCache();
      }),
    );
  }

  /**
   * Récupérer les trajets d'un transporteur (avec pagination)
   */
  getMesTrajets(
    page = 1,
    pageSize = 20,
    statut?: string,
    futureOnly = false,
  ): Observable<PaginatedResponse<Trajet>> {
    let params = new HttpParams()
      .set('page', page.toString())
      .set('page_size', pageSize.toString())
      .set('future_only', futureOnly ? 'true' : 'false');

    if (statut) {
      params = params.set('statut', statut);
    }

    return this.http.get<PaginatedResponse<Trajet>>(`${this.API}/trajets/mes-trajets/`, {
      params,
    });
  }

  /**
   * Récupérer les trajets par transporteur (ID)
   */
  getTrajetsParTransporteur(
    transporteurId: number,
    page = 1,
    pageSize = 20,
  ): Observable<PaginatedResponse<Trajet>> {
    let params = new HttpParams()
      .set('page', page.toString())
      .set('page_size', pageSize.toString());

    return this.http.get<PaginatedResponse<Trajet>>(
      `${this.API}/trajets/transporteur/${transporteurId}/trajets/`,
      { params },
    );
  }

  /**
   * Effacer le cache
   */
  private clearCache(): void {
    this.trajetsCache.clear();
  }

  /**
   * Forcer le rafraîchissement du cache
   */
  clearCacheManually(): void {
    this.clearCache();
  }
}
