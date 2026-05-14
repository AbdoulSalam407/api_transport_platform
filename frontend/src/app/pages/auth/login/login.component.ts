import { Component } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

interface AuthUser {
  email: string;
  password: string;
  role: 'passager' | 'transporteur' | 'admin';
  redirect: string;
}

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './login.component.html',
})
export class LoginComponent {
  email = '';
  password = '';
  error = '';

  private readonly users: AuthUser[] = [
    {
      email: 'passager@transport.com',
      password: 'Pass123!',
      role: 'passager',
      redirect: '/dashboard-passager',
    },
    {
      email: 'transporteur@transport.com',
      password: 'Trans123!',
      role: 'transporteur',
      redirect: '/dashboard-transporteur',
    },
    {
      email: 'admin@transport.com',
      password: 'Admin123!',
      role: 'admin',
      redirect: '/dashboard-admin',
    },
  ];

  constructor(private router: Router) {}

  login(): void {
    this.error = '';
    const user = this.users.find(
      (u) => u.email === this.email.trim() && u.password === this.password,
    );

    if (!user) {
      this.error = 'Identifiants incorrects. Vérifiez votre email et mot de passe.';
      return;
    }

    localStorage.setItem('transport_user', JSON.stringify(user));
    this.router.navigate([user.redirect]);
  }
}
