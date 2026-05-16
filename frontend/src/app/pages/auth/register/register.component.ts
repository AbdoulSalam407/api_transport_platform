import { Component, ChangeDetectorRef } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../../core/services/auth.service';
import { formatHttpErrorMessage, registerFieldHasError } from '../../../core/utils/format-http-error';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [RouterLink, FormsModule, CommonModule],
  templateUrl: './register.component.html',
})
export class RegisterComponent {
  username = '';
  firstName = '';
  lastName = '';
  email = '';
  password = '';
  passwordConfirm = '';
  phoneNumber = '';
  role = 'passager';
  nomEntreprise = '';
  numeroLicence = '';
  error = '';
  loading = false;
  /** Surligne le champ e-mail si le serveur signale un doublon. */
  emailTaken = false;

  constructor(
    private router: Router,
    private authService: AuthService,
    private cdr: ChangeDetectorRef,
  ) {}

  register(): void {
    this.error = '';
    this.emailTaken = false;

    if (this.password !== this.passwordConfirm) {
      this.error = 'Les mots de passe ne correspondent pas.';
      return;
    }

    this.loading = true;

    const data: any = {
      username: this.username || this.email.split('@')[0],
      email: this.email,
      password: this.password,
      password_confirm: this.passwordConfirm,
      nom: this.lastName,
      prenom: this.firstName,
      role: this.role,
      telephone: this.phoneNumber,
    };

    if (this.role === 'transporteur') {
      data.nom_entreprise = this.nomEntreprise;
      data.numero_licence = this.numeroLicence;
    }

    this.authService.register(data).subscribe({
      next: (res) => {
        setTimeout(() => {
          this.loading = false;
          const token = res?.token;
          const user = res?.user;
          if (!token || !user?.id) {
            this.error =
              'Réponse du serveur incomplète après inscription. Réessayez ou connectez-vous si le compte existe déjà.';
            this.cdr.markForCheck();
            return;
          }
          const role = user.role;
          if (role === 'passager') this.router.navigate(['/dashboard-passager']);
          else if (role === 'transporteur') this.router.navigate(['/dashboard-transporteur']);
          else this.router.navigate(['/']);
        });
      },
      error: (err) => {
        setTimeout(() => {
          this.loading = false;
          this.emailTaken = registerFieldHasError(err, 'email');
          this.error =
            formatHttpErrorMessage(err) || "Erreur lors de l'inscription. Vérifiez vos données.";
          this.cdr.markForCheck();
        });
      },
    });
  }
}
