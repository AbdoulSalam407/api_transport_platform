import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, shareReplay, tap } from 'rxjs/operators';

export interface StatistiquesGlobales {
  total_trajets_actifs: number;
  total_trajets: number;
  trajets_aujourd_hui: number;
  trajets_disponibles: number;
  total_places_disponibles: number;
  derniers_trajets: any[];
}

export interface StatistiquesTransporteur {
  total_trajets: number;
  trajets_actifs: number;
  trajets_termines: number;
  total_places: number;
  places_reservees: number;
  taux_remplissage_moyen: number;
  total_reservations: number;
}

/**
 * Service pour les statistiques globales et utilisateur
 * Inclut caching automatique
 */
@Injectable({ providedIn: 'root' })
export class StatistiquesService {
  private readonly API = 'http://127.0.0.1:8000';
  private statsGlobalesCache$: Observable<any> | null = null;
  private statsTransporteurCache$: Observable<any> | null = null;
  private cacheExpiry = 60000; // 1 minute

  constructor(private http: HttpClient) {}

  /**
   * Récupérer les statistiques globales (cachées)
   */
  getStatistiquesGlobales(): Observable<{ data: StatistiquesGlobales }> {
    // Retourner depuis le cache si disponible
    if (this.statsGlobalesCache$) {
      return this.statsGlobalesCache$;
    }

    // Fetch et cache
    this.statsGlobalesCache$ = this.http
      .get<{ data: StatistiquesGlobales }>(`${this.API}/trajets/statistiques/`)
      .pipe(
        tap(() => {
          // Vider le cache après expiry
          setTimeout(() => {
            this.statsGlobalesCache$ = null;
          }, this.cacheExpiry);
        }),
        shareReplay(1),
        catchError((error) => {
          console.error('Erreur lors du chargement des statistiques', error);
          this.statsGlobalesCache$ = null;
          return of({ data: this.getDefaultStats() });
        }),
      );

    return this.statsGlobalesCache$;
  }

  /**
   * Récupérer les statistiques du transporteur (cachées)
   */
  getStatistiquesTransporteur(): Observable<{ data: StatistiquesTransporteur }> {
    // Retourner depuis le cache si disponible
    if (this.statsTransporteurCache$) {
      return this.statsTransporteurCache$;
    }

    // Fetch et cache
    this.statsTransporteurCache$ = this.http
      .get<{ data: StatistiquesTransporteur }>(`${this.API}/trajets/statistiques-transporteur/`)
      .pipe(
        tap(() => {
          // Vider le cache après expiry
          setTimeout(() => {
            this.statsTransporteurCache$ = null;
          }, this.cacheExpiry);
        }),
        shareReplay(1),
        catchError((error) => {
          console.error('Erreur lors du chargement des statistiques transporteur', error);
          this.statsTransporteurCache$ = null;
          return of({ data: this.getDefaultTransporteurStats() });
        }),
      );

    return this.statsTransporteurCache$;
  }

  /**
   * Forcer le rafraîchissement des statistiques (vider le cache)
   */
  refreshStatistiques(): void {
    this.statsGlobalesCache$ = null;
    this.statsTransporteurCache$ = null;
  }

  private getDefaultStats(): StatistiquesGlobales {
    return {
      total_trajets_actifs: 0,
      total_trajets: 0,
      trajets_aujourd_hui: 0,
      trajets_disponibles: 0,
      total_places_disponibles: 0,
      derniers_trajets: [],
    };
  }

  private getDefaultTransporteurStats(): StatistiquesTransporteur {
    return {
      total_trajets: 0,
      trajets_actifs: 0,
      trajets_termines: 0,
      total_places: 0,
      places_reservees: 0,
      taux_remplissage_moyen: 0,
      total_reservations: 0,
    };
  }
}
