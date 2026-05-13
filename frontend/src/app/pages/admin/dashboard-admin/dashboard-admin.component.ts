import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-dashboard-admin',
  standalone: true,
  templateUrl: './dashboard-admin.component.html',
})
export class DashboardAdminComponent implements OnInit {
  userName = 'Admin';

  constructor(private router: Router) {}

  ngOnInit(): void {
    const raw = localStorage.getItem('transport_user');
    if (!raw) {
      this.router.navigate(['/login']);
      return;
    }

    const user = JSON.parse(raw) as { email: string; role: string };
    if (user.role !== 'admin') {
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