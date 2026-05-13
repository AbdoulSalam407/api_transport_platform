import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-dashboard-transporteur',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard-transporteur.component.html',
})
export class DashboardTransporteurComponent implements OnInit {
  userName = 'transporteur';

  constructor(private router: Router) {}

  ngOnInit(): void {
    const raw = localStorage.getItem('transport_user');
    if (!raw) {
      this.router.navigate(['/login']);
      return;
    }

    const user = JSON.parse(raw) as { email: string; role: string };
    if (user.role !== 'transporteur') {
      this.router.navigate(['/login']);
      return;
    }

    this.userName = user.email.split('@')[0];
  }

  logout(): void {
    localStorage.removeItem('transport_user');
    this.router.navigate(['/login']);
  }
}
