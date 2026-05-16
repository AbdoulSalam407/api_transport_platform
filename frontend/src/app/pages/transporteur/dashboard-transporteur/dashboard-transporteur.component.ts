import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { TrajetService, PaginatedResponse } from '../../../core/services/trajet.service';
import {
  StatistiquesService,
  StatistiquesTransporteur,
} from '../../../core/services/statistiques.service';
import { AuthService } from '../../../core/services/auth.service';
import { Trajet } from '../../../core/models/trajet.model';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'app-dashboard-transporteur',
  standalone: true,
  imports: [CommonModule],
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

  // Math référence pour le template
  Math = Math;

  private destroy$ = new Subject<void>();

  constructor(
    private router: Router,
    private trajetService: TrajetService,
    private statistiquesService: StatistiquesService,
    private authService: AuthService,
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
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (response) => {
          this.stats = response.data;
          this.statsLoading = false;
        },
        error: (err) => {
          console.error('Erreur lors du chargement des statistiques:', err);
          this.statsError = 'Impossible de charger les statistiques';
          this.statsLoading = false;
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
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (response: PaginatedResponse<Trajet>) => {
          this.trajets = response.results || [];
          this.totalTrajets = response.count || 0;
          this.trajetLoading = false;
        },
        error: (err) => {
          console.error('Erreur lors du chargement des trajets:', err);
          this.trajetError = 'Impossible de charger vos trajets';
          this.trajetLoading = false;
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

  /**
   * Calculer le taux de remplissage
   */
  getTauxRemplissage(trajet: Trajet): number {
    return Math.round(
      ((trajet.places_totales - trajet.places_disponibles) / trajet.places_totales) * 100,
    );
  }

  /**
   * Obtenir la couleur du statut
   */
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
