import { Component, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import {
  StatistiquesService,
  StatistiquesGlobales,
} from '../../core/services/statistiques.service';
import { Subject } from 'rxjs';
import { finalize, takeUntil } from 'rxjs/operators';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [RouterLink, CommonModule],
  templateUrl: './home.component.html',
})
export class HomeComponent implements OnInit, OnDestroy {
  stats: StatistiquesGlobales | null = null;
  loading = true;
  error: string | null = null;

  private destroy$ = new Subject<void>();

  constructor(
    private statistiquesService: StatistiquesService,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    this.chargerStatistiques();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  private chargerStatistiques(): void {
    this.loading = true;
    this.error = null;

    this.statistiquesService
      .getStatistiquesGlobales()
      .pipe(
        takeUntil(this.destroy$),
        finalize(() => {
          this.loading = false;
          this.cdr.markForCheck();
        }),
      )
      .subscribe({
        next: (response) => {
          this.stats = response.data;
        },
        error: () => {
          this.error = 'Impossible de charger les statistiques. Vérifiez que l\'API Django tourne (port 8000).';
          this.stats = null;
        },
      });
  }

  rafraichirStatistiques(): void {
    this.chargerStatistiques();
  }
}
