import { Component, OnInit, OnDestroy } from '@angular/core';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import {
  StatistiquesService,
  StatistiquesGlobales,
} from '../../core/services/statistiques.service';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [RouterLink, CommonModule],
  templateUrl: './home.component.html',
})
export class HomeComponent implements OnInit, OnDestroy {
  // Statistiques
  stats: StatistiquesGlobales | null = null;
  loading = true;
  error: string | null = null;

  private destroy$ = new Subject<void>();

  constructor(private statistiquesService: StatistiquesService) {}

  ngOnInit(): void {
    this.chargerStatistiques();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  /**
   * Charger les statistiques globales
   */
  private chargerStatistiques(): void {
    this.loading = true;
    this.error = null;

    this.statistiquesService
      .getStatistiquesGlobales()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (response) => {
          this.stats = response.data;
          this.loading = false;
        },
        error: (err) => {
          console.error('Erreur lors du chargement des statistiques:', err);
          this.error = 'Impossible de charger les statistiques. Veuillez réessayer.';
          this.loading = false;
        },
      });
  }

  /**
   * Rafraîchir les statistiques
   */
  rafraichirStatistiques(): void {
    this.statistiquesService.refreshStatistiques();
    this.chargerStatistiques();
  }
}
