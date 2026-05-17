import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { finalize } from 'rxjs/operators';
import { TrajetService } from '../../../core/services/trajet.service';
import { VehiculeService } from '../../../core/services/vehicule.service';
import { Vehicule } from '../../../core/models/vehicule.model';
import { Trajet } from '../../../core/models/trajet.model';
import { formatHttpErrorMessage } from '../../../core/utils/format-http-error';

@Component({
  selector: 'app-editer-trajet',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './editer-trajet.component.html',
})
export class EditerTrajetComponent implements OnInit {
  trajetId = 0;
  depart = '';
  destination = '';
  dateDepart = '';
  placesTotales = 1;
  prixBase = '';
  description = '';
  distanceKm: number | null = null;
  vehiculeId: number | null = null;
  placesReservees = 0;

  vehicules: Vehicule[] = [];
  loading = false;
  loadingTrajet = true;
  error = '';
  success = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private trajetService: TrajetService,
    private vehiculeService: VehiculeService,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    this.trajetId = Number(this.route.snapshot.paramMap.get('id'));
    if (!this.trajetId) {
      this.router.navigate(['/dashboard-transporteur']);
      return;
    }
    this.chargerVehicules();
    this.chargerTrajet();
  }

  chargerVehicules(): void {
    this.vehiculeService.getMesVehicules().subscribe({
      next: (res) => {
        this.vehicules = Array.isArray(res) ? res : (res.results ?? []);
        this.cdr.markForCheck();
      },
    });
  }

  chargerTrajet(): void {
    this.trajetService.getTrajet(this.trajetId).subscribe({
      next: (t) => {
        this.depart = t.depart;
        this.destination = t.destination;
        this.dateDepart = this.toDatetimeLocal(t.date_depart);
        this.placesTotales = t.places_totales;
        this.placesReservees = (t.places_totales ?? 0) - (t.places_disponibles ?? 0);
        if (t.places_reservees != null) {
          this.placesReservees = t.places_reservees;
        }
        this.prixBase = String(t.prix_base);
        this.description = t.description ?? '';
        this.distanceKm = t.distance_km ?? null;
        this.vehiculeId = t.vehicule ?? null;
        this.loadingTrajet = false;
        this.cdr.markForCheck();
      },
      error: () => {
        this.error = 'Trajet introuvable.';
        this.loadingTrajet = false;
        this.cdr.markForCheck();
      },
    });
  }

  onVehiculeChange(): void {
    const v = this.vehicules.find((x) => x.id === this.vehiculeId);
    if (v && this.placesReservees === 0) {
      this.placesTotales = v.capacite_places;
    }
  }

  enregistrer(): void {
    this.error = '';
    this.success = '';

    if (this.placesTotales < this.placesReservees) {
      this.error = `Minimum ${this.placesReservees} place(s) (déjà réservées).`;
      return;
    }

    const dateIso = new Date(this.dateDepart).toISOString();
    this.loading = true;

    const payload: Record<string, unknown> = {
      depart: this.depart.trim(),
      destination: this.destination.trim(),
      date_depart: dateIso,
      places_totales: this.placesTotales,
      prix_base: this.prixBase,
      description: this.description.trim(),
    };
    if (this.vehiculeId) {
      payload['vehicule'] = this.vehiculeId;
    }
    if (this.distanceKm != null && this.distanceKm > 0) {
      payload['distance_km'] = this.distanceKm;
    }

    this.trajetService
      .modifierTrajet(this.trajetId, payload)
      .pipe(
        finalize(() => {
          this.loading = false;
          this.cdr.markForCheck();
        }),
      )
      .subscribe({
        next: () => {
          this.success = 'Trajet mis à jour.';
          this.trajetService.clearCacheManually();
          setTimeout(() => this.router.navigate(['/dashboard-transporteur']), 1500);
        },
        error: (err) => {
          this.error = formatHttpErrorMessage(err) || 'Impossible de modifier le trajet.';
        },
      });
  }

  private toDatetimeLocal(iso: string): string {
    const d = new Date(iso);
    const pad = (n: number) => String(n).padStart(2, '0');
    return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
  }
}
