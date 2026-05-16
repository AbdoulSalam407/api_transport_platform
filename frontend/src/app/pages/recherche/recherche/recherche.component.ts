import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TrajetService } from '../../../core/services/trajet.service';
import { AuthService } from '../../../core/services/auth.service';
import { Trajet } from '../../../core/models/trajet.model';

@Component({
  selector: 'app-recherche',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './recherche.component.html',
})
export class RechercheComponent implements OnInit {
  userName = '';
  depart = '';
  destination = '';
  date = '';
  trajets: Trajet[] = [];
  loading = false;
  error = '';
  searched = false;

  constructor(
    private router: Router,
    private trajetService: TrajetService,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    if (!this.authService.isLoggedIn()) {
      this.router.navigate(['/login']);
      return;
    }
    const user = this.authService.getUser();
    this.userName = user ? `${user.prenom} ${user.nom}` : '';
  }

  rechercher(): void {
    this.loading = true;
    this.error = '';
    this.searched = true;

    this.trajetService.rechercher({
      depart: this.depart,
      destination: this.destination,
      date: this.date
    }).subscribe({
      next: (res) => {
        this.loading = false;
        this.trajets = Array.isArray(res) ? res : (res.results ?? []);
      },
      error: () => {
        this.loading = false;
        this.error = 'Erreur lors de la recherche.';
      }
    });
  }

  reserver(trajet: Trajet): void {
    this.router.navigate(['/reservation'], { state: { trajet } });
  }
}
