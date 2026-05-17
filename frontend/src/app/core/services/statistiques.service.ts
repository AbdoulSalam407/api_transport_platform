import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

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
  trajets_en_attente?: number;
  trajets_approuves?: number;
  total_places: number;
  places_reservees: number;
  places_disponibles?: number;
  taux_remplissage_moyen: number;
  total_reservations: number;
  reservations_confirmees?: number;
  reservations_en_attente?: number;
}

@Injectable({ providedIn: 'root' })
export class StatistiquesService {
  private readonly API = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient) {}

  getStatistiquesGlobales(): Observable<{ data: StatistiquesGlobales }> {
    return this.http
      .get<{ status?: string; data: StatistiquesGlobales }>(`${this.API}/trajets/statistiques/`)
      .pipe(
        map((res) => ({ data: res.data ?? this.getDefaultStats() })),
        catchError((error) => {
          console.error('Erreur lors du chargement des statistiques', error);
          return of({ data: this.getDefaultStats() });
        }),
      );
  }

  getStatistiquesTransporteur(): Observable<{ data: StatistiquesTransporteur }> {
    return this.http
      .get<{ data: StatistiquesTransporteur }>(`${this.API}/trajets/statistiques-transporteur/`)
      .pipe(
        map((res) => ({ data: res.data ?? this.getDefaultTransporteurStats() })),
        catchError((error) => {
          console.error('Erreur lors du chargement des statistiques transporteur', error);
          return of({ data: this.getDefaultTransporteurStats() });
        }),
      );
  }

  refreshStatistiques(): void {
    /* Conservé pour compatibilité ; plus de cache bloquant. */
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
