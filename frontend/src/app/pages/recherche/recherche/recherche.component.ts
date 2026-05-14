import { Component, OnInit } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-recherche',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './recherche.component.html',
})
export class RechercheComponent implements OnInit {
  userName = 'passager';

  constructor(private router: Router) {}

  ngOnInit(): void {
    const raw = localStorage.getItem('transport_user');
    if (!raw) {
      this.router.navigate(['/login']);
      return;
    }

    const user = JSON.parse(raw) as { email: string; role: string };
    if (user.role !== 'passager') {
      this.router.navigate(['/login']);
      return;
    }

    this.userName = user.email.split('@')[0];
  }
}
