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
  success = '';
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
    this.success = '';
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
          const user = res?.user;
          if (!user?.id) {
            this.error =
              'Réponse du serveur incomplète après inscription. Réessayez ou connectez-vous si le compte existe déjà.';
            this.cdr.markForCheck();
            return;
          }
          if (user.role === 'admin') {
            this.router.navigate(['/dashboard-admin']);
            return;
          }
          this.authService.clearSession();
          this.success =
            res.message ||
            'Compte créé. Un administrateur doit valider votre compte avant la connexion.';
          this.cdr.markForCheck();
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
