import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { finalize } from 'rxjs/operators';
import { TrajetService } from '../../../core/services/trajet.service';
import { VehiculeService } from '../../../core/services/vehicule.service';
import { Vehicule } from '../../../core/models/vehicule.model';
import { AuthService } from '../../../core/services/auth.service';
import { formatHttpErrorMessage } from '../../../core/utils/format-http-error';

@Component({
  selector: 'app-creer-trajet',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './creer-trajet.component.html',
})
export class CreerTrajetComponent implements OnInit {
  depart = '';
  destination = '';
  dateDepart = '';
  /** Capacité du véhicule — saisie libre par le transporteur (pas de valeur fixe). */
  placesTotales: number | null = null;
  prixBase = '';
  description = '';
  distanceKm: number | null = null;
  vehiculeId: number | null = null;
  vehicules: Vehicule[] = [];

  loading = false;
  error = '';
  success = '';

  constructor(
    private router: Router,
    private trajetService: TrajetService,
    private vehiculeService: VehiculeService,
    private authService: AuthService,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    this.chargerVehicules();
  }

  chargerVehicules(): void {
    this.vehiculeService.getMesVehicules().subscribe({
      next: (res) => {
        this.vehicules = Array.isArray(res) ? res : (res.results ?? []);
        this.cdr.markForCheck();
      },
    });
  }

  onVehiculeChange(): void {
    const v = this.vehicules.find((x) => x.id === this.vehiculeId);
    if (v) {
      this.placesTotales = v.capacite_places;
    }
  }

  publier(): void {
    this.error = '';
    this.success = '';

    if (!this.depart.trim() || !this.destination.trim() || !this.dateDepart || !this.prixBase) {
      this.error = 'Veuillez remplir tous les champs obligatoires.';
      return;
    }

    if (this.placesTotales == null || this.placesTotales < 1) {
      this.error = 'Indiquez le nombre de places de votre véhicule (minimum 1).';
      return;
    }

    if (this.placesTotales > 99) {
      this.error = 'Le nombre de places ne peut pas dépasser 99.';
      return;
    }

    const dateIso = new Date(this.dateDepart).toISOString();
    if (Number.isNaN(Date.parse(dateIso))) {
      this.error = 'Date de départ invalide.';
      return;
    }

    this.loading = true;

    const payload: Record<string, unknown> = {
      depart: this.depart.trim(),
      destination: this.destination.trim(),
      date_depart: dateIso,
      places_totales: this.placesTotales,
      places_disponibles: this.placesTotales,
      prix_base: this.prixBase,
      statut: 'actif',
      description: this.description.trim(),
    };

    if (this.vehiculeId) {
      payload['vehicule'] = this.vehiculeId;
    }
    if (this.distanceKm != null && this.distanceKm > 0) {
      payload['distance_km'] = this.distanceKm;
    }

    this.trajetService
      .creerTrajet(payload)
      .pipe(
        finalize(() => {
          this.loading = false;
          this.cdr.markForCheck();
        }),
      )
      .subscribe({
        next: () => {
          this.success =
            'Trajet soumis. Un administrateur doit l\'approuver avant qu\'il soit visible aux passagers.';
          this.trajetService.clearCacheManually();
          setTimeout(() => this.router.navigate(['/dashboard-transporteur']), 2000);
        },
        error: (err) => {
          this.error =
            formatHttpErrorMessage(err) || 'Impossible de publier le trajet. Vérifiez les données.';
        },
      });
  }

  retourDashboard(): void {
    this.router.navigate(['/dashboard-transporteur']);
  }

  logout(): void {
    this.authService.clearSession();
    this.router.navigate(['/login']);
  }
}
