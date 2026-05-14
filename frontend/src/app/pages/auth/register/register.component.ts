import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [RouterLink, FormsModule, CommonModule],
  templateUrl: './register.component.html',
})
export class RegisterComponent {
  firstName = '';
  lastName = '';
  email = '';
  password = '';
  phoneNumber = '';
  role = 'passager';

  register(): void {
    console.log('Register:', {
      firstName: this.firstName,
      lastName: this.lastName,
      email: this.email,
      password: this.password,
      phoneNumber: this.phoneNumber,
      role: this.role,
    });
    // TODO: Implement registration API call
  }
}
