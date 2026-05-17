import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import {
  LoginRequest,
  LoginResponse,
  RegisterRequest,
  RegisterResponse,
  User,
} from '../models/user.model';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly API = 'http://127.0.0.1:8000';
  private readonly TOKEN_KEY = 'transport_token';
  private readonly USER_KEY = 'transport_user';

  constructor(private http: HttpClient) {}

  login(credentials: LoginRequest): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${this.API}/users/login/`, credentials).pipe(
      tap((res) => {
        localStorage.setItem(this.TOKEN_KEY, res.token);
        localStorage.setItem(
          this.USER_KEY,
          JSON.stringify(
            res.user ?? {
              id: res.user_id,
              email: res.email,
              nom: res.nom,
              prenom: res.prenom,
              role: res.role,
            },
          ),
        );
      }),
    );
  }

  register(data: RegisterRequest): Observable<RegisterResponse> {
    return this.http.post<RegisterResponse>(`${this.API}/users/register/`, data).pipe(
      tap((res) => {
        localStorage.setItem(this.TOKEN_KEY, res.token);
        localStorage.setItem(this.USER_KEY, JSON.stringify(res.user));
      }),
    );
  }

  logout(): Observable<any> {
    return this.http.post(`${this.API}/users/logout/`, {}).pipe(tap(() => this.clearSession()));
  }

  getProfile(): Observable<User> {
    return this.http.get<User>(`${this.API}/users/me/`);
  }

  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  getUser(): User | null {
    const raw = localStorage.getItem(this.USER_KEY);
    return raw ? JSON.parse(raw) : null;
  }

  getCurrentUser(): User | null {
    return this.getUser();
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }

  getRole(): string | null {
    return this.getUser()?.role ?? null;
  }

  clearSession(): void {
    localStorage.removeItem(this.TOKEN_KEY);
    localStorage.removeItem(this.USER_KEY);
  }
}
