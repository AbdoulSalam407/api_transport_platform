import { Component, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { TrajetService, PaginatedResponse } from '../../../core/services/trajet.service';
import {
  StatistiquesService,
  StatistiquesTransporteur,
} from '../../../core/services/statistiques.service';
import { AuthService } from '../../../core/services/auth.service';
import { Trajet } from '../../../core/models/trajet.model';
import { Subject } from 'rxjs';
import { finalize, takeUntil } from 'rxjs/operators';

@Component({
  selector: 'app-dashboard-transporteur',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './dashboard-transporteur.component.html',
})
export class DashboardTransporteurComponent implements OnInit, OnDestroy {
  // Données utilisateur
  userName = 'Transporteur';
  userId: number | null = null;

  // Trajets
  trajets: Trajet[] = [];
  trajetLoading = false;
  trajetError: string | null = null;
  currentPage = 1;
  pageSize = 10;
  totalTrajets = 0;

  // Statistiques
  stats: StatistiquesTransporteur | null = null;
  statsLoading = false;
  statsError: string | null = null;
  private statsFromApi = false;

  // Math référence pour le template
  Math = Math;

  private destroy$ = new Subject<void>();

  constructor(
    private router: Router,
    private trajetService: TrajetService,
    private statistiquesService: StatistiquesService,
    private authService: AuthService,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    this.verifierAuthentification();
    this.chargerDonnees();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  /**
   * Vérifier l'authentification et le rôle
   */
  private verifierAuthentification(): void {
    const user = this.authService.getCurrentUser();
    if (!user) {
      this.router.navigate(['/login']);
      return;
    }

    if (user.role !== 'transporteur') {
      this.router.navigate(['/login']);
      return;
    }

    this.userName = user.prenom || user.email.split('@')[0];
    this.userId = user.id;
  }

  /**
   * Charger toutes les données du dashboard
   */
  private chargerDonnees(): void {
    this.chargerStatistiques();
    this.chargerMesTrajets();
  }

  /**
   * Charger les statistiques du transporteur
   */
  private chargerStatistiques(): void {
    this.statsLoading = true;
    this.statsError = null;

    this.statistiquesService
      .getStatistiquesTransporteur()
      .pipe(
        takeUntil(this.destroy$),
        finalize(() => {
          this.statsLoading = false;
          this.cdr.markForCheck();
        }),
      )
      .subscribe({
        next: (response) => {
          const body = response as { data?: StatistiquesTransporteur };
          if (body.data) {
            this.stats = body.data;
          }
          this.statsFromApi = true;
        },
        error: (err) => {
          console.error('Erreur lors du chargement des statistiques:', err);
          this.statsFromApi = false;
          this.statsError = null;
        },
      });
  }

  /**
   * Charger mes trajets (avec pagination)
   */
  private chargerMesTrajets(): void {
    this.trajetLoading = true;
    this.trajetError = null;

    this.trajetService
      .getMesTrajets(this.currentPage, this.pageSize)
      .pipe(
        takeUntil(this.destroy$),
        finalize(() => {
          this.trajetLoading = false;
          this.cdr.markForCheck();
        }),
      )
      .subscribe({
        next: (response: PaginatedResponse<Trajet>) => {
          this.trajets = response.results || [];
          this.totalTrajets = response.count ?? this.trajets.length;
          if (!this.statsFromApi) {
            this.calculerStatsDepuisTrajets();
          }
        },
        error: (err) => {
          console.error('Erreur lors du chargement des trajets:', err);
          this.trajetError = 'Impossible de charger vos trajets';
        },
      });
  }

  /**
   * Rafraîchir les données
   */
  rafraichirDonnees(): void {
    this.trajetService.clearCacheManually();
    this.statistiquesService.refreshStatistiques();
    this.chargerDonnees();
  }

  /**
   * Changer de page
   */
  allerPage(page: number): void {
    this.currentPage = page;
    this.chargerMesTrajets();
  }

  /**
   * Filtrer par statut
   */
  filtrerParStatut(statut: string): void {
    this.currentPage = 1;
    // À implémenter avec un paramètre dans le service
    this.chargerMesTrajets();
  }

  /**
   * Logout
   */
  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }

  /**
   * Naviguer vers la création d'un trajet
   */
  allerCreerTrajet(): void {
    this.router.navigate(['/transporteur/creer-trajet']);
  }

  /**
   * Éditer un trajet
   */
  editerTrajet(trajet: Trajet): void {
    this.router.navigate(['/transporteur/editer-trajet', trajet.id]);
  }

  /**
   * Voir détails d'un trajet
   */
  voirTrajet(trajet: Trajet): void {
    this.router.navigate(['/transporteur/trajet', trajet.id]);
  }

  /**
   * Formater la date
   */
  formatDate(date: string): string {
    return new Date(date).toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
    });
  }

  /**
   * Formater l'heure
   */
  formatTime(date: string): string {
    return new Date(date).toLocaleTimeString('fr-FR', {
      hour: '2-digit',
      minute: '2-digit',
    });
  }

  /** Recalcule / complète les stats à partir des trajets chargés (secours si API en échec). */
  private calculerStatsDepuisTrajets(): void {
    if (!this.trajets.length && !this.totalTrajets) {
      if (!this.stats) {
        this.stats = {
          total_trajets: 0,
          trajets_actifs: 0,
          trajets_termines: 0,
          total_places: 0,
          places_reservees: 0,
          taux_remplissage_moyen: 0,
          total_reservations: 0,
        };
      }
      return;
    }

    const total = this.totalTrajets || this.trajets.length;
    let totalPlaces = 0;
    let placesReservees = 0;
    let actifs = 0;
    let enAttente = 0;
    let approuves = 0;

    for (const t of this.trajets) {
      totalPlaces += t.places_totales ?? 0;
      placesReservees += (t.places_totales ?? 0) - (t.places_disponibles ?? 0);
      if (t.statut === 'actif') actifs++;
      if (t.validation_statut === 'en_attente') enAttente++;
      if (t.validation_statut === 'approuve') approuves++;
    }

    const taux = totalPlaces > 0 ? Math.round((placesReservees / totalPlaces) * 1000) / 10 : 0;

    this.stats = {
      total_trajets: total,
      trajets_actifs: actifs,
      trajets_termines: this.trajets.filter((t) => t.statut === 'termine').length,
      trajets_en_attente: enAttente,
      trajets_approuves: approuves,
      total_places: totalPlaces,
      places_reservees: placesReservees,
      places_disponibles: totalPlaces - placesReservees,
      taux_remplissage_moyen: taux,
      total_reservations: 0,
      reservations_confirmees: 0,
      reservations_en_attente: 0,
    };
    this.cdr.markForCheck();
  }

  /**
   * Calculer le taux de remplissage
   */
  getPlacesReservees(trajet: Trajet): number {
    if (trajet.places_reservees != null) {
      return trajet.places_reservees;
    }
    return Math.max(0, (trajet.places_totales ?? 0) - (trajet.places_disponibles ?? 0));
  }

  /** Places encore disponibles à la réservation. */
  getPlacesLibres(trajet: Trajet): number {
    return trajet.places_disponibles ?? 0;
  }

  /** Capacité définie par le transporteur à la création du trajet. */
  getCapaciteDefinie(trajet: Trajet): number {
    return trajet.places_totales ?? 0;
  }

  estComplet(trajet: Trajet): boolean {
    return this.getPlacesLibres(trajet) === 0 && (trajet.places_totales ?? 0) > 0;
  }

  getCouleurPlaces(trajet: Trajet): string {
    if (this.estComplet(trajet)) {
      return 'bg-red-100 text-red-800';
    }
    if (this.getPlacesReservees(trajet) > 0) {
      return 'bg-amber-100 text-amber-800';
    }
    return 'bg-green-100 text-green-800';
  }

  getTauxRemplissage(trajet: Trajet): number {
    if (!trajet.places_totales) {
      return 0;
    }
    return Math.round((this.getPlacesReservees(trajet) / trajet.places_totales) * 100);
  }

  /**
   * Obtenir la couleur du statut
   */
  getCouleurValidation(statut?: string): string {
    const map: Record<string, string> = {
      en_attente: 'bg-amber-100 text-amber-800',
      approuve: 'bg-green-100 text-green-800',
      rejete: 'bg-red-100 text-red-800',
    };
    return map[statut ?? ''] ?? 'bg-slate-100 text-slate-800';
  }

  getCouleurStatut(statut: string): string {
    switch (statut) {
      case 'actif':
        return 'bg-green-100 text-green-800';
      case 'complet':
        return 'bg-orange-100 text-orange-800';
      case 'termine':
        return 'bg-blue-100 text-blue-800';
      case 'annule':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-slate-100 text-slate-800';
    }
  }
}
